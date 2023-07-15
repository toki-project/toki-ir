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
        if type(expr) is ast.Block:
            return self.translate_block(expr)
        if type(expr) is ast.Function:
            return self.translate_function(expr)
        if type(expr) is ast.FunctionPrototype:
            return self.translate_function_prototype(expr)
        if type(expr) is ast.Module:
            return self.translate_module(expr)

        # datatypes
        if type(expr) is ast.Int32:
            return self.translate_i32(expr)

        raise Exception("No translation was found for the given expression.")

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
            f"{arg.type_.name} %{arg.name}" for arg in prototype.args
        )
        return (
            f"define {prototype.return_type.name} "
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
