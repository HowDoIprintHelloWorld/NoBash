from src.errors import panic
from src.types import Var


class VH():
  def __init__(self):
    self.globals = {}
    # For now, there are no scopes :)

    
    # self.globalfunc = {}
    


  def addToScope(self, var, val, scope, line):
    if scope == "global":
      newV = Var(val, var)
      if var in self.globals:
        if val.type != self.globals[var].varType:
          panic(f"Variable {var} already assigned to type {self.globals[var].varType}, can't assign to {val.type}")
      self.globals[var] = newV




vh = VH()