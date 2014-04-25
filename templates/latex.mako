\documentclass[a4paper]{report}

\usepackage{a4wide}
\usepackage{fancyvrb}
\usepackage{color}
\usepackage{underscore}

\input{style.tex}

\begin{document}
% for ex in exs:
\chapter{${ex.name}}
\section{Scade}

${ex.scade}
\section{XML}

${ex.xml}
\section{B}

% for name, bfile in ex.b.items():
\subsection{${name}}

% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
\subsubsection{${k}}

${v}
% endfor
% endfor
% endfor
\end{document}
