from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def __init__(self):
    self.errors = []

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}; "
        "arithmetic operations require numeric operands"
      )

    return self.numeric_result(left_type, right_type)

  def visitMod(self, ctx: SimpleLangParser.ModContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if not isinstance(left_type, IntType) or not isinstance(right_type, IntType):
      self.errors.append(
        f"Unsupported operand types for %: {left_type} and {right_type}; "
        "modulo requires int and int"
      )

    return IntType()

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}; "
        "arithmetic operations require numeric operands"
      )

    return self.numeric_result(left_type, right_type)

  def visitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))

    if not self.is_valid_equality_operation(left_type, right_type):
      self.errors.append(
        f"Unsupported operand types for ==: {left_type} and {right_type}; "
        "equality requires numeric operands or two operands of the same type"
      )

    return BoolType()
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())

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
