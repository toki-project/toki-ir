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

define dso_local i32 @add(i32 noundef %0, i32 noundef %1) {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  store i32 %1, i32* %4, align 4
  %5 = load i32, i32* %3, align 4
  %6 = load i32, i32* %4, align 4
  %7 = add nsw i32 %5, %6
  ret i32 %7
}

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  ret i32 0
}
