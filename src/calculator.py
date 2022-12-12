from src.token import Token
from src.errors import panic


class Calculator():
  def __init__(self):
    self.ops = [["pow"], ["mul", "div"], ["add", "sub"]]


  def cal(self, lf, r, op, line):
    for p in [lf, r]:
      if Token(str(p), line).type not in ["int", "float"]:
        panic(f"Non-number operation on line {line}")
    if op == "div" and r == 0:
      panic(f"Division by zero on line {str(line)}")
    r = {
      "add": lf+r
    }
    if op in r:
      return r[op]


  def calc(self, br, line):
    # br = [Token(b) if type(b) != Token else b for b in br]
    l = br
    x, y = True, True
    res = None
    while x:
      y = True
      for toks in self.ops:
        if not y:
          continue
        x = False
        for i, t in enumerate(l):
          if t.type in toks:
            lf, r = l[i-1].val.value, l[i+1].val.value
            i = i
            if t.type == "add":
              for _ in range(2):
                l.pop(i-1)
              r = self.cal(lf, r, t.type, line) 
              l[i-1] = Token(str(r), line)
            x = True
    res = l[0]
    return [res]
    
