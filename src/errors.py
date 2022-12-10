from sys import exit


def panic(errLine, line=None):
  err = "Exiting (1): Error found"
  if line:
    err += f" at line {str(line)}"
  err += ":\n"
  err += errLine
  print(err)
  exit(1)