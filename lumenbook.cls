%% lumenbook.cls -- 澄明讲义 / Lumen Book
%% 2026. Inspired primarily by Changxing Su's subook (2021), with
%% design references to Federico Marotta et al.'s kaobook (2021).
%% A new implementation; the original projects remain unmodified.
%% Distributed under LPPL 1.3c or later. See LICENSE and SOURCES.md.
\NeedsTeXFormat{LaTeX2e}[2022-06-01]
\ProvidesClass{lumenbook}[2026/11/09 v1.3 Bilingual margin lecture notes]

\RequirePackage{iftex}
\ifPDFTeX
  \ClassError{lumenbook}{XeLaTeX or LuaLaTeX is required}
    {Select XeLaTeX (recommended) or LuaLaTeX as your compiler.}
  \expandafter\endinput
\fi
\RequirePackage{kvoptions}
\SetupKeyvalOptions{family=lumen,prefix=lumen@}
\DeclareStringOption[right]{margin}
\DeclareStringOption[auto]{fontset}
\DeclareStringOption[local]{fonts}
\DeclareStringOption[fonts/]{fontpath}
\DeclareStringOption[english]{language}
\DeclareStringOption[jade]{theme}
\DeclareStringOption[editorial]{cover}
\DeclareStringOption[0mm]{bindingoffset}
\DeclareBoolOption[true]{boxes}
\DeclareBoolOption[true]{solutions}
\DeclareBoolOption[true]{hints}
\def\lumen@fontsize{11pt}
\def\lumen@opening{openany}
\DeclareVoidOption{10pt}{\def\lumen@fontsize{10pt}}
\DeclareVoidOption{11pt}{\def\lumen@fontsize{11pt}}
\DeclareVoidOption{12pt}{\def\lumen@fontsize{12pt}}
\DeclareVoidOption{openright}{\def\lumen@opening{openright}}
\DeclareVoidOption{openany}{\def\lumen@opening{openany}}
\DeclareVoidOption{print}{\def\lumen@margin{outer}}
\DeclareVoidOption{screen}{\def\lumen@margin{right}}
\DeclareVoidOption{twoside}{\def\lumen@margin{outer}}
\DeclareVoidOption{oneside}{\def\lumen@margin{right}}
\DeclareVoidOption{twocolumn}{\ClassError{lumenbook}{Two-column layout is unsupported}
  {Use the one-column text and margin layout.}}
\DeclareDefaultOption{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessKeyvalOptions*
\RequirePackage{etoolbox}
\newif\iflumen@outer
\ifdefstring{\lumen@margin}{outer}{\lumen@outertrue}{%
  \ifdefstring{\lumen@margin}{right}{}{%
    \ClassError{lumenbook}{Invalid margin option: \lumen@margin}
      {Use margin=right (default) or margin=outer.}}}
\ifdefstring{\lumen@language}{english}{}{%
  \ifdefstring{\lumen@language}{chinese}{}{%
    \ClassError{lumenbook}{Invalid language option}{Use english or chinese.}}}
\iflumen@outer
  \PassOptionsToClass{twoside}{book}
\else
  \PassOptionsToClass{oneside}{book}
\fi
\edef\lumen@baseoptions{a4paper,\lumen@fontsize,\lumen@opening}
\expandafter\PassOptionsToClass\expandafter{\lumen@baseoptions}{book}
\LoadClass{book}

\RequirePackage{lumen-fonts}
\RequirePackage{mathtools,amsthm}
\RequirePackage{unicode-math}
\setmathfont{TeX Gyre Termes Math}
\RequirePackage[protrusion=true,expansion=false]{microtype}

\RequirePackage{geometry}
\geometry{top=24mm,bottom=24mm,left=22mm,right=66mm,
  marginparwidth=48mm,marginparsep=6mm,headheight=16pt,headsep=7mm,
  footskip=12mm,bindingoffset=\lumen@bindingoffset}
% Geometry mirrors the type block and the margin together in print mode.
% In screen mode the base class is one-sided, so every margin is right.
\normalmarginpar
\setlength{\marginparpush}{8pt}
\setlength{\parindent}{1.25em}
\setlength{\parskip}{3pt plus 1pt}
\linespread{1.08}
\setlength{\emergencystretch}{1.5em}
\raggedbottom
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{2}

\RequirePackage{graphicx,booktabs,tabularx,enumitem}
\setlist{nosep,topsep=5pt,leftmargin=*}
\RequirePackage{lumen-style}
\RequirePackage{lumen-cover}
\RequirePackage{lumen-margins}
\RequirePackage{lumen-math}
\RequirePackage{lumen-code}
\RequirePackage[unicode,bookmarksnumbered]{hyperref}
\hypersetup{colorlinks=true,linkcolor=LumenAccent,
  citecolor=LumenAccent,urlcolor=LumenAccent,pdfborder={0 0 0}}
\RequirePackage{bookmark}
\RequirePackage{lumen-mark}
\RequirePackage{lumen-study}
\pdfstringdefDisableCommands{\def\\{ }}
\AtBeginDocument{\hypersetup{pdftitle={\@title},pdfauthor={\@author}}}

% Retain English textbook terminology by default; Chinese is an opt-in UI.
\ifdefstring{\lumen@language}{chinese}{%
  \renewcommand{\contentsname}{目录}
  \renewcommand{\listfigurename}{插图目录}
  \renewcommand{\listtablename}{表格目录}
  \renewcommand{\figurename}{图}\renewcommand{\tablename}{表}
  \renewcommand{\chaptername}{章}\renewcommand{\appendixname}{附录}
  \renewcommand{\bibname}{参考文献}
}{%
  \renewcommand{\contentsname}{Contents}
  \renewcommand{\listfigurename}{List of Figures}
  \renewcommand{\listtablename}{List of Tables}
  \renewcommand{\figurename}{Figure}\renewcommand{\tablename}{Table}
  \renewcommand{\chaptername}{Chapter}\renewcommand{\appendixname}{Appendix}
  \renewcommand{\bibname}{Bibliography}
}
\endinput
