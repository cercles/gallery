<%inherit file="main.mako" />
<a href="#" name="scade"></a>
<h2 name="scade">Scade</h2>
${scade|n}
<a href="#" name="xml"></a>
<h2>XML</h2>
${xml|n}
<a href="#" name="b"></a>
<h2>B</h2>
% for name, bfile in b.items():
<h3>${name}</h3>
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
<h4>${k}</h4>
${v|n}
% endfor
% endfor
