from lib.json_schema_parser import JSON_Schema_Parser
import sys

if __name__=='__main__':
    if len(sys.argv) > 1:
        schema = JSON_Schema_Parser(sys.argv[1])
        print ""
        print "Here is your pretty print json Schema:"
        print ""
        schema.print_it()
        print ""

    else:
        print "pass in the string as the first arguement"
        sys.exit(0)
