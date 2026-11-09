# Partial Differential Equations：英文精读与中文边注

基于 Lawrence C. Evans《Partial Differential Equations》第二版，
使用现有 `lumenbook.cls` 和 `lumen-*.sty` 排版。英文为正文，专业的中文数学解释放在边注，
简略证明的详细展开写在正文。扫描版《偏微分方程》是重要阅读参考。

**当前已整理两篇序言和第一至第六章的英文正文与专业中文数学边注**。第一章六节已填入原书英文内容、34 个模型方程、5 道原书习题与整理者解答，另补充主部计算、热方程估计与不稳定性、Burgers 梯度爆破及激波计算。
第二章新增四类线性方程的详细推导、球均值与热球平均专题、33 条中文边注和 24 题解答，独立版 32 页；详见 [第二章记录](./docs/CHAPTER-02.md)。
第三章新增特征线、Hopf–Lax、熵解与 N 波的证明，36 条中文边注、20 题解答及三组示意图，独立版 32 页；详见 [第三章记录](./docs/CHAPTER-03.md)。
第四章新增表示方法、渐近分析与解析 Cauchy 理论，38 条中文数学边注、21 处证明展开、19 题解答及两组图形，独立版 39 页；详见 [第四章记录](./docs/CHAPTER-04.md)。
第五章新增 47 条中文数学边注、26 处正文证明展开和 21 道习题解答，独立版 34 页；详见 [第五章记录](./docs/CHAPTER-05.md)。
第六章新增弱解、正则性、最大值原理与谱理论，43 条中文边注、18 处证明展开及 17 题解答，独立版 30 页；详见 [第六章记录](./docs/CHAPTER-06.md)。第 7–12 章和 A–E 附录仍为骨架。第一章已完成本轮来源核对与整理者自检，尚未独立数学审阅；详见 [第一章记录](./docs/CHAPTER-01.md)。
序言的来源核对、版本差异和完成范围见 [序言整理记录](./docs/PREFACES.md)。

**前六章另已补充 30 幅原生 TikZ 图**：每章 4 幅正文图、1 幅边注图，附数学图注与可编辑源码。图解位置、读图问题和源码入口见 [TikZ 图解索引](./docs/TIKZ-DIAGRAMS.md)。

## 图书与预览

| 文件 | 用途 |
| --- | --- |
| [Partial Differential Equations.pdf](./Partial%20Differential%20Equations.pdf) | 英文原书，作为章节结构、定理、公式与证明的主要来源 |
| [偏微分方程.pdf](./偏微分方程.pdf) | 第二版中译本扫描件，用于核对术语和辅助理解 |
| [札记预览](./output/pdf/pde-annotated-outline.pdf) | 当前 226 页，含两篇序言和第一至第六章详细证明与习题解答、中文边注及其余章节骨架 |
| [第一章独立学习稿](./output/pdf/pde-chapter-01-introduction.pdf) | 22 页；方程分类、模型机制、适定性、稳定性与特征线聚焦，含新增 TikZ 图 |
| [第二章独立学习稿](./output/pdf/pde-chapter-02-linear-equations.pdf) | 32 页；四类线性方程，重点为球均值与热球平均，以及 24 题解答 |
| [第三章独立学习稿](./output/pdf/pde-chapter-03-nonlinear-first-order.pdf) | 32 页；特征线、Hopf–Lax、熵解、Riemann 问题、N 波及 20 题解答 |
| [第四章独立学习稿](./output/pdf/pde-chapter-04-representation-methods.pdf) | 39 页；分离变量、相似解、变换、渐近、幂级数及 19 题解答 |
| [第五章独立学习稿](./output/pdf/pde-chapter-05-sobolev.pdf) | 34 页；弱导数、逼近、延拓、迹、嵌入、紧性及 21 题解答 |
| [第六章独立学习稿](./output/pdf/pde-chapter-06-elliptic-equations.pdf) | 30 页；弱解存在性、差商与边界正则性、最大值原理、特征值及 17 题解答 |

两本参考书 PDF、LaTeX 源码与发布预览一同纳入版本管理。
原书页码、PDF 物理页码与札记页码分别记录；详细对照见 [全书目录](./docs/CONTENTS.md)。

## 已完成

- [x] 沿用现有 `lumenbook.cls` 和全部 `lumen-*.sty` 排版配置。
- [x] 建立 3 个主体部分、12 章和 A–E 五个附录，按节拆分为 111 个文件。
- [x] 接通阅读说明、两篇序言、参考文献、索引和英汉术语表入口。
- [x] 记录英文各节起始页、中译本各章起始页及机器可读来源对照。
- [x] 配置按数学主题命名的边注：假设作用、结构、反例、退化与方法联系。
- [x] 配置正文中的详细证明与长推导说明环境。
- [x] 为前六章加入 24 幅正文及 6 幅边注原生 TikZ 图，核对图注、数学含义和版面。
- [x] 编译生成 226 页整书预览，以及第一至第六章独立版（22、32、32、39、34、30 页），核对书签、链接和边注版面。
- [x] 整理 Git 忽略规则与 PDF 二进制属性，保留两本参考书和发布预览。
- [x] 调整为 Part 整页居中、固定右侧 38 mm 边注栏和 **13pt 正文**。
- [x] 页码按整页底部居中；目录使用整页宽度、分层标题、`§` 节号与浅色点状引导线。
- [x] 完整转写并排版第一版、第二版序言，保留作者致谢、署名、日期及英文印次说明。
- [x] 为序言保留 7 条数学与版本边注，清理普通词汇与句式解释；核对中译本并标明印次差异。

## 待办

按以下顺序推进；每节完成后同步更新 [详细进度](./docs/PROGRESS.md)。

- [x] 整理第 1 章六节英文内容，补充多重指标、主部与分类约定。
- [x] 以第 1 章形成完整样章：英文正文、22 条专业数学边注、5 题解答、出处标识与交叉引用。
- [x] 整理第 2 章四类线性方程，展开球均值及热球均值证明、权重归一化和联系，完成 24 题解答。
- [x] 整理第 3 章六节，补充局部解梯度相容、半凹与熵唯一性、N 波证明及 20 题解答。
- [x] 整理第 4 章八节，展开 Fourier／Radon、Cole–Hopf、驻相、均匀化和 CK 证明，完成 19 题解答。
- [x] 整理第 5 章 Sobolev 工具与第 6 章椭圆方程理论，补齐全部习题解答。
- [ ] 继续整理第 7–12 章及附录 A–E，按正文补建三级小节。
- [ ] 逐节核对中译本的对应页码、术语和解释。
- [ ] 建立原书与札记的定理、引理、公式及习题编号对照。
- [ ] 整理习题与所需解答，补充英汉术语表和索引条目。
- [ ] 核对证明的假设、边界项、极限交换、常数依赖及外部定理引用。
- [ ] 开展内容复核与独立数学审阅，记录发现的问题和修订。

第 1–6 章已形成学习稿，尚待独立数学审阅；第 7–12 章及附录正文仍未开始。来源核对、整理者自检、编译和视觉检查分别记录，不能相互替代。

## 更新记录

| 日期 | 已完成记录 | 后续工作 |
| --- | --- | --- |
| 2026-11-09 | 建立 12 章、5 个附录及 111 节目录骨架；加入来源对照、边注与证明接口；生成并检查 40 页预览 | 从第 1 章和附录 A 开始正文整理 |
| 2026-11-09 | 完善 `.gitignore`、增加 `.gitattributes`，整理 README 的文件入口、完成清单与待办；将两本 PDF 与项目源码一同纳入版本管理 | 随正文进展持续更新文档与发布预览 |
| 2026-11-09 | Part 页取消边注栏并整页居中；边注固定右侧、栏宽从 48 mm 收窄至 38 mm；正文字号从 11pt 调整至 12pt，更新为 41 页 A4 预览 | 按新版式整理第 1 章 |
| 2026-11-09 | 统一正文、前置页与 Part 页的底部居中页码；美化整页目录，111 个节条目加入 `§` 符号与点状引导线 | 按新版式整理第 1 章 |
| 2026-11-09 | 按最终要求将正文字号设为 13pt；完成两篇原著序言全文与 12 条中文边注，核对英文原文及中译本，更新为 45 页预览 | 开始第 1 章与附录 A 的正文整理 |

本轮更新（2026-11-09）：补齐第一章六节、34 个模型与 5 题解答；采用按数学主题命名的边注，重写阅读说明并清理序言词句边注，加入第一章英汉术语，更新 63 页预览。此前按学习需要完成第五章，再补第二章热球专题；此前完成第三章；本轮补齐第四章，形成 188 页整书预览。后续开展已整理章节的独立数学复核。

本轮更新（2026-11-10）：补齐第六章二阶椭圆方程，新增 43 条中文数学边注、18 处证明展开和 17 题解答，独立版 29 页，整书更新为 216 页。后续继续第七章及已整理章节的独立数学复核。

本轮图解更新（2026-11-10）：前六章每章新增 5 幅 TikZ 图，补充第一章独立版，并更新六份章节预览；整书为 226 页。图解校验和页码以 [图解索引](./docs/TIKZ-DIAGRAMS.md) 为准。

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

默认 A4 单面阅读版式，英文正文字号为 **13pt**，所有边注固定在**右侧**。
边注栏宽 **38 mm**，与正文间隔 **6 mm**；正文宽度为 **132 mm**。
Part 分隔页临时取消边注栏，保留标准书籍样式并以整页居中；进入章节后恢复正文与边注布局。
页码位于整张页面底部正中。目录临时采用整页宽度，分部标题突出、章标题加粗，节编号以 `§ 1.1` 的形式显示，并用浅色点线连接页码。
项目版式与实际正文字号集中在 `config/pde-layout.tex`，通过 `fontsize` 宏包设为 13pt；`main.tex` 负责基础类与右侧边注选项。
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
config/pde-layout.tex             右侧窄边注、居中页码、Part 与目录布局
frontmatter/                     阅读说明、已完成的两篇原著序言与中文边注
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
docs/PREFACES.md                  两篇序言的来源、版本差异与核对记录
output/pdf/                      交付预览
build/                           LaTeX 中间文件与编译结果
```

原书第 1 章位于 Part I 之前。Part I 为第 2–4 章，Part II 为第 5–7 章，Part III 为第 8–12 章。
全书目录列到“节”；第一至第六章正文已加入三级小节，其余章节随精读正文继续建立。
原书书内页码、PDF 物理页码和本札记页码分别记录。

## 开始填充内容

1. 通过 [全书目录](./docs/CONTENTS.md) 找到目标节文件及英文来源页。
2. 核对英文正文与中译本，按 [编写约定](./docs/EDITORIAL-GUIDE.md) 填入英文内容和必要边注。
3. 使用 `expandedproof` / `proofdetails` 补充证明，保留原书出处与新增步骤的区别。
4. 完成内容核对后移除该节 `\PDEPending`，更新进度并编译检查页面。

常用环境仍为 `definition`、`theorem`、`lemma`、`proof`、`example`、`exercise`。
专业数学边注使用 `\PDEAnnotation{具体数学主题}{数学解释}`；普通词汇和句式不再占用边栏。
底层仍可直接使用模板的 `\mn`、`\sn`、`marginfigure` 等接口。

## 来源与许可

排版模板的来源和 LPPL 许可见 [SOURCES.md](./SOURCES.md) 与 [LICENSE](./LICENSE)。
原著与中译本另有其各自权利；模板许可不覆盖这些图书内容。
章节骨架依据英文 PDF 的目录与书签建立；两篇序言与第 1 章已对照英文原书整理；中文数学边注及标记为 Editorial supplement 的推导和习题解答为整理者新增。第二至第五章按原书顺序重新撰写学习讲义，证明与习题解答为整理者重构，非逐字转写。第 7–12 章和附录仍为骨架。

第五章可单独编译：latexmk -xelatex -halt-on-error chapter-05.tex；输出为 build/chapter-05.pdf。其余详情和建议学习路线见 [第五章记录](./docs/CHAPTER-05.md)。

第二章可独立编译：latexmk -xelatex -halt-on-error chapter-02.tex。球均值在独立版第 4–6 页，热球专题在第 12–17 页；推导、来源和验证见 [第二章记录](./docs/CHAPTER-02.md)。
