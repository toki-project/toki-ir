from typing import Any, Callable, Dict, List

from arxir.expr.base import Expr
from arxir.expr import structures as st
from arxir.expr import datatypes as dts
from arxir.expr.modifiers import ScopeKind

from arxir.builders.base import Builder, BuilderTranslator


class LLVMTranslator(BuilderTranslator):
    def translate(self, expr: Expr) -> str:
        """
        Translate the expression using the appropriated function.

        It works as a multi-dispatch visitor approach.
        """
        # structures
        if type(expr) is st.Block:
            return self.translate_block(expr)
        if type(expr) is st.Function:
            return self.translate_function(expr)
        if type(expr) is st.FunctionPrototype:
            return self.translate_function_prototype(expr)
        if type(expr) is st.Module:
            return self.translate_module(expr)

        # datatypes
        if type(expr) is dts.Int32:
            return self.translate_i32(expr)

        raise Exception("No translation was found for the given expression.")

    def translate_module(self, module: st.Module) -> str:
        block_result = self.translate_block(module.block)

        return (
            f"""; ModuleID = '{module.name}'\n"""
            f"""target datalayout = "{module.target.datalayout}"\n"""
            f"""target triple = "{module.target.triple}"\n"""
        ) + block_result

    def translate_block(self, block: st.Block) -> str:
        result = ""

        for expr in block:
            result += self.translate(expr) + "\n"
        return result

    def translate_i32(self, i32: dts.Int32) -> str:
        return f"i32 {i32.value}"

    def translate_function_prototype(
        self, prototype: st.FunctionPrototype
    ) -> str:
        scope = '@' if prototype.scope == ScopeKind.global_ else "%"
        args = ", ".join(
            f"{arg.typ.name} %{arg.name}" for arg in prototype.args
        )
        return (
            f"define {prototype.return_type.name} "
            f"{scope}{prototype.name}("
            f"{args}"
            ")"
        )

    def translate_function(self, fn: st.Function) -> str:
        prototype_result = self.translate_function_prototype(fn.prototype)
        body_result = self.translate_block(fn.body)
        return (
            f"""{prototype_result} {{\n"""
            f"""{body_result}\n"""
            f"}}"
        )
