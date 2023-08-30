"""LLVM-IR builder."""
import tempfile

from typing import Dict, cast

import sh

from arxir import ast
from arxir.builders.base import Builder, BuilderTranslator
from arxir.builders.symbol_table import RegisterTable, SymbolTable

MAP_TYPE_STR: Dict[ast.ExprType, str] = {
    ast.Int8: "i8",
    ast.Int16: "i16",
    ast.Int32: "i32",
    ast.Int64: "i64",
}


class LLVMTranslator(BuilderTranslator):
    """LLVM-IR Translator."""

    regtable: RegisterTable
    symtable: SymbolTable
    n_branches: int

    def __init__(self) -> None:
        """Initialize LLVMTranslator object."""
        super().__init__()
        self.regtable = RegisterTable()
        self.symtable = SymbolTable()
        self.n_branches = 0

    def reset(self) -> None:
        """Reset the LLVMTranslator state."""
        self.regtable = RegisterTable()
        self.symtable = SymbolTable()
        self.n_branches = 0

    def translate(self, expr: ast.AST) -> str:  # noqa: PLR0911
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

        # control-flows
        if expr_type is ast.ForCountLoop:
            return self.translate_for_count_loop(cast(ast.ForCountLoop, expr))
        if expr_type is ast.ForRangeLoop:
            return self.translate_for_range_loop(cast(ast.ForRangeLoop, expr))

        raise Exception(
            f"No translation was found for the given expression ({expr})."
        )

    def translate_binary_op(self, binop: ast.BinaryOp) -> str:
        """Translate ASTx Binary Operation to LLVM-IR."""
        # note: need to check if it is needed to be handle in some way
        self.translate(binop.lhs)
        self.translate(binop.rhs)

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
            else "lt"
            if binop.op_code == "<"
            else "le"
            if binop.op_code == "<="
            else "gt"
            if binop.op_code == ">"
            else "ge"
            if binop.op_code == ">="
            else "eq"
            if binop.op_code == "=="
            else "ne"
            if binop.op_code == "!="
            else ""
        )

        if not op_name:
            raise Exception("The given binary operator is not valid.")

        reg = self.regtable

        alloca_tpl = "  %{} = alloca {}, align 4\n"
        store_tpl = "  store {} %{}, {}* %{}, align 4\n"
        load_tpl = "  %{} = load {}, {}* %{}, align 4\n"
        op_tpl = "  %{} = {} nsw {} %{}, %{}"

        result = ""

        # alloca
        result += alloca_tpl.format(reg.last, lhs_type)
        reg.increase()
        result += alloca_tpl.format(reg.last, rhs_type)

        # store
        reg_lhs = binop.lhs.comment
        reg_rhs = binop.rhs.comment
        result += store_tpl.format(lhs_type, reg_lhs, lhs_type, reg.last - 1)
        result += store_tpl.format(rhs_type, reg_rhs, rhs_type, reg.last)

        # load
        reg.increase()
        result += load_tpl.format(reg.last, lhs_type, lhs_type, reg.last - 2)
        reg.increase()
        result += load_tpl.format(reg.last, rhs_type, rhs_type, reg.last - 2)

        # operation
        reg.increase()
        result += op_tpl.format(
            reg.last, op_name, lhs_type, reg.last - 2, reg.last - 1
        )

        binop.comment = str(reg.last)
        self.symtable.define(binop)

        return result

    def translate_block(self, block: ast.Block) -> str:
        """Translate ASTx Block to LLVM-IR."""
        result = ""

        for expr in block:
            result += self.translate(expr) + "\n"
        return result

    def translate_integer_comparison(self, op_code) -> str:
        """
        Return the comparison instruction.

        Comparison operators for signed integers:

        * slt: Signed less than
        * sle: Signed less than or equal to
        * seq: Signed equal to
        * sne: Signed not equal to
        * sgt: Signed greater than
        * sge: Signed greater than or equal to

        Comparison operators for unsigned integers:

        * ult: Unsigned less than
        * ule: Unsigned less than or equal to
        * ueq: Unsigned equal to
        * une: Unsigned not equal to
        * ugt: Unsigned greater than
        * uge: Unsigned greater than or equal to
        """
        comp = "icmp s" + (
            "slt"
            if op_code == "<"
            else "sle"
            if op_code == "<="
            else "seq"
            if op_code == "=="
            else "sne"
            if op_code == "!="
            else "sgt"
            if op_code == ">"
            else "sge"
            if op_code == ">="
            else ""
        )
        if comp == "icmp s":
            raise Exception("Operator not recognized.")
        return comp

    def translate_for_count_loop(self, loop: ast.ForCountLoop) -> str:
        """Translate ASTx For Range Loop to LLVM-IR."""
        init_type = MAP_TYPE_STR[loop.initializer.type_]

        # cond = self.translate(loop.condition)
        comp = self.translate_integer_comparison(loop.condition.op_code)
        comp_rhs = loop.condition.rhs.value

        result = (
            "for.cond:"
            f"  %i.val = load {init_type}, {init_type}* %i"
            f"  %cond = {comp} {init_type} %i.val, {comp_rhs}"
            "  br i1 %cond, label %for.body, label %for.end"
            ""
            "for.body:"
            "  %i.next = add i32 %i.val, 1"
            "  store i32 %i.next, i32* %i"
            "  br label %for.cond"
            ""
            "for.end:"
        )

        return result

    def translate_for_range_loop(self, loop: ast.ForRangeLoop) -> str:
        """Translate ASTx For Range Loop to LLVM-IR."""
        return ""

    def translate_module(self, module: ast.Module) -> str:
        """Translate ASTx Module to LLVM-IR."""
        scope = self.symtable.scopes.add(f"module {module.name}")
        self.symtable.scopes.set_default_parent(scope)

        block_result = self.translate_block(module.block)

        if scope.parent:
            self.symtable.scopes.set_default_parent(scope.parent)
        self.symtable.scopes.destroy(scope)

        return (
            f"""; ModuleID = '{module.name}.arx'\n"""
            f"""source_filename = "{module.name}.arx"\n"""
            f"""target datalayout = "{module.target.datalayout}"\n"""
            f"""target triple = "{module.target.triple}"\n\n"""
        ) + block_result

    def translate_i32_literal(self, i32: ast.Int32Literal) -> str:
        """Translate ASTx Int32Literal to LLVM-IR."""
        self.regtable.increase()

        result = (
            "  %{0} = alloca i32, align 4\n"
            "  store i32 0, i32* %{0}, align 4\n"
            "  %{1} = load i32, i32* %{0}, align 4\n"
        ).format(self.regtable.last, self.regtable.last + 1)
        self.regtable.increase()

        i32.comment = str(self.regtable.last)

        return result

    def translate_function_prototype(
        self, prototype: ast.FunctionPrototype
    ) -> str:
        """Translate ASTx Function Prototype to LLVM-IR."""
        scope = "@" if prototype.scope == ast.ScopeKind.global_ else "%"

        trans_args = []
        for i, arg in enumerate(prototype.args):
            self.symtable.define(arg)
            arg.comment = str(self.regtable.last + i)
            trans_args.append(
                f"{MAP_TYPE_STR[arg.type_]} noundef %{arg.comment}"
            )

        args = ", ".join(trans_args)

        # note: `+ 1` is used here because the previous register is used
        # somewhere and the compiler will raise an error.
        if prototype.args:
            self.regtable.redefine(len(prototype.args) + 1)
        else:
            self.regtable.reset()

        return (
            f"define dso_local {MAP_TYPE_STR[prototype.return_type]} "
            f"{scope}{prototype.name}("
            f"{args}"
            ")"
        )

    def translate_function(self, fn: ast.Function) -> str:
        """Translate ASTx Function to LLVM-IR."""
        scope = self.symtable.scopes.add(f"function {fn.prototype.name}")
        self.symtable.scopes.set_default_parent(scope)
        self.regtable.append()

        prototype_result = self.translate_function_prototype(fn.prototype)
        body_result = self.translate_block(fn.body)

        self.regtable.pop()
        if scope.parent:
            self.symtable.scopes.set_default_parent(scope.parent)
        self.symtable.scopes.destroy(scope)

        return f"""{prototype_result} {{\n""" f"""{body_result}\n""" f"}}"

    def translate_return(self, ret: ast.Return) -> str:
        """Translate ASTx Return to LLVM-IR."""
        ret_tpl = "  ret {} %{}"

        ret_value = self.translate(ret.value)

        reg_n = ret.value.comment

        reg_tp = MAP_TYPE_STR[ret.value.type_]
        return f"{ret_value}\n{ret_tpl.format(reg_tp, reg_n)}"

    def translate_variable(self, var: ast.Variable) -> str:
        """Translate ASTx Variable to LLVM-IR."""
        return f"variable {var.name}"


class LLVMIR(Builder):
    """LLVM-IR transpiler and compiler."""

    def __init__(self) -> None:
        """Initialize LLVMIR."""
        super().__init__()
        self.translator: BuilderTranslator = LLVMTranslator()

    def build(self, expr: ast.AST, output_file: str) -> None:
        """Transpile the ASTx to LLVM-IR and build it to an executable file."""
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
        """Run the generated executable."""
        sh([self.output_file])
