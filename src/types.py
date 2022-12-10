from src.errors import panic


class Base():
  def __init__(self):
    self.value = None   # Set this to default (eg: 0, "")
    self.isVar = False
    self.isFunc = False
    self.type = None   # Set this to type (eg: int, string)


  def set(self, val):
    t = type(val)
    
    if type(self.value) == t:
      self.value = val
      
      if self.type == "bool":
        if val:
          self.value = True
        else:
          self.value = False
      
      return self

      
    return globals()[t.__name__]().set(val)


  def __str__(self):
    if self.isVar:
      return str(self.varName)
    return str(self.value)




class int(Base):
  def __init__(self, val=None):
    super().__init__()
    self.value = 0
    if val:
      self.set(val)




class float(Base):
  def __init__(self, val=None):
    super().__init__()
    self.value = 0.0
    if val:
      self.set(val)


class bool(Base):
  def __init__(self, val=None):
    super().__init__()
    self.value = True
    if val:
      self.set(val)




class Str(Base):
  def __init__(self, val=None):
    super().__init__()
    self.value = ""
    if val:
      self.set(val)
    self.type = "str"



class Var(Base):
  def __init__(self, val, varName):
    super().__init__()
    self.isVar = True
    while val.isVar:
      val = val.value
    self.value = val
    self.type = "var"
    self.valType = val.type
    self.varName = varName



class Func(Base):
  def __init__(self, name, argsLen=None, lines=None):
    super().__init__()
    self.isFunc = True
    self.argsLen = argsLen
    self.value = name
    self.type = "func"
    self.lines = None
    self.pyFunc = None

  def checkArgs(self, args, line):
    if len(args) != self.argsLen:
      panic(f"Function '{self.value}' given {str(len(args))} arguments on line {str(line)} when {str(self.argsLen)} can be given")


  # This will later be used to add etc in the args
  def makeArgs(self, args):
    newA = []
    for arg in args:
      if arg:
        newA.append(arg[0].val)
    return newA


  def run(self, args, line):
    self.checkArgs(args, line)
    args = self.makeArgs(args)
    if self.pyFunc:
      self.pyFunc(*args)