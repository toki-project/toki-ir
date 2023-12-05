"""Tests for the Module AST."""
# import pytest

# from arxir import ast
# from arxir.builders.llvmir import LLVMIR

# from .conftest import check_result


# @pytest.mark.parametrize(
#     "action,expected_file",
#     [
#         ("translate", "test_binary_op_basic.ll"),
#         # ("build", ""),
#     ],
# )
# def test_binary_op_basic(action: str, expected_file: str) -> None:
#     """Test ASTx Module with a function called add."""
#     builder = LLVMIR()
#     builder.translator.reset()
#     module = builder.module()

#     a = ast.Variable(name="a", type_=ast.Int32, value=ast.Int32Literal(1))
#     b = ast.Variable(name="b", type_=ast.Int32, value=ast.Int32Literal(2))
#     c = ast.Variable(name="c", type_=ast.Int32, value=ast.Int32Literal(4))
#     lit_1 = ast.Int32Literal(1)

#     basic_op = lit_1 + b - a * c / a + (b - a + c / a)

#     main_proto = ast.FunctionPrototype(
#         name="main", args=[], return_type=ast.Int32
#     )
#     main_block = ast.Block()
#     main_block.append(ast.Return(basic_op))
#     main_fn = ast.Function(prototype=main_proto, body=main_block)

#     module.block.append(main_fn)
#     check_result(action, builder, module, expected_file)
