# 编写约定

## 内容与来源

1. 英文正文以文件夹内 Evans 第二版为数学来源，保留原有章、节顺序。正文使用英文；中文集中用于有必要的词句释义、概念理解和难点提示。
2. 中译本是重要阅读参考，逐页核对术语和解释。它是扫描件；不要把提取不到文字误判为缺页，也不要假定中英文页码对应。
3. 每节文件头记录英文书内页码与物理页码。`SOURCE-MAP.json` 保存对应关系；纸面目录和 PDF 书签共同核过章、节标题。三级小节待整理正文时再补。
4. 保留原书定理、引理、公式、习题的出处标识。模板自有编号与原书编号是两套编号，不得默认相同。新增推论、例子、证明步骤须明确属于整理补充。
5. 原书正文及译文的权利不由模板的 LPPL 许可覆盖。保留原著与译本归属说明。

## 边注接口

```tex
\PDEVocab{provided that}{只要；后面引出假设条件。}
\PDEChinese{一条必要的中文句意或术语说明。}
\PDEIdea{Explain the key idea or a hidden hypothesis.}
```

这些命令调用现有 `\mn` 和 `\marginheading`。边注要短且就近，不能每句都译。
中文帮助识别定义、假设、结论和关键逻辑，避免直接以整段译文替代英文阅读。
普通边注放在正文段落或环境之后，勿直接放入定理盒子、标题或目录参数。
如需现有模板的 `\mn[位移]{...}`，应逐页看排版，确认没有碰撞再保留。

## 证明展开接口

```tex
\begin{expandedproof}[source section ..., Theorem ...]
  % Complete English proof, with explicit steps and cross-references.
\end{expandedproof}

\begin{proofdetails}[Why this limit is valid / 极限交换的理由]
  % Longer supplementary explanation belongs in the main text.
\end{proofdetails}
```

`expandedproof` 沿用 `amsthm` 的证明机制；`proofdetails` 沿用模板的可跨页说明盒子。
不要只把“显然”换成“容易看出”。展开时要：

- 列清定义域、边界光滑性、系数条件、函数空间与指数范围。
- 说明每次分部积分的合法性及边界项处理；说明非光滑函数如何由逼近得到。
- 对极限交换给出收敛类型、控制条件或紧性依据；注明常数依赖。
- 把外部引用的定理、仍未证明的结论与本节完成的证明区分开。
- 标记整理者补充，核对是否无意加强原书结论或更改假设。

模板示例位于 `templates/`，只供复制，不直接加入主文件。
每节完成后去掉该节的 `\PDEPending`，并更新进度记录。不得以编译成功替代数学核对。

## 文件与排版

- `main.tex` 控制整书顺序；`parts/` 只负责分部及章节入口。
- 每章/附录一个目录，每节一个文件，后续小节先在相应节文件中使用 `\subsection`。
- 项目专用命令只放 `config/pde-macros.tex`，尽量不改 `lumenbook.cls` 和 `lumen-*.sty`。
- 项目版式在 `config/pde-layout.tex`：默认 A4、右侧 38 mm 边注、6 mm 间隔与 132 mm 正文。`main.tex` 使用 `margin=right,12pt` 基础类配置，实际正文字号通过 `fontsize` 宏包设为 **13pt**；边注固定为 10pt，目录使用独立字号。不使用可能被 geometry 识别为纸张尺寸的 `screen` 选项。
- `\part` 与 `\part*` 使用标准书籍分部标题，分隔页临时取消边注栏并整页居中，随后自动恢复正文版式。
- 页码以整张物理页面为基准，在底部居中；正文页、章首页、目录与 Part 页一致。
- 目录临时取消边注栏，使用整页宽度；`\titlecontents` 在节编号前添加 `\S`（§），配合浅色点线。此符号仅用于目录排版，不改变原书节号、正文编号或 PDF 书签。
- 交付前运行 XeLaTeX 完整编译，检查目录链接、页眉、中文字体、长标题和边注碰撞，并查看 PDF 渲染页。
