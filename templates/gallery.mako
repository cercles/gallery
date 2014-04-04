<html>
<head>
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<link rel="stylesheet" href="pygments.css">
</head>
<body>
<div class="container">
<div class="row">
<div class="col-md-2">
<ul class="nav" style="position: fixed">
<li><a href="#scade">Scade</a></li>
<li><a href="#xml">XML</a></li>
<li><a href="#b">B</a></li>
</ul>
</div>
<div class="col-md-10">
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
</div>
</div>
</div>
</body>
</html>
