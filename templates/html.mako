<html>
<head>
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<link rel="stylesheet" href="pygments.css">
</head>
<body>

<nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <div class="container">
    <div class="collapse navbar-collapse">
    <a class="navbar-brand" href="#">Scade2B</a>
    <ul class="nav navbar-nav">
% for ex in exs:
    <li><a href="#${ex.name}">${ex.name}</a></li>
% endfor
    </ul>
    </div>
    </div>
</nav>

<div class="container" style="padding-top:20px">
% for ex in exs:
    <hr />
    <a href="#" name="${ex.name}"></a>
    <h1>${ex.name}</h1>
    <div class="row">
    <div class="col-md-8">
        <a href="#" name="${ex.name}-scade"></a>
        <h2>Scade</h2>
        ${ex.scade}
        <a href="#" name="${ex.name}-xml"></a>
        <h2>XML</h2>
        ${ex.xml}
    </div>
    <div class="col-md-4">
        <a href="#" name="${ex.name}-b"></a>
        <h2>B</h2>
% for name, bfile in ex.b.items():
        <h3>${name}</h3>
% for k, v in sorted(bfile.items(), key=lambda t: t[0]):
        <h4>${k}</h4>
        ${v}
% endfor
% endfor
    </div>
    </div>
% endfor
</div>
</body>
</html>
