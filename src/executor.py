from src.errors import panic
from src.varhandler import vh

class Executor():
  def __init__(self):
    self.line = []
    self.context = ""
    self.varhandler = vh


  def checkAssign(self, tok):
    if tok.type in ["var", "undefined"]:
          self.assignVars.append(tok)
    elif tok.type == "equator":
      self.doneAssign = True
      return True
    else:
      if len(self.assignVars):
        panic(f"Missing operator '=' at line {self.lN}")
      self.doneAssign = True


  def getAssigners(self):
    for i, tok in enumerate(self.line):
      if not self.doneAssign:
        hasEq = self.checkAssign(tok)
      if hasEq:
        self.line = self.line[i+1:]
        return


  def checkForUnassigned(self):
    for tok in self.line:
      if tok.type == "undefined":
        panic(f"Undefined token {tok} in line {self.lN}")


  def getArgs(self, b):
    args = []
    tmp = []
    for tok in b:
      if tok.type == "separator":
        args.append(tmp)
        continue
      tmp.append(tok)
    args.append(tmp)
    return args


  def getFirstFunc(self):
    # index of open and closing brackets
    iO, iC = None, None
    for indx, tok in enumerate(self.line):
      if tok.type == "openbracket":
        iO = indx
      elif tok.type == "closingbracket":
        iC = indx
        if iO == None:
          panic(f"Closing bracket without opening found at line {self.lN}!")
        if iO == 0:
          return
        br = self.line[iO+1:iC]
        if self.line[iO-1].type == "func":
          fn = self.line[iO-1].val
          args = self.getArgs(br)
          fn.run(args, self.lN)
        
      

  
  def assignVarsF(self):
    self.line = [tok for tok in self.line if tok.type != "equator"]

    # Checks if nothing is assigned...
    if not len(self.assignVars):
      return
    
    if len(self.line) == len(self.assignVars):
      for i in range(len(self.line)):
        vh.addToScope(self.assignVars[i].val, self.line[i].val, "global", self.lN)
        
    else:
      panic(f"Unequal amounts of variables assigned to values at line {self.lN}", line=self.lN)

  

  def init(self, lN, line, context):
    self.lN = lN
    self.line = line
    self.context = context

    self.doneAssign = False
    self.assignVars = []

  

  def execute(self, line, context, lN):
    # Sets initial variables
    self.init(lN, line, context)
    # Gets vars to assign end result to
    self.getAssigners()
    # Checks for unassigned
    self.checkForUnassigned()
    # Exeuctes...
    self.getFirstFunc()
    pass
    # Assign vars
    self.assignVarsF()
