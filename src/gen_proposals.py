"""Genera proposals.json (las propuestas de decoración) a partir de layout.json (la distribución base).

Cada fila es [planta, tipo, x m, y m, giro, volteado(0/1, opcional)].
Las propuestas se montan por zonas de la casa (salón, cocina, porche...), cada una con su variante.
Los radiadores se copian de layout.json a todas las propuestas.

Uso (desde la raíz del repo):  python src/gen_proposals.py
"""
import json, os

here = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(here, 'layout.json'), encoding='utf8'))
RAD = ('rad', 'toallero')
rads = [r for r in base if r[1].startswith(RAD)]
furn = [r for r in base if not r[1].startswith(RAD)]


def zone(r):
    f, t, x, y = r[0], r[1], r[2], r[3]
    if f == 'sotano':
        return 'garaje'
    if f == 'baja':
        if y < 2.85: return 'porche'
        if y > 12.9: return 'patio'
        if y >= 9.3: return 'cocina'
        return 'dorm3' if (x >= 6.1 and y < 7.5) else 'salon'
    if y < 6.5: return 'dorm2' if x < 3.55 else 'dorm1'
    return 'principal'


def B(f):  # fila de planta baja / primera / sótano
    return lambda t, x, y, r=0, m=0: [f, t, x, y, r] + ([1] if m else [])

b, p, s = B('baja'), B('primera'), B('sotano')

# ---------------- variantes por zona ----------------
Z = {}

# --- salón (x 2,97–6,09 · y 3,15–9,22; el comedor va aparte) ---
Z['salon'] = {
 'chaise': [b('chaise', 3.8, 4.85, 270), b('tv150', 5.9, 4.9, 90), b('tv55', 5.9, 4.9, 90), b('alf160', 4.95, 4.85, 90), b('mcentroR', 5.15, 4.9),
            b('lampp', 3.5, 6.7), b('plantaG', 5.75, 3.4)],
 'minimal': [b('sofa4', 3.5, 4.9, 270), b('tvw65', 6.04, 4.9, 90), b('alf', 4.9, 4.9), b('mcentroR', 4.8, 4.9), b('plantaG', 5.75, 3.45),
             b('lampp', 3.5, 6.6), b('tripode', 5.7, 6.4)],
 'familia': [b('sofa4', 3.5, 4.8, 270), b('arm', 5.0, 6.15, 180), b('puf', 3.6, 6.5), b('tv240', 5.9, 4.8, 90), b('mcentro', 4.75, 4.8, 90),
             b('alf2', 4.7, 4.8, 90), b('plantaM', 5.75, 3.4), b('lampp', 4.3, 6.85)],
 'esquina': [b('sofaL2', 4.05, 4.75, 270), b('tv', 5.9, 4.6, 90), b('tv55', 5.9, 4.6, 90), b('mcentro2', 4.8, 4.9, 90), b('alf', 4.85, 4.9),
             b('plantaG', 5.75, 3.4), b('lampp', 3.6, 6.5), b('aparador', 5.9, 6.2, 90)],
}
# --- comedor ---
Z['comedor'] = {
 'c140': [b('mesa140', 4.4, 8.15), b('silla', 3.9, 7.5), b('silla', 4.9, 7.5), b('silla', 3.9, 8.8, 180), b('silla', 4.9, 8.8, 180), b('pend60', 4.4, 8.15)],
 'redonda': [b('mesaR120', 4.4, 8.05), b('silla', 4.4, 7.2), b('silla', 5.25, 8.05, 90), b('silla', 4.4, 8.9, 180), b('silla', 3.55, 8.05, 270), b('pend100', 4.4, 8.05)],
 'c200': [b('mesa200', 4.35, 8.15), b('silla', 3.65, 7.4), b('silla', 4.35, 7.4), b('silla', 5.05, 7.4), b('silla', 3.65, 8.9, 180), b('silla', 4.35, 8.9, 180),
          b('silla', 5.05, 8.9, 180), b('pendl', 4.35, 8.15)],
 'tu': [b('mesaC', 4.2, 8.2), b('silla', 3.8, 7.52), b('silla', 4.6, 7.52), b('silla', 3.8, 8.88, 180), b('silla', 4.6, 8.88, 180), b('pend100', 4.2, 8.2),
        b('aparador', 5.95, 8.2, 90)],
}
# --- cocina (x 2,97–5,85 · y 9,35–12,45; nevera y encimera en el muro oeste) ---
KIT = [b('nevera', 3.33, 9.68), b('enc', 3.35, 11.21, 270)]
Z['cocina'] = {
 'tu': KIT + [b('mcoc', 5.45, 11.36, 90), b('silla', 4.80, 11.06, 270), b('silla', 4.80, 11.62, 270), b('silla', 5.50, 10.52), b('silla', 5.54, 12.21, 180),
              b('cafet', 3.35, 10.4, 270), b('micro', 3.35, 11.9, 270), b('pend60', 5.45, 11.36)],
 'desayunador': KIT + [b('mcoc90', 4.95, 11.2, 90), b('silla', 4.3, 10.95, 270), b('silla', 4.3, 11.45, 270), b('silla', 5.6, 11.2, 90),
                       b('cafet', 3.35, 10.4, 270), b('tost', 3.35, 11.9, 270)],
 'isla': KIT + [b('isla', 4.8, 11.0, 90), b('taburete', 5.55, 10.4), b('taburete', 5.55, 11.0), b('taburete', 5.55, 11.6),
                b('pend40', 4.8, 10.5), b('pend40', 4.8, 11.5), b('micro', 3.35, 11.9, 270)],
 'peninsula': KIT + [b('pen', 4.7, 10.9, 90), b('taburete', 5.4, 10.3), b('taburete', 5.4, 10.9), b('taburete', 5.4, 11.5), b('cafet', 3.35, 10.4, 270),
                     b('freid', 3.35, 11.9, 270)],
 'minimal': KIT + [b('mcoc120', 4.95, 11.2, 90), b('silla', 4.15, 10.95, 270), b('silla', 4.15, 11.6, 270), b('silla', 4.95, 10.2), b('silla', 4.95, 12.2, 180),
                   b('cafet', 3.35, 10.4, 270)],
}
# --- porche (x 2,65–8,83 · y 0,15–2,85) ---
Z['porche'] = {
 'tu': [b('sofaJL', 7.49, 1.73, 180, 1), b('mcentro2', 7.14, 1.43), b('mesaJR', 4.0, 1.55), b('sillaJ', 4.0, 0.62), b('sillaJ', 3.15, 1.55, 270),
        b('sillaJ', 4.85, 1.55, 90), b('maceta', 5.7, 2.55), b('plantaG', 3.3, 2.5)],
 'trabajo': [b('mesaJ', 5.9, 1.45), b('silla', 5.4, 0.72), b('silla', 6.4, 0.72), b('silla', 5.4, 2.18, 180), b('silla', 6.4, 2.18, 180), b('portatil', 5.6, 1.3),
             b('plantaG', 3.2, 2.4), b('plantaM', 8.4, 2.4)],
 'minimal': [b('sofaJ', 6.2, 2.35, 180), b('mesaAux', 5.4, 1.5), b('mesaAux', 7.0, 1.5), b('plantaG', 3.2, 2.3), b('plantaG', 8.4, 0.7)],
 'familia': [b('mesaJ', 5.9, 1.45), b('silla', 5.4, 0.72), b('silla', 6.4, 0.72), b('silla', 5.4, 2.18, 180), b('silla', 6.4, 2.18, 180), b('alf', 5.9, 1.45),
             b('maceta', 3.0, 2.5), b('maceta', 8.5, 2.55), b('bici', 8.4, 1.3, 90)],
 'anfitriones': [b('mesaJ200', 4.6, 1.6), b('sillaJ', 3.9, 0.75), b('sillaJ', 4.6, 0.75), b('sillaJ', 5.3, 0.75), b('sillaJ', 3.9, 2.45, 180), b('sillaJ', 4.6, 2.45, 180),
                 b('sillaJ', 5.3, 2.45, 180), b('pendl', 4.6, 1.6), b('sofaJL', 7.49, 1.73, 180, 1), b('mcentro2', 7.14, 1.43), b('plantaG', 3.3, 2.45)],
}
# --- dormitorio 3 (x 6,2–8,83 · y 3,15–6,64) ---
Z['dorm3'] = {
 'oficina': [b('escrG', 7.4, 3.6), b('monD', 7.4, 3.5), b('teclado', 7.4, 3.8), b('flexo', 8.0, 3.4), b('sillaErg', 7.4, 4.5, 180), b('c90', 8.3, 5.6),
             b('arm100', 6.7, 6.3, 180), b('estante', 6.4, 4.9, 90)],
 'ninos': [b('litera', 8.3, 4.4), b('c80', 6.75, 4.4), b('escr100', 7.9, 6.35), b('sillaE', 7.9, 5.8), b('alf120', 7.55, 4.4), b('cesto', 6.5, 6.2)],
 'invitados': [b('c150', 7.5, 4.4), b('mesita', 6.45, 3.4), b('mesita', 8.55, 3.4), b('lampm', 6.45, 3.4), b('lampm', 8.55, 3.4), b('arm120', 8.1, 6.3, 180),
               b('plantaM', 6.5, 6.3)],
 'tu': [b('c135', 8.05, 4.2), b('mesita', 7.05, 3.3), b('lampm', 7.05, 3.3), b('arm200', 6.5, 4.8, 270)],
}
# --- patio (x 0,1–9 · y 12,9–20,4) ---
Z['patio'] = {
 'tu': [b('tumb', 1.0, 17.0), b('tumb', 2.4, 17.0), b('mesaAux', 1.7, 17.0), b('bbq', 7.9, 14.5), b('maceta', 0.6, 13.6), b('maceta', 8.5, 13.6), b('arbol', 3.0, 19.3)],
 'verde': [b('tumb', 1.2, 17.0), b('tumb', 2.2, 17.0), b('bbq', 7.9, 14.5), b('jardineraL', 4.5, 13.5), b('huerto', 7.7, 18.2), b('arbol', 3.0, 19.3),
           b('arbol', 8.0, 19.8), b('plantaG', 0.6, 13.6)],
 'minimal': [b('tumb', 1.3, 17.0), b('tumb', 2.3, 17.0), b('arbol', 3.2, 19.3), b('arbol', 7.6, 15.0), b('jardineraL', 1.2, 13.6)],
 'familia': [b('perg', 6.2, 16.6), b('mesaJ200', 6.2, 16.6), b('sillaJ', 5.5, 15.85), b('sillaJ', 6.2, 15.85), b('sillaJ', 6.9, 15.85), b('sillaJ', 5.5, 17.35, 180),
             b('sillaJ', 6.2, 17.35, 180), b('sillaJ', 6.9, 17.35, 180), b('bbq', 8.0, 14.4), b('huerto', 1.4, 14.2), b('huerto', 3.6, 14.2), b('arbol', 2.3, 18.6),
             b('cobertizo', 8.0, 19.2)],
 'anfitriones': [b('perg2', 5.0, 16.2), b('mesaJ200', 5.0, 16.2), b('sillaJ', 4.3, 15.45), b('sillaJ', 5.0, 15.45), b('sillaJ', 5.7, 15.45), b('sillaJ', 4.3, 16.95, 180),
                 b('sillaJ', 5.0, 16.95, 180), b('sillaJ', 5.7, 16.95, 180), b('pend100', 5.0, 16.2), b('bbq', 8.0, 14.4), b('tumb', 0.9, 17.5), b('tumb', 2.1, 17.5),
                 b('mesaAux', 1.5, 17.5), b('arbol', 1.5, 19.3), b('arbol', 8.0, 19.3), b('jardineraL', 7.5, 13.4), b('maceta', 0.6, 13.4)],
}
# --- planta primera ---
Z['dorm2'] = {
 'oficina': [p('escrG', 1.9, 3.45), p('monD', 1.9, 3.45), p('teclado', 1.9, 3.75), p('flexo', 2.5, 3.35), p('sillaErg', 2.0, 4.25, 180), p('libreria', 3.3, 4.9, 90),
             p('c80', 1.15, 5.0), p('plantaM', 3.2, 3.35)],
 'ninos': [p('c90', 1.15, 4.3), p('c90', 2.55, 4.3), p('mesita', 1.85, 3.25), p('lampm', 1.85, 3.25), p('alf120', 1.85, 5.2), p('arm150', 1.7, 6.2, 180)],
 'minimal': [p('c150', 2.05, 4.1), p('mesita', 1.0, 3.3), p('mesita', 3.1, 3.3), p('lampm', 1.0, 3.3), p('lampm', 3.1, 3.3), p('arm120', 1.9, 6.14, 180)],
 'tu': [p('c135', 1.65, 3.89, 270), p('mesita', 0.82, 4.85, 270), p('lampm', 0.82, 4.85), p('arm120', 1.35, 6.14, 180), p('escr', 3.25, 4.7, 90)],
}
Z['dorm1'] = {
 'tu': [p('c135', 5.47, 3.88, 90), p('mesita', 6.32, 4.85, 90), p('lampm', 6.32, 4.85), p('arm120', 5.7, 6.14, 180), p('escr', 3.95, 4.9, 270)],
 'juegos': [p('c90', 6.0, 4.3), p('escr', 4.3, 3.5), p('sillaE', 4.3, 4.2, 180), p('cesto', 3.9, 6.1), p('alf120', 5.0, 5.1), p('plantaM', 6.2, 6.2)],
 'minimal': [p('c150', 5.1, 4.1), p('mesita', 4.1, 3.3), p('mesita', 6.1, 3.3), p('lampm', 4.1, 3.3), p('lampm', 6.1, 3.3), p('arm120', 5.5, 6.14, 180)],
 'invitados': [p('c90', 4.4, 4.2), p('c90', 5.9, 4.2), p('mesita', 5.15, 3.25), p('lampm', 5.15, 3.25), p('arm120', 5.5, 6.14, 180), p('plantaM', 6.3, 6.2)],
}
Z['principal'] = {
 'tu': [p('c150', 1.68, 11.0, 270), p('mesita', 0.94, 10.0, 270), p('lampm', 0.94, 10.0), p('arm200', 2.2, 9.46), p('comoda', 3.65, 12.14, 180), p('plantaG', 4.3, 9.5)],
 'grande': [p('c160', 1.72, 11.0, 270), p('mesita', 1.15, 9.85, 270), p('lampm', 1.15, 9.85), p('arm150', 2.5, 9.46), p('tocador', 3.7, 12.14, 180),
            p('bpie', 2.98, 11.0, 270), p('alf120', 3.5, 11.0, 90), p('plantaG', 4.3, 9.6)],
 'familia': [p('c160', 1.72, 11.0, 270), p('mesita', 1.15, 9.85, 270), p('arm150', 2.5, 9.46), p('cuna', 4.1, 10.2), p('comoda120', 3.65, 12.14, 180), p('lampm', 1.15, 9.85)],
}
# --- garaje ---
Z['garaje'] = {
 'tu': [s('coche', 3.3, 3.2, 90), s('estG', 0.73, 2.5, 270), s('banco', 5.97, 2.5, 90), s('estG', 6.07, 4.8, 90)],
 'taller': [s('coche', 4.35, 3.3, 90), s('moto', 0.95, 2.0, 90), s('scooter', 0.95, 4.4, 90), s('estG', 6.13, 2.4, 90), s('banco', 2.3, 5.5, 0)],
 'familia': [s('cochep', 3.3, 3.0, 90), s('bici', 0.95, 3.0, 90), s('bici', 1.65, 3.0, 90), s('estG', 6.13, 2.3, 90), s('arcon', 6.0, 4.6, 90), s('trast', 2.0, 5.7)],
 'furgo': [s('furg', 3.3, 3.4, 90), s('moto', 1.0, 3.0, 90), s('bici', 1.75, 3.0, 90), s('estG', 6.13, 2.5, 90), s('banco', 6.0, 5.0, 90)],
}

# Las zonas que se dejan sin tocar copian la distribución base
def keep(zn):
    return [r for r in furn if zone(r) == zn]

# En la base, la zona "salón" incluye el comedor: se separan por tipo de mueble
SALON_BASE = [r for r in furn if zone(r) == 'salon']


LIV_BASE = [r for r in SALON_BASE if r[1] in ('sofa3', 'alf', 'mcentro', 'tv')]
DIN_BASE = [r for r in SALON_BASE if r[1] in ('mesaC', 'silla')]
ZONES = ['salon', 'comedor', 'cocina', 'porche', 'dorm3', 'patio', 'dorm2', 'dorm1', 'principal', 'garaje']
BASEZ = {'salon': LIV_BASE, 'comedor': DIN_BASE, 'cocina': keep('cocina'), 'porche': keep('porche'), 'dorm3': keep('dorm3'), 'patio': keep('patio'),
         'dorm2': keep('dorm2'), 'dorm1': keep('dorm1'), 'principal': keep('principal'), 'garaje': keep('garaje')}

PROPS = [
 ('Clásica', 'La distribución base: salón con sofá de 3 plazas y TV, comedor para 4, cocina con mesa, dormitorios dobles y garaje con coche.',
  {}),
 ('Tu porche y cocina', 'Tu porche con sofá en L y mesa de centro, y tu cocina con mesa de 110×70 y cuatro sillas. El resto, equilibrado y acogedor.',
  {'porche': 'tu', 'cocina': 'tu', 'salon': None, 'comedor': 'tu', 'dorm3': 'tu', 'patio': 'tu', 'dorm2': 'tu', 'dorm1': 'tu', 'principal': 'tu'}),
 ('Teletrabajo', 'Despachos en el dormitorio 3 y en el dormitorio 2 (con cama de invitados), chaise longue en el salón y cocina con desayunador.',
  {'salon': 'chaise', 'comedor': 'c140', 'cocina': 'desayunador', 'porche': 'trabajo', 'dorm3': 'oficina', 'dorm2': 'oficina', 'garaje': 'taller'}),
 ('Minimalista', 'Pocos muebles, líneas limpias, TV en la pared, mesa redonda y mucha planta. Dormitorios con camas de 150-160 y mesitas simétricas.',
  {'salon': 'minimal', 'comedor': 'redonda', 'cocina': 'minimal', 'porche': 'minimal', 'dorm3': 'invitados', 'patio': 'minimal',
   'dorm2': 'minimal', 'dorm1': 'minimal', 'principal': 'grande', 'garaje': 'taller'}),
 ('Familia con niños', 'Salón grande con TV de 240 y alfombra, mesa de 200 para seis, isla en la cocina, literas, cunas y un patio con huerto y pérgola.',
  {'salon': 'familia', 'comedor': 'c200', 'cocina': 'isla', 'porche': 'familia', 'dorm3': 'ninos', 'patio': 'familia',
   'dorm2': 'ninos', 'dorm1': 'juegos', 'principal': 'familia', 'garaje': 'familia'}),
 ('Anfitriones', 'Pensada para recibir: sofá en L en el salón, península con taburetes, mesa para seis en el porche, pérgola con barbacoa y habitaciones para invitados.',
  {'salon': 'esquina', 'comedor': 'redonda', 'cocina': 'peninsula', 'porche': 'anfitriones', 'dorm3': 'invitados', 'patio': 'anfitriones',
   'dorm2': 'tu', 'dorm1': 'invitados', 'principal': 'grande', 'garaje': 'furgo'}),
]

# En "Tu porche y cocina" el salón usa la base con algún complemento
EXTRAS = {
 1: [b('tv55', 5.9, 4.6, 90), b('lampp', 3.5, 6.5), b('plantaG', 5.75, 3.4)],
}

out = []
for i, (name, desc, sel) in enumerate(PROPS):
    rows = []
    for zn in ZONES:
        v = sel.get(zn, 'base' if i == 0 else None)
        if i == 0 or v is None or zn not in Z or v not in Z[zn]:
            rows += BASEZ[zn]
        else:
            rows += Z[zn][v]
    rows += EXTRAS.get(i, [])
    rows += rads
    out.append({'n': name, 'd': desc, 'items': rows})

json.dump(out, open(os.path.join(here, 'proposals.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('proposals.json:', len(out), 'propuestas;', ', '.join('%s=%d' % (o['n'], len(o['items'])) for o in out))
