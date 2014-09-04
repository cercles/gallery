% for lbltable in labels:
\begin{tabular}{ll}
% for l, tests in lbltable:
\texttt{${quote_tex(l)}} & ${ ', '.join([quote_tex(t) + " (\\ref{" + section_name(t) + "})" for t in tests]) }
\\\

% endfor
\end{tabular}

% endfor

% for ex in exs:
\subsection{${quote_tex(ex.name)}}
\label{${section_name(ex.name)}}

% if ex.labels:
\'Etiquettes de tests:

\begin{itemize}
% for l in ex.labels:
\item \texttt{${quote_tex(l)}}
% endfor
\end{itemize}
% endif

\subsubsection{Scade}

${ex.scade}
\subsubsection{XML}

${ex.xml}
% if ex.b:
\subsubsection{B}

% for name, bfile in ex.b.items():
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
${quote_tex(name)} -- ${k}:

${v}
% endfor
% endfor
% endif
% endfor
