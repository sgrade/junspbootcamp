
statement1 = """    ge-0/0/9 {
        description "Receiver2 to R5";
        unit 0 {
            family inet {
                address 172.27.1.2/24;
            }
        }
    }
"""


def remove_statement(conf):
    return conf.replace(statement1)

