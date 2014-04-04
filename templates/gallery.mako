<html>
<head>
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<link rel="stylesheet" href="pygments.css">
</head>
<body>
<div class="container">
<h2>Scade</h2>
${scade|n}
<h2>XML</h2>
${xml|n}
<h2>B</h2>
% for name, bfile in b.items():
<h3>${name}</h3>
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
<h4>${k}</h4>
${v|n}
% endfor
% endfor
</div>
</body>
</html>
