from typing import Any, Callable, Dict, List

from arxir import ast


from arxir.builders.base import Builder, BuilderTranslator, SymbolTable


MAP_TYPE_STR = {
    ast.Int8: "i8",
    ast.Int16: "i16",
    ast.Int32: "i32",
    ast.Int64: "i64",
}

registers: List[int] = []
registers_expr: Dict[int, int] = {}

symtable = SymbolTable()


class LLVMTranslator(BuilderTranslator):
    def translate(self, expr: ast.Expr) -> str:
        """
        Translate the expression using the appropriated function.

        It works as a multi-dispatch visitor approach.
        """
        # structures
        expr_type = type(expr)

        if expr_type is ast.BinaryOp:
            return self.translate_binary_op(expr)
        if expr_type is ast.Block:
            return self.translate_block(expr)
        if expr_type is ast.Function:
            return self.translate_function(expr)
        if expr_type is ast.FunctionPrototype:
            return self.translate_function_prototype(expr)
        if expr_type is ast.Module:
            return self.translate_module(expr)
        if expr_type is ast.Variable:
            return self.translate_variable(expr)
        if expr_type is ast.Return:
            return self.translate_return(expr)

        # datatypes
        if expr_type is ast.Int32:
            return self.translate_i32(expr)

        raise Exception(
            f"No translation was found for the given expression ({expr})."
        )

    def translate_binary_op(self, binop: ast.BinaryOp) -> str:
        lhs = self.translate(binop.lhs)
        rhs = self.translate(binop.rhs)

        lhs_type = MAP_TYPE_STR[binop.lhs.type_]
        rhs_type = MAP_TYPE_STR[binop.rhs.type_]

        op_name = (
            "add"
            if binop.op_code == "+"
            else "sub"
            if binop.op_code == "-"
            else "mul"
            if binop.op_code == "*"
            else "div"
            if binop.op_code == "/"
            else "rem"
            if binop.op_code == "%"
            else ""
        )

        if not op_name:
            raise Exception("The given binary operator is not valid.")

        # TODO: change the operation to `nsw` with if any element of the
        #       operation is a poison value.

        # alias
        reg = registers

        alloca_tpl = "  %{} = alloca {}, align 4\n"
        store_tpl = "  store {} {}, {}* %{}, align 4\n"
        load_tpl = "  ${} = load {}, {}* %{}, align 4\n"
        op_tpl = "  %{} = {} {} %{}, %{}"

        result = ""

        # alloca
        result += alloca_tpl.format(reg[-1], lhs_type)
        reg[-1] += 1
        result += alloca_tpl.format(reg[-1], rhs_type)

        # store
        reg_lhs = registers_expr[id(binop.lhs)]
        reg_rhs = registers_expr[id(binop.rhs)]
        result += store_tpl.format(lhs_type, reg_lhs, lhs_type, reg[-1] - 1)
        result += store_tpl.format(rhs_type, reg_rhs, rhs_type, reg[-1])

        # load
        reg[-1] += 1
        result += load_tpl.format(reg[-1], lhs_type, lhs_type, reg[-1] - 2)
        reg[-1] += 1
        result += load_tpl.format(reg[-1], rhs_type, rhs_type, reg[-1] - 4)

        # operation
        reg[-1] += 1
        result += op_tpl.format(
            reg[-1], op_name, lhs_type, reg[-1] - 1, reg[-1] - 2
        )

        registers_expr[id(binop)] = reg[-1]

        return result

    def translate_module(self, module: ast.Module) -> str:
        scope = symtable.scopes.add(f"module {module.name}")
        symtable.scopes.set_default_parent(scope)

        block_result = self.translate_block(module.block)

        symtable.scopes.set_default_parent(scope.parent)
        symtable.scopes.destroy(scope)

        return (
            f"""; ModuleID = '{module.name}'\n"""
            f"""target datalayout = "{module.target.datalayout}"\n"""
            f"""target triple = "{module.target.triple}"\n"""
        ) + block_result

    def translate_block(self, block: ast.Block) -> str:
        result = ""

        for expr in block:
            result += self.translate(expr) + "\n"
        return result

    def translate_i32(self, i32: ast.Int32) -> str:
        return f"i32 {i32.value}"

    def translate_function_prototype(
        self, prototype: ast.FunctionPrototype
    ) -> str:
        scope = "@" if prototype.scope == ast.ScopeKind.global_ else "%"

        trans_args = []
        for i, arg in enumerate(prototype.args):
            symtable.define(arg)
            trans_args.append(
                f"{MAP_TYPE_STR[arg.type_]} %{registers[-1] + i}"
            )

        args = ", ".join(trans_args)

        # note: `+ 1` is used here because the previous register is used
        # somewhere and the compiler will raise an error.
        registers[-1] = +len(prototype.args) + 1

        return (
            f"define {MAP_TYPE_STR[prototype.return_type]} "
            f"{scope}{prototype.name}("
            f"{args}"
            ")"
        )

    def translate_function(self, fn: ast.Function) -> str:
        scope = symtable.scopes.add(f"function {fn.prototype.name}")
        symtable.scopes.set_default_parent(scope)
        registers.append(0)

        prototype_result = self.translate_function_prototype(fn.prototype)
        body_result = self.translate_block(fn.body)

        registers.pop()
        symtable.scopes.set_default_parent(scope.parent)
        symtable.scopes.destroy(scope)

        return f"""{prototype_result} {{\n""" f"""{body_result}\n""" f"}}"

    def translate_return(self, ret: ast.Return) -> str:
        ret_tpl = "  ret {} %{}"

        reg_n = registers_expr[id(ret.value)]
        reg_tp = MAP_TYPE_STR[ret.value.type_]
        return ret_tpl.format(reg_tp, reg_n)

    def translate_variable(self, var: ast.Variable) -> str:
        return "variable"


class LLVMIR(Builder):
    def __init__(self):
        self.translator: BuilderTranslator = LLVMTranslator()
