from arxir.expr.base import Expr



class IfStmt(Expr):
    if_cond: Expr
    if_then: Expr
    if_else: Expr
