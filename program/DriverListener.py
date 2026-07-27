import sys
from antlr4 import *
from SimpleLangLexer import SimpleLangLexer
from SimpleLangParser import SimpleLangParser
from type_check_listener import TypeCheckListener
from antlr4.tree.Tree import ParseTreeWalker

def main(argv):
  if len(argv) != 2:
    print(f"Usage: python3 {argv[0]} <input_file>")
    return 1

  input_stream = FileStream(argv[1])
  lexer = SimpleLangLexer(input_stream)
  stream = CommonTokenStream(lexer)
  parser = SimpleLangParser(stream)
  tree = parser.prog()

  if parser.getNumberOfSyntaxErrors() > 0:
    print("Syntax checking failed")
    return 1

  walker = ParseTreeWalker()
  listener = TypeCheckListener()
  walker.walk(listener, tree)

  if listener.errors:
    for error in listener.errors:
      print(f"Type checking error: {error}")
    return 1
  else:
    print("Type checking passed")
    return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
