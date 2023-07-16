from typing import Any, Callable, Dict, List

from arxir import ast


from arxir.builders.base import Builder, BuilderTranslator


class LLVMTranslator(BuilderTranslator):
    def translate(self, expr: ast.Expr) -> str:
        """
        Translate the expression using the appropriated function.

        It works as a multi-dispatch visitor approach.
        """
        # structures
        if type(expr) is ast.BinaryOp:
            return self.translate_binary_op(expr)
        if type(expr) is ast.Block:
            return self.translate_block(expr)
        if type(expr) is ast.Function:
            return self.translate_function(expr)
        if type(expr) is ast.FunctionPrototype:
            return self.translate_function_prototype(expr)
        if type(expr) is ast.Module:
            return self.translate_module(expr)
        if type(expr) is ast.Variable:
            return self.translate_variable(expr)

        # datatypes
        if type(expr) is ast.Int32:
            return self.translate_i32(expr)

        raise Exception(
            f"No translation was found for the given expression ({expr})."
        )

    def translate_binary_op(self, binop: ast.BinaryOp) -> str:
        lhs = self.translate(binop.lhs)
        rhs = self.translate(binop.rhs)

        f_name = (
            "add" if binop.op_code == "+" else
            "sub" if binop.op_code == "-" else
            "mul" if binop.op_code == "*" else
            "div" if binop.op_code == "/" else
            "rem" if binop.op_code == "%" else
            ""
        )

        if not f_name:
            raise Exception("The given binary operator is not valid.")

        return (
            # just an example
            """
            %1 = alloca i32, align 4
            %2 = alloca i32, align 4
            %3 = alloca i32, align 4
            store i32 0, i32* %1, align 4
            store i32 5, i32* %2, align 4
            store i32 3, i32* %3, align 4
            %4 = load i32, i32* %2, align 4
            %5 = load i32, i32* %3, align 4
            %6 = add nsw i32 %4, %5
            ret i32 %6
            """
        )

    def translate_module(self, module: ast.Module) -> str:
        block_result = self.translate_block(module.block)

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
        scope = '@' if prototype.scope == ast.ScopeKind.global_ else "%"
        args = ", ".join(
            f"{arg.type_} %{arg.name}" for arg in prototype.args
        )
        return (
            f"define {prototype.return_type} "
            f"{scope}{prototype.name}("
            f"{args}"
            ")"
        )

    def translate_function(self, fn: ast.Function) -> str:
        prototype_result = self.translate_function_prototype(fn.prototype)
        body_result = self.translate_block(fn.body)
        return (
            f"""{prototype_result} {{\n"""
            f"""{body_result}\n"""
            f"}}"
        )

    def translate_variable(self, var: ast.Variable) -> str:
        return "variable"
