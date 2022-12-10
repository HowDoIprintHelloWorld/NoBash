from sys import argv


def read():  
  testing = True
  
  if testing:
    file = "test.ns"
  else:
    file = argv[1]
    
  with open(file, "r") as f:
    lR = []
    for l in f.readlines() :
      if l.endswith("\n"):
        l = l[:-1]
      lR.append(l)
    return lR