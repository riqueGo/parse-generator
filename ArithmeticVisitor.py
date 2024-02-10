from antlr4 import *
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor ():
    def __init__(self):
        self.vars = {}

    def visit(self, ctx):
        if isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)
        elif isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)

    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            if ctx.getChild(i * 2 - 1).getText() == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            if ctx.getChild(i * 2 - 1).getText() == '*':
                result *= self.visit(ctx.factor(i))
            else:
                result /= self.visit(ctx.factor(i))
        return result

    def visitFactor(self, ctx):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            value = self.vars.get(ctx.VAR().getText())
            if not value:
               raise VariableNotDeclaredException(ctx.VAR().getText())
            return value
        else:
            return self.visit(ctx.expr())
    
    def visitProgram(self, ctx):
        result = None
        for statement in ctx.statement():
            result = self.visit(statement)
        return result
    
    def visitStatement(self, ctx):
        if ctx.expr():
            return self.visit(ctx.expr())
        else:
            return self.visit(ctx.assignment())
    
    def visitAssignment(self, ctx):
        self.vars[ctx.VAR().getText()] = self.visitExpr(ctx.expr())

    
class VariableNotDeclaredException(Exception):
    def __init__(self, var):
        self.message = "Variable '{0}' not declared".format(var)
        super().__init__(self.message)
