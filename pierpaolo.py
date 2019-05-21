from lark import Lark 
import sys
from itertools import product, combinations
from dataclasses import dataclass
from enum import Enum
from random import randint
# grammar
with open("pierpaolo.lark") as handle: grammar = ''.join(handle.readlines())
parser = Lark(grammar)

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
@dataclass
class Persona:
    name: str
    plan : Plan
    xpos: float


class Opera:
    def __init__(self):
        self.characters = dict()
        self.history = dict() # dict of lists
        self.time = 0
    def _set_persona(self,persona):
        self.characters[persona.name] = persona
        self.history[(persona.name,self.time)] = persona 
    def _check_name(self, name):
        if name not in self.characters:
            raise ValueError(f'{name} NOT INTRODUCED')
        else:
            return True
    def _update_persona(self,persona):
        if self._check_name(persona.name):
            self._set_persona(Persona(
                        name = persona.name, 
                        xpos = persona.xpos, 
                        plan = persona.plan))
    def _pos_dict(self):
        return {persona: self.characters[persona].xpos for persona in self.characters}
    def _check_collisions(self):
        return all([self.characters[a].xpos!=self.characters[b].xpos\
                    for a,b in combinations(self.characters.keys(),2)])
    def execute_introduce(self,name):
        self._set_persona(Persona(
                        name = name, 
                        xpos = 0, 
                        plan = 'RANDOM'))
    def prepare_move(self,name, plan):
        persona = self.characters[name]
        self.characters[name] = Persona(
                        name = name, 
                        xpos = persona.xpos, 
                        plan = plan)
    def execute_move(self,persona):
        plan = persona.plan; xpos = persona.xpos
        if plan == "RIGHT": xpos +=1
        elif plan == "LEFT": xpos -=1
        elif plan == "RANDOM": xpos += randint(-1,1)
        self._update_persona(Persona(
                        name =persona.name, 
                        xpos = xpos,
                        plan = "RANDOM"))
    def vale(self):
        self.time +=1
        for name in self.characters:
            self.execute_move(self.characters[name]) 
        if not self._check_collisions():
            print(16*'CRASH')
        print(f'{self.time:03d}'+make_ascii_line(self._pos_dict()))

    def run_act(self,subtree):
        for token in subtree.find_data('introduction'):
            self.execute_introduce(token.children[0].value)
        for token in subtree.find_data('motion'):
            self.prepare_move(name=token.children[0].value, plan=token.children[1].value)
        self.vale()

opera = Opera()
print(83*"=")
for num, verse in enumerate(tree.find_data('step')):
    #print(verse)
    opera.run_act(verse)
    #print(f"-------------\nACT{num+1}: DRAMATIS PERSONAE", '\n', opera.characters)