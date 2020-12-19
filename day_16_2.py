import numpy as np

def parse_rule(field_rule):
    ranges = [ r.split("-") for r in field_rule.split(" or ") ]
    ranges = [(int(a), int(b)) for a,b in ranges]
    def is_valid(x):
        return any( a <= x <= b for (a,b) in  ranges)
    return is_valid

def parse_ticket(ticket):
    return [ int(x) for x in ticket.split(",") ]

def get_inputs(string_input):
    [
        rules,
        my_ticket,
        nearby_tickets_string
    ] = string_input.split("\n\n")
    
    nearby_tickets = map(parse_ticket, nearby_tickets_string.splitlines()[1:])
    my_ticket = parse_ticket(my_ticket.splitlines()[1])

    validators = {}

    for field in rules.splitlines():
        field_name, field_rule = field.split(":")
        validators[field_name] = parse_rule(field_rule)
    return nearby_tickets, my_ticket, validators

def validate_column(validator, column):
    return all( validator(val) for val in column )

def is_valid_ticket(validators):
    def _is_valid_ticket(ticket):
        return all(
            any( rule(val) for rule in validators.values() )
            for val in ticket
        )
    return _is_valid_ticket

def main():
    with open("inputs/day16.txt") as f:
        nearby_tickets, my_ticket, validators = get_inputs( f.read() )
        nearby_valid_tickets = np.array( list(filter(is_valid_ticket(validators), nearby_tickets)) )
        result_mapping = {}

        while len(validators) > 0:
            for (i, column) in enumerate(nearby_valid_tickets.T):                

                candidate_fields = [
                    field_name for (field_name, field_rule) in validators.items()
                    if validate_column(field_rule, column)
                ]

                if len(candidate_fields) == 1:
                    field_name = candidate_fields[0]
                    del validators[field_name]
                    result_mapping[field_name] = i

        total = np.prod([ 
            my_ticket[index] for (field_name, index) in filter(
                lambda item: item[0].startswith("departure"),
                result_mapping.items()
            )
        ])
        print(total)
            
if __name__ == "__main__":
    main()