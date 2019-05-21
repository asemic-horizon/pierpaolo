from lark import Lark 
import sys
from itertools import product, combinations
from dataclasses import dataclass
from enum import Enum
from typing import List
from random import randint
# grammar
with open("pierpaolo.lark") as handle: grammar = ''.join(handle.readlines())
parser = Lark(grammar)

def sub(subtree,i=0): return subtree.children[i].value
def make_ascii_line(marker_values, max_width = 80, max_abs = 10):
    factor = max_width/(2*max_abs)
    line = max_width*"-"
    for marker in marker_values:
        pos = int(factor * (marker_values[marker] + max_abs))
        line = line[:pos-1]+marker[0]+line[pos:]
    return line
# program

with open(sys.argv[1]) as file: program = ''.join(file.readlines())
tree = parser.parse(program)
#print(tree.pretty())

class Plan(str,Enum):
    left = "LEFF"
    right = "RIGHT"
    random = "RANDOM"
    fixed = "FIXED"

@dataclass
class Thing:
    name: str
    plan : Plan = "RANDOM"
    xpos = 0
    history = [0]

    def move(self):
        if self.plan == "RIGHT": self.xpos +=1
        elif self.plan == "LEFT": self.xpos -=1
        elif self.plan == "RANDOM": self.xpos += randint(-1,1)
        self.history.append(self.xpos)
 
    def set_plan(self, plan):
        self.plan = plan

class Opera:
    def __init__(self):
        self.cast = dict()
        self.time = 0

    def _pos_dict(self):
        return {persona: self.cast[persona].xpos for persona in self.cast}
    def _check_collisions(self):
        return all([self.cast[a].xpos!=self.cast[b].xpos\
                    for a,b in combinations(self.cast.keys(),2)])

    def vale(self):
        self.time +=1
        for persona in self.cast.values(): persona.move()

        if not self._check_collisions():
            print(16*'CRASH')
        print(f'{self.time:03d}'+make_ascii_line(self._pos_dict()))

    def run_act(self,subtree):
        for token in subtree.find_data('introduction'):
            name = sub(token)
            assert name not in self.cast, f"{name} PREVIOUSLY INTRODUCED ALREADY"
            self.cast[name] = Thing(name = name, plan="RANDOM")

        for token in subtree.find_data('motion'):
            self.cast[sub(token)].set_plan(sub(token,1))
        self.vale()

opera = Opera()
print(83*"=")
for num, verse in enumerate(tree.find_data('step')):
    #print(verse)
    opera.run_act(verse)
    #print(f"-------------\nACT{num+1}: DRAMATIS PERSONAE", '\n', opera.cast)