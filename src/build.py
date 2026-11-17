"""Genera ../index.html a partir de tpl.html, las máscaras de muros y la distribución inicial.

Uso (desde la raíz del repo):  python src/build.py
Solo usa la biblioteca estándar de Python.
"""
import base64, json, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)

s = open(os.path.join(here, 'tpl.html'), encoding='utf8').read()
for f in ('sotano', 'baja', 'primera'):
    b = base64.b64encode(open(os.path.join(here, f + '_mask.png'), 'rb').read()).decode()
    s = s.replace('__MASK_' + f + '__', 'data:image/png;base64,' + b)
s = s.replace('__LAYOUT__', open(os.path.join(here, 'layout.json'), encoding='utf8').read())
s = s.replace('__FAVICON__', 'data:image/png;base64,' + base64.b64encode(open(os.path.join(here, 'favicon.png'), 'rb').read()).decode())

# La plantilla trae solo el contenido; aquí se envuelve en un documento completo
i = s.index('<div class="app">')
head = s[:i].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
out = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       '<style>:root{color-scheme:light}[hidden]{display:none!important}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}</style>\n'
       + head + '</head>\n<body>\n' + s[i:] + '</body>\n</html>\n')
open(os.path.join(root, 'index.html'), 'w', encoding='utf8', newline='\n').write(out)
print('index.html generado,', len(out), 'caracteres')
