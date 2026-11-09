# 来源与许可

Lumenbook 是独立实现的 LaTeX 类与八个样式模块，按 LPPL 1.3c 或更新版本
分发；完整许可见 `LICENSE`。源码文件中的版权和许可说明应予保留。
项目维护者为 faguomarry-ux/lumenbook 仓库维护者。

主要设计参考是 Changxing Su 的 subook（2021），包括边注讲义的整体方向。
次要参考是 Federico Marotta 等人的 kaobook（0.9.8，2021），包括模块化
配置及浅底色环境。两个原项目均使用 LPPL；本包不包含其源码快照。

PDE 封面参考 Lawrence C. Evans《Partial Differential Equations》AMS 第二版
的蓝黄几何构图，使用重新绘制的 TikZ 色块、独立排版、中英文标识及热方程。
未附带原封面图片、出版社标志或原书正文；本项目的 LPPL 不覆盖原书封面设计。
Evans 参考书说明可按实际写作需要填写在 `book-info.tex` 的 `\coverreference` 中。

CTeX、fontspec、unicode-math、TikZ、tcolorbox 等外部宏包及发行版字体
仍适用各自的许可。本包不重新分发它们，通过本机 TeX 发行版调用。

项目地址：https://github.com/faguomarry-ux/lumenbook

## 本项目阅读来源（2026-11-09）

- 英文来源：Lawrence C. Evans, *Partial Differential Equations*, Second Edition, Graduate Studies in Mathematics 19, American Mathematical Society。文件夹内 PDF 共 730 页；版权页标示第二版及后续修订重印信息。
- 中文参考：文件夹内《偏微分方程》第二版扫描件，共 524 页。已核对目录、章节起始页及两篇序言（PDF 第 9、11–12 页）；第 1–12 章及附录的逐节译文和证明尚未核对。
- 已转写正文范围：英文原书的第二版序言（书内 xi–xii 页；PDF 第 12–13 页）与第一版序言（书内 xiii–xv 页；PDF 第 14–16 页）。原文中的第一人称、致谢与署名属于 Lawrence C. Evans；中文边注由整理者添加，详见 `docs/PREFACES.md`。
- 原书章、节结构保留；阅读说明、中文边注接口、详细证明接口和英汉术语表入口为本札记新增。内容来源、整理者补充和未完成项须分别记录。
- 此处来源说明不改变原著与译本的版权归属，也不将模板 LPPL 许可扩展到原书内容。
