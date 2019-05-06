# run with python -i to explore the syntax trees of the examples

from lark import Lark 

with open("pierpaolo.lark") as handle:
    grammar = handle.readlines()

parser = Lark(''.join(grammar))

small_example = parser.parse("""PIERPAOLO SMALL
INTRODUCE MARIA
VALE
BRAVO
""")

example = parser.parse("""PIERPAOLO README

 INTRODUCE MARIA
 MOVE MARIA LEFT
 VALE

 INTRODUCE MATEO
 (BEWARE MARIA WHO IS UNSCHEDULED)
 MOVE MATEO RIGHT
 VALE
 BRAVO

""")
