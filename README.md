# Partial Differential Equations：英文精读与中文边注

基于 Lawrence C. Evans《Partial Differential Equations》第二版，
使用现有 `lumenbook.cls` 和 `lumen-*.sty` 排版。英文为正文，必要的中文词句释义和数学解释放在边注，
简略证明的详细展开写在正文。扫描版《偏微分方程》是重要阅读参考。

**当前是目录骨架**：已建立原书 12 章、3 个主体部分、A–E 五个附录及各节文件；
英文正文、习题、证明补充和逐节中文注释尚未开始。阅读说明中的边注仅用于展示接口。

## 图书与预览

| 文件 | 用途 |
| --- | --- |
| [Partial Differential Equations.pdf](./Partial%20Differential%20Equations.pdf) | 英文原书，作为章节结构、定理、公式与证明的主要来源 |
| [偏微分方程.pdf](./偏微分方程.pdf) | 第二版中译本扫描件，用于核对术语和辅助理解 |
| [目录骨架预览](./output/pdf/pde-annotated-outline.pdf) | 当前 41 页的札记骨架，含目录链接和边注示例 |

两本参考书 PDF、LaTeX 源码与发布预览一同纳入版本管理。
原书页码、PDF 物理页码与札记页码分别记录；详细对照见 [全书目录](./docs/CONTENTS.md)。

## 已完成

- [x] 沿用现有 `lumenbook.cls` 和全部 `lumen-*.sty` 排版配置。
- [x] 建立 3 个主体部分、12 章和 A–E 五个附录，按节拆分为 111 个文件。
- [x] 接通阅读说明、两篇序言、参考文献、索引和英汉术语表入口。
- [x] 记录英文各节起始页、中译本各章起始页及机器可读来源对照。
- [x] 配置词句释义、中文提示、数学难点三类边注，并提供版面示例。
- [x] 配置正文中的详细证明与长推导说明环境。
- [x] 编译生成 41 页目录骨架，核对 138 个书签与 138 个目录链接，检查版面。
- [x] 整理 Git 忽略规则与 PDF 二进制属性，保留两本参考书和发布预览。
- [x] 调整为 Part 整页居中、固定右侧 38 mm 边注栏和 12pt 正文。

## 待办

按以下顺序推进；每节完成后同步更新 [详细进度](./docs/PROGRESS.md)。

- [ ] 整理第 1 章英文正文，结合附录 A 统一记号和多重指标约定。
- [ ] 以第 1 章形成完整样章：英文正文、必要中文边注、出处标识与交叉引用。
- [ ] 进入第 2 章，逐节整理四类线性方程，并补充原书省略的推导和证明步骤。
- [ ] 依次整理第 3–12 章及附录 A–E，按正文补建三级小节。
- [ ] 逐节核对中译本的对应页码、术语和解释。
- [ ] 建立原书与札记的定理、引理、公式及习题编号对照。
- [ ] 整理习题与所需解答，补充英汉术语表和索引条目。
- [ ] 核对证明的假设、边界项、极限交换、常数依赖及外部定理引用。
- [ ] 开展内容复核与独立数学审阅，记录发现的问题和修订。

以上正文与数学工作均尚未完成。编译通过和版面检查不代表数学证明已经补全或通过审阅。

## 更新记录

| 日期 | 已完成记录 | 后续工作 |
| --- | --- | --- |
| 2026-11-09 | 建立 12 章、5 个附录及 111 节目录骨架；加入来源对照、边注与证明接口；生成并检查 40 页预览 | 从第 1 章和附录 A 开始正文整理 |
| 2026-11-09 | 完善 `.gitignore`、增加 `.gitattributes`，整理 README 的文件入口、完成清单与待办；将两本 PDF 与项目源码一同纳入版本管理 | 随正文进展持续更新文档与发布预览 |
| 2026-11-09 | Part 页取消边注栏并整页居中；边注固定右侧、栏宽从 48 mm 收窄至 38 mm；正文字号从 11pt 调整至 12pt，更新为 41 页 A4 预览 | 按新版式整理第 1 章 |

## 编译与预览

需要 TeX Live / MiKTeX，使用 XeLaTeX 和 UTF-8：

```powershell
latexmk -xelatex main.tex
```

编译结果为 `build/main.pdf`；仓库内的发布预览为 `output/pdf/pde-annotated-outline.pdf`。
没有 latexmk 时，先创建 `build`，再运行两遍：

```powershell
New-Item -ItemType Directory -Force build
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

默认 A4 单面阅读版式，英文正文字号为 **12pt**，所有边注固定在**右侧**。
边注栏宽 **38 mm**，与正文间隔 **6 mm**；正文宽度为 **132 mm**。
Part 分隔页临时取消边注栏，保留标准书籍样式并以整页居中；进入章节后恢复正文与边注布局。
项目版式集中在 `config/pde-layout.tex`，字号与单面选项位于 `main.tex`。
当前沿用模板自带的 TeX Gyre / Fandol 字体；类与样式文件保持原样。

更新发布预览时，在完整编译和版面检查通过后运行：

```powershell
Copy-Item -LiteralPath build/main.pdf -Destination output/pdf/pde-annotated-outline.pdf
```

`build/` 和 `tmp/` 只存放本地中间文件，不提交到 GitHub；`output/pdf/` 存放有意发布的预览。

## 目录分工

```text
main.tex                         整书入口
book-info.tex                    封面与 PDF 元数据
config/pde-macros.tex             边注、来源、证明展开接口
config/pde-layout.tex             右侧窄边注与 Part 整页居中布局
frontmatter/                     阅读说明、两篇序言的整理入口
parts/                           三个主体部分
chapters/01-introduction/        第 1 章入口与各节文件
chapters/02-.../ 至 12-.../       第 2–12 章，各章按节拆分
appendices/a-notation/ 至 e-.../  附录 A–E，各附录按节拆分
backmatter/                      参考文献、索引、附加英汉术语表
templates/                       节与证明的编写示例，不直接编译
docs/CONTENTS.md                  全书章/节、源页码和文件链接
docs/SOURCE-MAP.json              机器可读来源对照
docs/EDITORIAL-GUIDE.md            写作、来源、边注与证明展开约定
docs/PROGRESS.md                  已完成工作和未开始内容
docs/VALIDATION.md                本轮结构、编译和版面验证记录
output/pdf/                      交付预览
build/                           LaTeX 中间文件与编译结果
```

原书第 1 章位于 Part I 之前。Part I 为第 2–4 章，Part II 为第 5–7 章，Part III 为第 8–12 章。
目录先搭到“节”；三级小节在精读相应英文正文时继续建立。
原书书内页码、PDF 物理页码和本札记页码分别记录。

## 开始填充内容

1. 通过 [全书目录](./docs/CONTENTS.md) 找到目标节文件及英文来源页。
2. 核对英文正文与中译本，按 [编写约定](./docs/EDITORIAL-GUIDE.md) 填入英文内容和必要边注。
3. 使用 `expandedproof` / `proofdetails` 补充证明，保留原书出处与新增步骤的区别。
4. 完成内容核对后移除该节 `\PDEPending`，更新进度并编译检查页面。

常用环境仍为 `definition`、`theorem`、`lemma`、`proof`、`example`、`exercise`。
项目新增 `\PDEVocab{词句}{释义}`、`\PDEChinese{中文提示}`、`\PDEIdea{难点解释}`；
底层仍可直接使用模板的 `\mn`、`\sn`、`marginfigure` 等接口。

## 来源与许可

排版模板的来源和 LPPL 许可见 [SOURCES.md](./SOURCES.md) 与 [LICENSE](./LICENSE)。
原著与中译本另有其各自权利；模板许可不覆盖这些图书内容。
当前构建过程只从英文 PDF 的书签与目录读取结构，没有将整本 PDF 自动转写为正文。
