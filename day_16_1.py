def parse_rule(field_rule):
    ranges = [ r.split("-") for r in field_rule.split(" or ") ]
    ranges = [(int(a), int(b)) for a,b in ranges]
    def is_valid(x):
        return any( a <= x <= b for (a,b) in  ranges)
    return is_valid

def is_valid_ticket(ticket, validators):
    fields = map(int, ticket.split(","))
    field_error_rate = 0
    for field in fields:
        if not any( is_valid_field(field) for is_valid_field in validators.values() ):
            field_error_rate += field
    return field_error_rate

def main():
    with open("inputs/day16.txt") as f:
        [
            rules,
            my_ticket,
            nearby_tickets
        ] = f.read().split("\n\n")

        validators = {}

        for field in rules.splitlines():
            field_name, field_rule = field.split(":")
            validators[field_name] = parse_rule(field_rule)
        
        ticket_scanning_error_rate = 0
        for nearby_ticket in nearby_tickets.splitlines()[1:]:

            ticket_scanning_error_rate += is_valid_ticket(nearby_ticket, validators)
                
        print(ticket_scanning_error_rate)

if __name__ == "__main__":
    main()