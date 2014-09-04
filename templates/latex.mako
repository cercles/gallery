% for ex in exs:
\subsection{${quote_tex(ex.name)}}
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
