from arxir.builders.base import Builder, BuilderTranslator
from arxir.builders.llvmir.translator import LLVMTranslator

# numeric binary operation


class LLVMIR(Builder):
    def __init__(self):
        self.translator: BuilderTranslator = LLVMTranslator()
