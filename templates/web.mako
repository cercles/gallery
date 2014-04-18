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
% for ex in exs:
<li><a href="#${ex['name']}">${ex['name']}</a>
<ul>
<li><a href="#${ex['name']}-scade">Scade</a></li>
<li><a href="#${ex['name']}-xml">XML</a></li>
<li><a href="#${ex['name']}-b">B</a></li>
</ul>
</li>
% endfor
</ul>
</div>
<div class="col-md-10">
% for ex in exs:
<a href="#" name="${ex['name']}"></a>
<h1>${ex['name']}</h1>
<a href="#" name="${ex['name']}-scade"></a>
<h2>Scade</h2>
${ex['scade']|n}
<a href="#" name="${ex['name']}-xml"></a>
<h2>XML</h2>
${ex['xml']|n}
<a href="#" name="${ex['name']}-b"></a>
<h2>B</h2>
% for name, bfile in ex['b'].items():
<h3>${name}</h3>
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
<h4>${k}</h4>
${v|n}
% endfor
% endfor
% endfor
</div>
</div>
</div>
</body>
</html>
