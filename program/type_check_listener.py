from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}; "
        "arithmetic operations require numeric operands"
      )
    self.types[ctx] = self.numeric_result(left_type, right_type)

  def exitMod(self, ctx: SimpleLangParser.ModContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
      self.errors.append(
        f"Unsupported operand types for %: {left_type} and {right_type}; "
        "modulo requires int and int"
      )
    self.types[ctx] = IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}; "
        "arithmetic operations require numeric operands"
      )
    self.types[ctx] = self.numeric_result(left_type, right_type)

  def exitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_equality_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for ==: {left_type} and {right_type}; "
        "equality requires numeric operands or two operands of the same type"
      )
    self.types[ctx] = BoolType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    return (
      isinstance(left_type, (IntType, FloatType))
      and isinstance(right_type, (IntType, FloatType))
    )

  def is_valid_equality_operation(self, left_type, right_type):
    if self.is_valid_arithmetic_operation(left_type, right_type):
      return True
    return type(left_type) is type(right_type)

  def numeric_result(self, left_type, right_type):
    if isinstance(left_type, FloatType) or isinstance(right_type, FloatType):
      return FloatType()
    return IntType()
