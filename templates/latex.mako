% for ex in exs:
\subsection{${ex.name}}
\subsubsection{Scade}

${ex.scade}
\subsubsection{XML}

${ex.xml}
\subsubsection{B}

% for name, bfile in ex.b.items():
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
${name} -- ${k}:

${v}
% endfor
% endfor
% endfor
