
\NeedsTeXFormat{LaTeX2e}[1996/12/01]
\ProvidesClass{tesisutec}[2017/05/03 v1.0 LaTeX document class]
\def\baseclass{book}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\baseclass}}
\def\@checkoptions#1#2{
  \edef\@curroptions{\@ptionlist{\@currname.\@currext}}
  \@tempswafalse
  \@tfor\@this:=#2\do{
    \@expandtwoargs\in@{,\@this,}{,\@curroptions,}
    \ifin@ \@tempswatrue \@break@tfor \fi}
  \let\@this\@empty
  \if@tempswa \else \PassOptionsToClass{#1}{\baseclass}\fi
}
\@checkoptions{11pt}{{10pt}{11pt}{12pt}}
\PassOptionsToClass{a4paper}{\baseclass}
\ProcessOptions\relax
\LoadClass{\baseclass}

\newcommand\bhrule{\typeout{------------------------------------------------------------------------------}}

% For Spanish
\usepackage[utf8]{inputenc}
\PassOptionsToPackage{english}{babel}
\PassOptionsToPackage{spanish,es-tabla,es-nodecimaldot}{babel}
\RequirePackage{babel}
% For Times New Roman
\RequirePackage{amsthm}
\RequirePackage{newtxtext,newtxmath}
% For section styles
\RequirePackage{titlesec}

\renewcommand{\thesection}{\arabic{chapter}.\arabic{section}}
\renewcommand{\thesubsection}{\arabic{chapter}.\arabic{section}.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\arabic{chapter}.\arabic{section}.\arabic{subsection}.\arabic{subsubsection}}




% For contents table
\RequirePackage[subfigure]{tocloft}
%\usepackage[tocflat]{tocstyle}
%\usetocstyle{standard}

%%%
\newcommand{\orcid}[1]{\href{https://orcid.org/#1}{\includegraphics[width=10pt]{./images/ORCID128px.png}}}

% ====================================================================

% ====================================================================
\newcommand\dedicatory[1]{
  \setstretch{1.0}
  \null\vfil
  \vskip 60\p@
  \vspace{4.5cm}
  ${~}$\hfill \textbf{DEDICATORIA:} \\
  \begin{flushright}{\sl #1}\end{flushright}
  \vfil\null
  \thispagestyle{empty}
  \cleardoublepage
  \setstretch{1.5}
}

\newcommand\acknowledgements[1]{
  \setstretch{1.0}
  \null\vfil
  \vskip 60\p@
  \vspace{4.5cm}
  ${~}$\hfill \textbf{AGRADECIMIENTOS:} \\
  \begin{flushright}{\sl #1}\end{flushright}
  \vfil\null
  \thispagestyle{empty}
  \cleardoublepage
  \setstretch{1.5}
}

% ====================================================================


\newcommand\btypeout[1]{\bhrule\typeout{\space #1}\bhrule}
\usepackage{setspace}
\onehalfspacing
\setlength{\parindent}{1.25cm}
\setlength{\parskip}{2.0ex plus0.5ex minus0.2ex}
\usepackage{vmargin}
\setmarginsrb           { 3.0cm}  % left margin
                        { 3.0cm}  % top margin
                        { 3.0cm}  % right margin
                        { 3.0cm}  % bottom margin
                        {  20pt}  % head height
                        {0.25in}  % head sepa
                        {   9pt}  % foot height
                        { 0.3in}  % foot sep
\raggedbottom
\setlength{\topskip}{1\topskip \@plus 5\p@}
\doublehyphendemerits=10000       % No consecutive line hyphens.
\brokenpenalty=10000              % No broken words across columns/pages.
\widowpenalty=9999                % Almost no widows at bottom of page.
\clubpenalty=9999                 % Almost no orphans at top of page.
\interfootnotelinepenalty=9999    % Almost never break footnotes.
\usepackage{fancyhdr}
\chead{}\rfoot{\thepage}\lfoot{}\cfoot{}
\renewcommand{\headrulewidth}{0pt} % To remove header line
\fancyhead{}
\pagestyle{fancy}
\renewcommand{\chaptermark}[1]{\btypeout{\thechapter\space #1}\markboth{\@chapapp\ \thechapter\ #1}{\@chapapp\ \thechapter\ #1}}
\renewcommand{\sectionmark}[1]{}
\renewcommand{\subsectionmark}[1]{}
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
\hbox{}
\thispagestyle{empty}
\newpage
\if@twocolumn\hbox{}\newpage\fi\fi\fi}
\usepackage{amsmath,amsfonts,amscd,xspace}
\theoremstyle{plain}
\newtheorem{example}{Example}[chapter]
\newtheorem{theorem}{Theorem}[chapter]
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\usepackage[centerlast,small,sc]{caption}
\setlength{\captionmargin}{20pt}
\newcommand{\fref}[1]{Figure~\ref{#1}}
\newcommand{\tref}[1]{Table~\ref{#1}}
\newcommand{\eref}[1]{Equation~\ref{#1}}
\newcommand{\cref}[1]{Chapter~\ref{#1}}
\newcommand{\sref}[1]{Section~\ref{#1}}
\newcommand{\aref}[1]{Appendix~\ref{#1}}
\renewcommand{\topfraction}{0.85}
\renewcommand{\bottomfraction}{.85}
\renewcommand{\textfraction}{0.1}
\renewcommand{\dbltopfraction}{.85}
\renewcommand{\floatpagefraction}{0.75}
\renewcommand{\dblfloatpagefraction}{.75}
\setcounter{topnumber}{9}
\setcounter{bottomnumber}{9}
\setcounter{totalnumber}{20}
\setcounter{dbltopnumber}{9}
\usepackage{graphicx}
\usepackage{epstopdf}
\usepackage[scriptsize]{subfigure}
\usepackage{booktabs}
\usepackage{rotating}
\usepackage{listings}

\usepackage[pdfpagemode={UseOutlines},bookmarks=true,bookmarksopen=true,
   bookmarksopenlevel=0,bookmarksnumbered=true,hypertexnames=false,
   colorlinks,linkcolor={black},citecolor={blue},urlcolor={red},
   pdfstartview={FitV},unicode,breaklinks=true]{hyperref}
\pdfstringdefDisableCommands{
   \let\\\space
}
\newcommand*{\supervisor}[1]{\def\supname{#1}}
\newcommand*{\examiner}[1]{\def\examname{#1}}
\newcommand*{\examinertwo}[1]{\def\examnametwo{#1}}
\newcommand*{\president}[1]{\def\presname{#1}}
\newcommand*{\degree}[1]{\def\degreename{#1}}
\renewcommand*{\author}[1]{\def\authornames{#1}}
\newcommand*{\authorid}[1]{\def\studentid{#1}}
\newcommand*{\department}[1]{\def\deptname{#1}}
\newcommand*{\subject}[1]{\def\subjectname{#1}}
\newcommand*{\keywords}[1]{\def\keywordnames{#1}}
\renewcommand*{\date}[1]{\def\dateMY{#1}}
\supervisor  {}
\examiner    {}
\degree      {}
\author      {}
\subject     {}
\keywords    {}

% ====================================================================
\renewcommand\maketitle{
  \btypeout{Title Page}
  \hypersetup{pdftitle={\@title}}
  \hypersetup{pdfsubject=\subjectname}
  \hypersetup{pdfauthor=\authornames}
  \hypersetup{pdfkeywords=\keywordnames}
  \thispagestyle{empty}
  \begin{titlepage}
    \let\footnotesize\small
    \let\footnoterule\relax
    \let \footnote \thanks
    \setcounter{footnote}{1}
    \null\vfil
    %\vskip 60\p@
    \begin{center}
      \setlength{\parskip}{0pt}
      \vspace{-1.5cm}
      {\Large \textbf{UNIVERSIDAD DE INGENIERÍA Y TECNOLOGÍA}\par}
      \vspace{0.5cm}
      {\Large {ESCUELA DE POSGRADO }\par}
      \vfill
      \vspace{0.5cm}
      \includegraphics[height=2.6cm]{images/Logo versión 4.png}\\
      \vfill
      {\Large \bf \@title \par}
      \vspace{1.5cm}
      {\large \textbf{TRABAJO DE INVESTIGACIÓN}\par}
      {\large Para optar el grado de \degreename \par}
      \vfill
      \smallskip
      \vspace{0.5cm}
      {\large \textbf{AUTOR(ES)}\par}
      {\large \authornames \par}
      \vspace{0.5cm}
%      {\large \textbf{Código \studentid} \par}
      \vspace{0.5cm}
      {\large \bf ASESOR(ES) \par}
      \smallskip
      {\large \supname \par}
      \vfill
      \vspace{1.5cm}
      {\large Lima -- Perú \par}
      {\large \dateMY \par}
    \end{center}
    \par
    \@thanks
    \vfil\null
  \end{titlepage}
  %\setcounter{footnote}{1}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\and\relax
  \cleardoublepage
}


% ====================================================================

% ====================================================================

\addtocounter{secnumdepth}{2}
\setcounter{tocdepth}{6}
\newcounter{dummy}
\newcommand\addtotoc[1]{
%\refstepcounter{dummy}
\addcontentsline{toc}{chapter}{#1}}




\cftsetindents{section}{0em}{2em}
\cftsetindents{subsection}{0em}{2em}
%\renewcommand\contentsname{TABLA DE CONTENIDO}
%\renewcommand{\contentsname}{\centering TABLA DE CONTENIDO}
\renewcommand\cfttoctitlefont{\hfill\Large}
\renewcommand\cftaftertoctitle{\hfill\mbox{}}
%\setcounter{tocdepth}{2}


\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\thechapter}{\Roman{chapter}}
\renewcommand{\thefigure}{\arabic{chapter}.\arabic{figure}.}
\renewcommand{\thetable}{\arabic{chapter}.\arabic{table}.}
\renewcommand{\theequation}{\arabic{chapter}.\arabic{equation}}
\renewcommand{\cftchapaftersnum}{\quad}
\renewcommand{\cftchappagefont}{\normalfont}
\addtocontents{toc}{\hfill{P\'ag.}\par}

\RequirePackage{titletoc}

% Solo muestra el título del capítulo en el TOC
\titlecontents{chapter}
  [0pt]
  {\normalfont}
  {} % <-- quitamos "CAPÍTULO I"
  {}
  {\titlerule*[0.6em]{.}\contentspage}
  []


%\RequirePackage{tocloft}


\RequirePackage{caption}
% ====================================================================
% ÍNDICE DE FIGURAS
% ====================================================================

\renewcommand\listoffigures{%
\begin{spacing}{1}{
  \setlength{\parskip}{1pt}
  \if@twocolumn
    \@restonecoltrue\onecolumn
  \else
    \@restonecolfalse
  \fi
  % --- Título del índice ---
  \chapter*{\vspace{-2.0cm}\begin{center}\Large{\textbf{ÍNDICE DE FIGURAS}}\end{center}}
  % --- Contenido del índice ---
  \@starttoc{lof}
  \if@restonecol\twocolumn\fi
  \cleardoublepage
}\end{spacing}
}

% --- Cabecera del índice ---
\addtocontents{lof}{\hfill{P\'ag.}\par}
\renewcommand\cftloftitlefont{\hfill\Large}
\renewcommand\cftafterloftitle{\hfill\mbox{}}

\renewcommand{\cftfigfont}{Figura~} 


% --- Configuración del caption ---
\captionsetup[figure]{%
  labelfont={bf,rm}, % Times New Roman
  textfont={rm},
  labelsep=space,
  name=Figura
}

% ========================
% ÍNDICE DE TABLAS
% ========================
\renewcommand\listoftables{
  \begin{spacing}{1}{
    \setlength{\parskip}{1pt}
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    % Título del índice (opcional)
    %\chapter*{\vspace{-2.0cm}\begin{center}\Large{\textbf{ÍNDICE DE TABLAS}}\end{center}
    %  \@mkboth{\MakeUppercase\listtablename}{\MakeUppercase\listtablename}}
    \@starttoc{lot}
    \if@restonecol\twocolumn\fi
    \cleardoublepage
  }\end{spacing}
}

% Encabezado de columnas del índice
\addtocontents{lot}{\hfill{P\'ag.}\par}

% Estilo visual del título
\renewcommand\cftlottitlefont{\hfill\Large}
\renewcommand\cftafterlottitle{\hfill\mbox{}}

\renewcommand{\cfttabfont}{Tabla~} 

% --- Configuración del caption ---
\captionsetup[table]{%
  labelfont={bf,rm}, % Times New Roman
  textfont={rm},
  labelsep=space,
  name=Tabla
}

% ====================================================================
% ÍNDICE DE ANEXOS
% ====================================================================
\newcommand\listofannexes{%
  \begin{spacing}{1.5}{ % Interlineado 1.5
    \setlength{\parskip}{1pt}
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    %\chapter*{\vspace{-2.0cm}\begin{center}\Large{\textbf{ÍNDICE DE ANEXOS}}\end{center}
     % \@mkboth{\MakeUppercase{ÍNDICE DE ANEXOS}}{\MakeUppercase{ÍNDICE DE ANEXOS}}}
    \@starttoc{loa} % <-- archivo auxiliar de anexos
    \if@restonecol\twocolumn\fi
    \cleardoublepage
  }\end{spacing}
}
\addtocontents{loa}{\hfill{P\'ag.}\par}



% ====================================================================
% For the chapter
\def\@makechapterhead#1{%
  %\vspace*{50\p@}%
  {\parindent \z@ \centering
    \normalfont
      \thispagestyle{empty}
    \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
      \if@mainmatter
        {\Large \bfseries \MakeUppercase{\@chapapp}~\Roman{chapter}\par}         %\par\nobreak
      \fi
    \fi
    %\interlinepenalty\@M
    {\Large \bfseries \MakeUppercase{#1}\par\nobreak}
    \vskip 40\p@
  }
}


\titleformat{\section}
  {\normalfont \bf}{\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont \bf}{\thesubsection}{1em}{}

\newcommand{\anexossection}{%
  \cleardoublepage
  \thispagestyle{empty}%
  \begin{center}
    \vspace*{\fill}
    {\Large \bfseries ANEXOS}
    \vspace*{\fill}
  \end{center}
  \clearpage
}

\newcounter{anexo}
\renewcommand{\theanexo}{\arabic{anexo}}

\newcommand{\anexo}[1]{%
  \refstepcounter{anexo}%
  \cleardoublepage
  \thispagestyle{plain}%
  % Agregar entrada al índice de anexos
  \addcontentsline{loa}{section}{Anexo \theanexo: #1}%
  \begin{center}
    {\Large \bfseries ANEXO \theanexo: #1}
  \end{center}
  \vspace{1cm}
}
