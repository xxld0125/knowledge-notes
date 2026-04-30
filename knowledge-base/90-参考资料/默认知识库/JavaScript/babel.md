# 一、babel基本理解
+ `babylon` 将 `ES6/ES7` 代码解析成 `AST`
+ `babel-traverse` 对 `AST` 进行遍历转译，得到新的 `AST`
+ 新 `AST` 通过 `babel-generator` 转换成 `ES5`



单纯理解的话还是容易理解的：



1. 黑白七巧板组成的形状，拆分出来得到零件（`ES6/ES7` 解析成 `AST`）
2. 将这些零件换成彩色的（`AST` 编译得到新 `AST`）
3. 将彩色零件拼装成新的形状（`AST` 转换为 `ES5`）



