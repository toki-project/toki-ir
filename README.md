# Arx-IR

**Arx-IR** aims to provide a translator to LLVM-IR and other IR languages from
[**ASTx**](https://github.com/arxlang/astx) objects.

**ASTx** is a generic project that offers a way to compound in an expressive way
an **AST**. It is not specific for the **ArxLang** project, although it is main
focus is to provide all needed feature for it.

**Arx-IR** does not use any **LLVM-IR** dependency to create the **LLVM-IR**
source, in another words, it creates all **LLVM-IR** source from scratch.
**Arx-IR** just uses `clang` and `llc` as dependencies in order to compile the
generated **LLVM-IR** source to binary files.

- Free software: BSD 3 Clause
- Documentation: https://arxlang.github.io/arx-ir.

## Features

- Generate **LLVM-IR** from **ASTx**
- Compile **LLVM-IR** to binary files using `clang` and `llc`
