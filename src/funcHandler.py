from src.types import Func
from inspect import signature
import importlib

class FH():
  def __init__(self):
    # funcname, func obj
    self.funcs = {}


  def loadPy(self, file):
    f = importlib.import_module(file)
    funcs = [func for func in dir(f) if not func.startswith("__")]
    for func in funcs:
      fn = getattr(f, func)
      arglen = len(signature(fn).parameters)
      self.funcs[func] = Func(func, arglen)
      self.funcs[func].pyFunc = fn


fh = FH()