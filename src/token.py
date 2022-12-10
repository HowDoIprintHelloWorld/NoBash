from data.keys import numbersAndDot, types

from src.errors import panic
from src.funcHandler import fh
from src.varhandler import vh
import src.types as ty


class Token():
  def __init__(self, val, line):
    self.val = val
    self.detect(line)


  def __str__(self):
    return str(self.val)

  
  def __repr__(self):
    return f"{str(self.val)} ({str(self.type)})"

  
  def detect(self, line=None):
    tok = self.val

    # Float or Int
    if not any(l for l in tok if l not in numbersAndDot):
      dotCount = tok.count(".") 
      if dotCount == 0:
        self.val = ty.int(int(self.val))
        self.type =  "int"
      elif dotCount == 1:
        if tok.startswith(".") or tok.endswith("."):
          panic("Invalid position of '.' in "+tok, line=line)
        self.val = ty.float(float(self.val))
        self.type =  "float"
      else:
        panic(f"Too many '.' in {tok}", line=line)

    
    elif tok in vh.globals.keys():
      self.type = "var"
      self.val = vh.globals[tok]


    elif tok in fh.funcs.keys():
      self.type = "func"
      self.val = fh.funcs[tok]
        

    # String
    elif tok.startswith('"') and tok.endswith('"'):
      self.val = ty.Str(self.val[1:-1])
      self.type = "string"

    # String
    elif tok in types.keys():
      self.type = types[tok]
      if self.type == "bool":
        self.val = bool(self.val)
        self.val = ty.bool(self.val)


    # If none of the others, undefined 
    # For example in function declarations
    else: 
      self.type = "undefined"