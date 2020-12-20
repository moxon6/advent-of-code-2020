import re

parser = re.compile("(?P<rule_id>\d*): (?P<rule>.*)")

def parse_element(el):
    el = el.strip()
    try:
        return int(el)
    except:
        if el == "|":
            return el
        else:
            return el[1:-1]

with open("inputs/day19_2.txt") as f:

    rule_section, message_section = f.read().split("\n\n")
    
    parsed_rules = [ parser.match(line.strip()).groupdict() for line in rule_section.splitlines() ]

    rules = {
        int( rule["rule_id"] ): rule["rule"] for rule in parsed_rules
    }

    MAX_DEPTH = 400

    def generate_regex_pattern(rule_index, depth = 0):

        if depth > MAX_DEPTH:
            # Hopefully the match doesn't go this deep...
            return "()"
        
        rule = rules[rule_index]
        
        elements = [ parse_element(element) for element in rule.split(" ") ]
        sub_rules = [ 
            generate_regex_pattern(el, depth + 1)
                if isinstance(el, int)
                else el
                for el in elements
        ]
        
        result = "".join(sub_rules)

        if len(result) > 1:
            return f"({result})"
        else:
            return result[0]

    pattern = f"^{ generate_regex_pattern(0) }$"
    matcher = re.compile(pattern)    
    messages = [x.strip() for x in message_section.splitlines()]

    total = sum( bool(matcher.match(message)) for message in messages )
    print(f"Total matches: {total}")
