; ModuleID = 'main.arx'
source_filename = "main.arx"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

declare i32 @"putchar"(i32 %".1")

define float @"putchard"(float %".1")
{
entry:
  %"intcast" = fptoui float %".1" to i32
  %".3" = call i32 @"putchar"(i32 %"intcast")
  ret float              0x0
}

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 1, i32* %2, align 4
  store i32 2, i32* %3, align 4
  store i32 4, i32* %4, align 4
  %5 = load i32, i32* %3, align 4
  %6 = add nsw i32 1, %5
  %7 = load i32, i32* %2, align 4
  %8 = load i32, i32* %4, align 4
  %9 = mul nsw i32 %7, %8
  %10 = load i32, i32* %2, align 4
  %11 = sdiv i32 %9, %10
  %12 = sub nsw i32 %6, %11
  %13 = load i32, i32* %3, align 4
  %14 = load i32, i32* %2, align 4
  %15 = sub nsw i32 %13, %14
  %16 = load i32, i32* %4, align 4
  %17 = load i32, i32* %2, align 4
  %18 = sdiv i32 %16, %17
  %19 = add nsw i32 %15, %18
  %20 = add nsw i32 %12, %19
  ret i32 %20
}
