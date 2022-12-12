from src.lexer import Lexer
from src.reader import read
from src.executor import Executor
from src.funcHandler import fh


lines = read()
l = Lexer()
ex = Executor()
fh.loadPy("libs.std")


for i, line in enumerate(lines):
  i += 1
  l.lex(line, i)
  #print(l.toks)
  ex.execute(l.toks, "globe", i, )
  