import numpy as np

def parse_rule(field_rule):
    ranges = [ r.split("-") for r in field_rule.split(" or ") ]
    ranges = [(int(a), int(b)) for a,b in ranges]
    def is_valid(x):
        return any( a <= x <= b for (a,b) in  ranges)
    return is_valid

def parse_ticket(ticket):
    return [ int(x) for x in ticket.split(",") ]

def main():
    with open("inputs/day16.txt") as f:
        [
            rules,
            my_ticket,
            nearby_tickets_string
        ] = f.read().split("\n\n")
        nearby_tickets = [ parse_ticket(ticket) for ticket in nearby_tickets_string.splitlines()[1:] ]

        my_ticket = parse_ticket(my_ticket.splitlines()[1])

        validators = {}

        for field in rules.splitlines():
            field_name, field_rule = field.split(":")
            validators[field_name] = parse_rule(field_rule)
        
        ticket_scanning_error_rate = 0


        def is_valid_ticket(ticket):
            return all(
                any( rule(val) for rule in validators.values() )
                for val in ticket
            )

        nearby_tickets = list(filter(is_valid_ticket, nearby_tickets))
        nearby_tickets = np.array(list(nearby_tickets))

        def validate_column(field_name, validator, column):
            for i, val in enumerate(column):
                if not validator(val):
                    return False
            return True

        mapping = {}

        while len(validators) > 0:
            for (i, column) in enumerate(nearby_tickets.T):                
                candidate_fields = []

                for (field_name, field_rule) in validators.items():
                    if validate_column(field_name, field_rule, column):
                        candidate_fields.append(field_name)

                if len(candidate_fields) == 1:
                    field_name = candidate_fields[0]
                    del validators[field_name]
                    mapping[field_name] = i
        

        total = 1
        for (field, index) in mapping.items():
            if field.startswith("departure"):
                total *= my_ticket[index]
        print(total)
            
if __name__ == "__main__":
    main()