from lark import Lark 
import sys
from itertools import product, combinations
from dataclasses import dataclass
from enum import Enum
from typing import List
from random import randint, choice
# grammar
with open("pierpaolo.lark") as handle: grammar = ''.join(handle.readlines())
parser = Lark(grammar)

def sub(subtree,i=0): return subtree.children[i].value
def make_ascii_line(marker_values, max_width = 80, max_abs = 10):
    factor = max_width/(2*max_abs)
    line = max_width*"-"
    for marker in marker_values:
        pos = int(factor * (marker_values[marker] + max_abs))
        if pos>0 and pos<max_width:
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
    xpos : int = 0
    history = [0]

    def move(self):
        if self.plan == "RIGHT": self.xpos +=1
        elif self.plan == "LEFT": self.xpos -=1
        elif self.plan == "RANDOM": self.xpos += choice([-1,1])
        self.history.append(self.xpos)
        self.plan = "RANDOM"
 
    def set_plan(self, plan):
        self.plan = plan

class Opera:
    def __init__(self):
        self.cast = dict()
        self.time = 0

    def _pos_dict(self):
        return {persona: self.cast[persona].xpos for persona in self.cast}
    # def _check_collisions(self):
    #     return all([self.cast[a].xpos!=self.cast[b].xpos\
    #                 for a,b in combinations(self.cast.keys(),2)])
    def _get_collisions(self):
        return [a \
            for a,b\
            in product(self.cast.keys(),self.cast.keys()) 
            if a!=b and self.cast[a].xpos==self.cast[b].xpos]
    def _introduce(self,name,xpos=0,plan="RANDOM"):
            assert name not in self.cast, f"{name} PREVIOUSLY INTRODUCED ALREADY"
            self.cast[name] = Thing(name = name, xpos = xpos, plan=plan)
    def vale(self):
        self.time +=1
        for persona in self.cast.values(): persona.move()
        print(f'{self.time:03d}'+make_ascii_line(self._pos_dict()))
        collisions = self._get_collisions()
        if collisions:
            print("   "+16*'CRASH')
            collision_string ='REQUIESCAT ' + ' AND '.join([name[:10] for name in collisions])
            print(f'{collision_string:^80}')
            for name in collisions: self.cast.pop(name)


    def run_act(self,subtree):
        for token in subtree.find_data('introduction'):
            self._introduce(name =  sub(token))
        for token in subtree.find_data('placed_introduction'):
            self._introduce(name = sub(token), xpos = int(sub(token,1)))
        for token in subtree.find_data('motion'):
            assert sub(token) in self.cast, f"AYAYAY {sub(token)} NO MAS"
            self.cast[sub(token)].set_plan(sub(token,1))
        self.vale()

opera = Opera()
print(83*"=")
for num, verse in enumerate(tree.find_data('step')):
    #print(verse)
    opera.run_act(verse)
    #print(f"-------------\nACT{num+1}: DRAMATIS PERSONAE", '\n', opera.cast)