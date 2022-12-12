from src.errors import panic
from src.varhandler import vh
from src.token import Token
from src.calculator import Calculator

class Executor():
  def __init__(self):
    self.ranIf = False 
    self.calculator = Calculator()
    self.line = []
    self.context = ""
    self.varhandler = vh
    self.conditions = [] # When open bracket encountered, check the last here!


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


  def funcFromBr(self, br, prev, iO, iC):
    fn = prev.val
    args = self.getArgs(br)
    res = fn.run(args, self.lN)

    return res
      


  def getFirstBrackets(self):
    # index of open and closing brackets
    iO, iC = None, None
    for indx, tok in enumerate(self.line):
      if tok.type == "openbracket":
        iO = indx
      elif tok.type == "closingbracket":
        iC = indx
        if iO == None:
          panic(f"Closing bracket without opening found at line {self.lN}!")
        res = None
        br = self.line[iO+1:iC]
        prev, x = None, False
        if iO != 0:
          prev = self.line[iO-1]
        if prev:
          if prev.type == "func":
            res = self.funcFromBr(br, prev, iO, iC)
            x = True
        if x:
          res = self.calculator.calc(br, self.lN)

        newL = []
        if iO != 0:
          newL = self.line[:iO-1]
        if res:
          newL += [Token(str(r), self.lN) for r in res]
        newL += self.line[iC+1:]
        print(newL)
        self.line = newL
      
        


  def checkForBrackets(self):
    toks = [tok.type for tok in self.line]
    if "openbracket" in toks and "closingbracket" in toks:
      return True
    return False
      

  
  def assignVarsF(self):
    self.line = [tok for tok in self.line if tok.type != "equator"]

    # Checks if nothing is assigned...
    if not len(self.assignVars):
      return
    
    if len(self.line) == len(self.assignVars):
      for i in range(len(self.line)):
        vh.addToScope(self.assignVars[i].val, self.line[i].val, "global", self.lN)
        
    else:
      print(f"{str(self.line)=}; {str(self.assignVars)=}")
      panic(f"Unequal amounts of variables assigned to values at line {self.lN}", line=self.lN)


  def formatCond(self, cond):
    lastOp = 0
    nCond = []
    for i, tok in enumerate(cond):
      if tok.type == "orop" or tok.type == "andop":
        nCond.append(cond[lastOp:i])
        nCond.append([cond[i]])
        lastOp = i+1
    nCond.append(cond[lastOp:])
    return nCond



  def evalC(self, c):
    for i, tok in enumerate(c):
      # should calculate, but dont have that now
      if tok.type == "iseq":
        l,r = c[:i], c[i+1:]
        return l[0].val.value == r[0].val.value
      elif tok.type == "isgr":
        l,r = c[:i], c[i+1:]
        return l[0].val.value >= r[0].val.value
      elif tok.type == "issm":
        l,r = c[:i], c[i+1:]
        return l[0].val.value <= r[0].val.value
    panic(f"No comparison made on line {str(self.lN)}")


  
  def evalCond(self, cond):
    # first step: seperate ands and ors
    cond = self.formatCond(cond)
    # For now, just work with one cond.. (so no ands etc)
    for c in cond:
      res = self.evalC(c)
    return res
  


  def checkIf(self, l=None):
    if l == None:
      l = self.line
    if len(l) >= 2:
      if l[-1].type == "opencurly":
        cond = l[1:-1]
        if l[0].type == "ifcond":
          e = self.evalCond(cond)
          self.conditions.append({"cond":cond, "evaluation":e})
          if e:
            self.ranIf = True
        else:
          e = False
          if l[0].type == "elsecond" and not self.ranIf:
            e = True
          elif l[0].type == "elseifcond" and not self.ranIf:
            e = self.evalCond(cond)
          elif self.ranIf:            
            self.conditions[-1] = {"cond":"else", "evaluation":False}
            return
          else:
            panic(f"Invalid token {str(l[0].val)} at line {str(self.lN)}")
          if e and not self.ranIf:
            self.ranIf = True
            if not self.shouldRun():
              self.conditions[-1] = {"cond":"else", "evaluation":True}
            elif self.conditions:
              self.conditions[-1] = {"cond":"else", "evaluation":False}
  
    

  def checkCondEnd(self):
    if not self.line:
      return
    if self.line[0].type == "closingcurly":  
      if self.line[-1].type == "opencurly":
        self.checkIf(l=self.line[1:])
      elif len(self.line) == 1:
          self.ranIf = False
          self.removeCond()
      return True


  def removeCond(self):
    if self.conditions:
      self.conditions.pop(-1)


  def shouldRun(self):
    if not self.conditions:
      return True
    return self.conditions[-1]["evaluation"]

  

  def init(self, lN, line, context):
    self.lN = lN
    self.line = line
    self.context = context

    self.doneAssign = False
    self.assignVars = []


  def setVars(self):
    newLine = []
    for tok in self.line:
      if tok.type == "var":
        tok = Token(str(tok.val.value), self.lN)
      newLine.append(tok)
    self.line = newLine

  

  def execute(self, line, context, lN):
    self.condFound = False
    
    # Sets initial variables
    self.init(lN, line, context)
    # Check for condition end
    r = self.checkCondEnd()
    if r:
      return
    # Checks if should run
    if not self.shouldRun():
      return
    # Gets vars to assign end result to
    self.getAssigners()
    # Checks for unassigned
    self.checkForUnassigned()
    # Sets the vars to their values
    self.setVars()
    # Exeuctes funcs
    while self.checkForBrackets():
      self.getFirstBrackets()
    # checks for if's
    if not self.condFound:
      self.checkIf()
    # Assign vars
    self.assignVarsF()
