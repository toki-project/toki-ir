import tempfile

from typing import Any, Dict, List, cast

import sh

from arxir import ast
from arxir.builders.base import Builder, BuilderTranslator
from arxir.builders.symbol_table import SymbolTable


MAP_TYPE_STR: Dict[ast.ExprType, str] = {
    ast.Int8: "i8",
    ast.Int16: "i16",
    ast.Int32: "i32",
    ast.Int64: "i64",
}

registers: List[int] = []
registers_expr: Dict[str, int] = {}

symtable = SymbolTable()


def strid(obj: Any) -> str:
    return str(id(obj))


class LLVMTranslator(BuilderTranslator):
    def translate(self, expr: ast.AST) -> str:
        """
        Translate the expression using the appropriated function.

        It works as a multi-dispatch visitor approach.
        """
        # structures
        expr_type = type(expr)

        if expr_type is ast.BinaryOp:
            return self.translate_binary_op(cast(ast.BinaryOp, expr))
        if expr_type is ast.Block:
            return self.translate_block(cast(ast.Block, expr))
        if expr_type is ast.Function:
            return self.translate_function(cast(ast.Function, expr))
        if expr_type is ast.FunctionPrototype:
            return self.translate_function_prototype(
                cast(ast.FunctionPrototype, expr)
            )
        if expr_type is ast.Module:
            return self.translate_module(cast(ast.Module, expr))
        if expr_type is ast.Variable:
            return self.translate_variable(cast(ast.Variable, expr))
        if expr_type is ast.Return:
            return self.translate_return(cast(ast.Return, expr))

        # datatypes
        if expr_type is ast.Int32Literal:
            return self.translate_i32_literal(cast(ast.Int32Literal, expr))

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
        store_tpl = "  store {} %{}, {}* %{}, align 4\n"
        load_tpl = "  %{} = load {}, {}* %{}, align 4\n"
        op_tpl = "  %{} = {} nsw {} %{}, %{}"

        result = ""

        # alloca
        result += alloca_tpl.format(reg[-1], lhs_type)
        reg[-1] += 1
        result += alloca_tpl.format(reg[-1], rhs_type)

        # store
        reg_lhs = binop.lhs.comment
        reg_rhs = binop.rhs.comment
        result += store_tpl.format(lhs_type, reg_lhs, lhs_type, reg[-1] - 1)
        result += store_tpl.format(rhs_type, reg_rhs, rhs_type, reg[-1])

        # load
        reg[-1] += 1
        result += load_tpl.format(reg[-1], lhs_type, lhs_type, reg[-1] - 2)
        reg[-1] += 1
        result += load_tpl.format(reg[-1], rhs_type, rhs_type, reg[-1] - 2)

        # operation
        reg[-1] += 1
        result += op_tpl.format(
            reg[-1], op_name, lhs_type, reg[-1] - 2, reg[-1] - 1
        )

        binop.comment = str(reg[-1])
        symtable.define(binop)

        return result

    def translate_block(self, block: ast.Block) -> str:
        result = ""

        for expr in block:
            result += self.translate(expr) + "\n"
        return result

    def translate_module(self, module: ast.Module) -> str:
        scope = symtable.scopes.add(f"module {module.name}")
        symtable.scopes.set_default_parent(scope)

        block_result = self.translate_block(module.block)

        symtable.scopes.set_default_parent(scope.parent)
        symtable.scopes.destroy(scope)

        return (
            f"""; ModuleID = '{module.name}.arx'\n"""
            f"""source_filename = "{module.name}.arx"\n"""
            f"""target datalayout = "{module.target.datalayout}"\n"""
            f"""target triple = "{module.target.triple}"\n\n"""
        ) + block_result

    def translate_i32_literal(self, i32: ast.Int32Literal) -> str:
        registers[-1] += 1
        reg_n = registers[-1]

        result = (
            "  %{0} = alloca i32, align 4\n"
            "  store i32 0, i32* %{0}, align 4\n"
            "  %{1} = load i32, i32* %{0}, align 4\n"
        ).format(reg_n, reg_n + 1)
        registers[-1] += 1

        i32.comment = str(reg_n + 1)

        return result

    def translate_function_prototype(
        self, prototype: ast.FunctionPrototype
    ) -> str:
        scope = "@" if prototype.scope == ast.ScopeKind.global_ else "%"

        trans_args = []
        for i, arg in enumerate(prototype.args):
            symtable.define(arg)
            arg.comment = str(registers[-1] + i)
            trans_args.append(
                f"{MAP_TYPE_STR[arg.type_]} noundef %{arg.comment}"
            )

        args = ", ".join(trans_args)

        # note: `+ 1` is used here because the previous register is used
        # somewhere and the compiler will raise an error.
        if prototype.args:
            registers[-1] = len(prototype.args) + 1
        else:
            # note: this is an workaround
            registers[-1] = 0

        return (
            f"define dso_local {MAP_TYPE_STR[prototype.return_type]} "
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

        ret_value = self.translate(ret.value)

        reg_n = ret.value.comment

        reg_tp = MAP_TYPE_STR[ret.value.type_]
        return f"{ret_value}\n{ret_tpl.format(reg_tp, reg_n)}"

    def translate_variable(self, var: ast.Variable) -> str:
        return f"variable {var.name}"


class LLVMIR(Builder):
    def __init__(self):
        super().__init__()
        self.translator: BuilderTranslator = LLVMTranslator()

    def build(self, expr: ast.AST, output_file: str) -> None:
        result = self.compile(expr)

        with tempfile.NamedTemporaryFile(suffix="", delete=False) as temp_file:
            self.tmp_path = temp_file.name

        file_path_ll = f"{self.tmp_path}.ll"
        file_path_o = f"{self.tmp_path}.o"

        with open(file_path_ll, "w") as f:
            f.write(result)

        sh.llc(
            [
                "-filetype=obj",
                file_path_ll,
                "-o",
                file_path_o,
            ],
            **self.sh_args,
        )
        self.output_file = output_file
        sh.clang([file_path_o, "-o", self.output_file], **self.sh_args)

    def run(self) -> None:
        sh([self.output_file])
