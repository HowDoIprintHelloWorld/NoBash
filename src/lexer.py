from src.token import Token
from src.errors import panic

from data.keys import numbersAndDot, numbers


class Lexer():
  def __init__(self):
    self.inpt = ""
    self.toks = []

    self.splitters = ["=", "(", ")"]


  def addTok(self, tok):
    if tok:
      self.toks.append(tok)


  def lex(self, inpt, line):
    self.inpt = inpt
    self.toks = []
    strMode = False
    tok = ""

    self.inpt = self.inpt.replace("==", "iseq")
    self.inpt = self.inpt.replace(">=", "isgr")
    self.inpt = self.inpt.replace("<=", "issm")

    
    for l in self.inpt:
      if l == '"':
        strMode = not strMode

      
      if not strMode:  
        if l == "#":
          self.addTok(tok)
          self.toks = [Token(tok, line) for tok in self.toks]
          return self.toks
          
        
        elif l == " ":
          self.addTok(tok)
          tok = ""
          continue 

        
        elif l in self.splitters:
          self.addTok(tok)
          self.addTok(l)
          tok = ""
          continue

      
      tok += l
    self.addTok(tok)

    self.toks = [Token(tok, line) for tok in self.toks]
    return self.toks
      