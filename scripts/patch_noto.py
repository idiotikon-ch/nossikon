#!/usr/bin/env python3

import argparse
import math
from collections import defaultdict
from dataclasses import dataclass, field

import ufoLib2
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.misc.transform import Transform
from ufoLib2.objects import Anchor, Component, Contour, Point


COPYRIGHT = (
    'Original: Copyright 2022 The Noto Project Authors '
    '(https://github.com/notofonts/latin-greek-cyrillic)\n'
    'Modifications: Copyright 2024 Schweizerisches Idiotikon.'
)

COMBINING_LETTERS = [
    'acomb', 'ecomb', 'icomb', 'ocomb', 'ucomb', 'ccomb', 'dcomb',
    'hcomb', 'mcomb', 'rcomb', 'tcomb', 'vcomb', 'xcomb',
]

# Nossikon uses the combining letters U+0363-036F of a heavier weight
# (Regular -> Bold, Bold -> ExtraBold); keys and values are design
# coordinates of the weight axis.
COMBINING_LETTER_WEIGHTS = {
    'Nossikon Sans': {26: 44, 90: 151, 151: 169, 190: 190},
    'Nossikon Serif': {28: 45, 94: 152, 152: 175, 194: 194},
}

MOD_LIGATURES = [
    ('uni1D43_uni0308', 'amod', 'dieresiscomb', 'top'),
    ('uni1D52_uni0308', 'omod', 'dieresiscomb', 'top'),
    ('uni1D58_uni0308', 'umod', 'dieresiscomb', 'top'),
    ('uni1D58_uni032F', 'umod', 'breveinvertedbelowcomb', 'bottom'),
    ('uni2071_uni032F', 'imod', 'breveinvertedbelowcomb', 'bottom'),
]

LIGATURES = [
    ('j tildeoverlaycomb', 'j_uni0334'),
    ('dotaccentcomb dotaccentcomb', 'uni0307_uni0307'),
    ('commaabovecomb acutecomb', 'uni0313_acutecomb'),
    ('amod dieresiscomb', 'uni1D43_uni0308'),
    ('amod emod', 'uni1D43_uni1D49'),
    ('omod dieresiscomb', 'uni1D52_uni0308'),
    ('umod breveinvertedbelowcomb', 'uni1D58_uni032F'),
    ('umod dieresiscomb', 'uni1D58_uni0308'),
    ('imod breveinvertedbelowcomb', 'uni2071_uni032F'),
]

CATEGORIES = {
    'uniECAC': 'base',
    'uni1D43_uni1D49': 'base',
    'j_uni0334': 'base',
    'uni0313_acutecomb': 'mark',
    'uni0307_uni0307': 'mark',
    **{name: 'base' for name, *_ in MOD_LIGATURES},
}


@dataclass
class Shape:
    contours: list = field(default_factory=list)
    anchors: dict = field(default_factory=dict)
    width: float = 0

    def transformed(self, t):
        return Shape(
            [[(*t.transformPoint((x, y)), typ, smooth)
              for x, y, typ, smooth in c] for c in self.contours],
            {n: t.transformPoint(p) for n, p in self.anchors.items()},
            self.width,
        )

    def bounds(self):
        pts = [(x, y) for c in self.contours for x, y, *_ in c]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)


def lerp(a, b, t):
    return a + (b - a) * t


def interpolate(s1, s2, t):
    if len(s1.contours) != len(s2.contours) or any(
            len(c1) != len(c2) for c1, c2 in zip(s1.contours, s2.contours)):
        raise ValueError('incompatible shapes')
    contours = [
        [(lerp(x1, x2, t), lerp(y1, y2, t), typ, smooth)
         for (x1, y1, typ, smooth), (x2, y2, *_) in zip(c1, c2)]
        for c1, c2 in zip(s1.contours, s2.contours)
    ]
    anchors = {
        n: (lerp(p[0], s2.anchors[n][0], t), lerp(p[1], s2.anchors[n][1], t))
        for n, p in s1.anchors.items() if n in s2.anchors
    }
    return Shape(contours, anchors, lerp(s1.width, s2.width, t))


class WidthGroup:
    """All sources (masters and sparse layers) sharing one width value."""

    def __init__(self, sources, xheights):
        self.sources = sorted(sources, key=lambda s: s[0])
        self.xheights = sorted(xheights)
        self.cache = {}

    def xheight(self, weight):
        for (w1, x1), (w2, x2) in zip(self.xheights, self.xheights[1:]):
            if w1 <= weight <= w2:
                return lerp(x1, x2, (weight - w1) / (w2 - w1))

    def layers_with(self, name):
        return [(w, layer) for w, layer in self.sources if name in layer]

    def shape(self, name, weight):
        key = (name, weight)
        if key not in self.cache:
            self.cache[key] = self._shape(name, weight)
        return self.cache[key]

    def _shape(self, name, weight):
        layers = self.layers_with(name)
        for w, layer in layers:
            if w == weight:
                return self.decompose(layer[name], w)
        lower = [(w, l) for w, l in layers if w < weight]
        upper = [(w, l) for w, l in layers if w > weight]
        (w1, l1), (w2, l2) = lower[-1], upper[0]
        return interpolate(self.decompose(l1[name], w1),
                           self.decompose(l2[name], w2),
                           (weight - w1) / (w2 - w1))

    def decompose(self, glyph, weight):
        shape = Shape(
            [[(p.x, p.y, p.type, p.smooth) for p in c] for c in glyph.contours],
            {a.name: (a.x, a.y) for a in glyph.anchors},
            glyph.width,
        )
        for comp in glyph.components:
            sub = self.shape(comp.baseGlyph, weight).transformed(
                Transform(*comp.transformation))
            shape.contours.extend(sub.contours)
        return shape


def set_glyph(layer, name, width, contours=(), components=(), anchors=None):
    glyph = layer[name] if name in layer else layer.newGlyph(name)
    glyph.clear()
    glyph.width = round(width)
    for c in contours:
        glyph.contours.append(Contour(points=[
            Point(round(x), round(y), typ, smooth) for x, y, typ, smooth in c]))
    for base, t in components:
        glyph.components.append(Component(
            base, Transform(t[0], t[1], t[2], t[3], round(t[4]), round(t[5]))))
    for n, (x, y) in (anchors or {}).items():
        glyph.anchors.append(Anchor(round(x), round(y), n))


def build_glyphs(group, weight, slant, cmap, letter_weights):
    s = lambda n: group.shape(n, weight)
    glyphs = []

    def add(name, width, **kwargs):
        glyphs.append((name, width, kwargs))

    for name in COMBINING_LETTERS:
        target = letter_weights[weight]
        heavier = s(name) if target == weight else group.shape(name, target)
        anchors = dict(heavier.anchors)
        if 'top' not in anchors:
            x, y = anchors['_top']
            top = heavier.bounds()[3]
            anchors['top'] = (x + (top - y) * slant, top)
        add(name, 0, contours=heavier.contours, anchors=anchors)

    o, u = s('o'), s('u')
    gap = (o.width - o.bounds()[2]) + u.bounds()[0]
    dx = o.width - round(0.4 * gap)
    anchors = {n: ((p[0] + u.anchors[n][0] + dx) / 2,
                   (p[1] + u.anchors[n][1]) / 2)
               for n, p in o.anchors.items() if n in u.anchors}
    if 'topright' in u.anchors:
        x, y = u.anchors['topright']
        anchors['topright'] = (x + dx, y)
    add('uniECAC', dx + u.width,
              components=[('o', (1, 0, 0, 1, 0, 0)), ('u', (1, 0, 0, 1, dx, 0))],
              anchors=anchors)

    aemod = cmap[0x10783]
    add('uni1D43_uni1D49', s(aemod).width,
              components=[(aemod, (1, 0, 0, 1, 0, 0))],
              anchors=s(aemod).anchors)

    for name, mod, mark, anchor in MOD_LIGATURES:
        letter_comp = next(l[mod].components[0] for _, l in group.sources
                           if mod in l and l[mod].components)
        t = Transform(*letter_comp.transformation)
        letter, m, modshape = s(letter_comp.baseGlyph), s(mark), s(mod)
        lx, ly = letter.anchors[anchor]
        mx, my = m.anchors['_' + anchor]
        ox, oy = t.transformPoint((lx - mx, ly - my))
        mark_t = (t.xx, 0, 0, t.yy, ox, oy)
        anchors = dict(modshape.anchors)
        if anchor in m.anchors:
            ax, ay = m.anchors[anchor]
            anchors[anchor] = (t.xx * ax + ox, t.yy * ay + oy)
        add(name, modshape.width,
                  components=[(mod, (1, 0, 0, 1, 0, 0)), (mark, mark_t)],
                  anchors=anchors)

    psilioxia, acute = s(cmap[0x1FCE]), s('acutecomb')
    pb, ab = psilioxia.bounds(), acute.bounds()
    add('uni0313_acutecomb', 0,
              components=[(cmap[0x1FCE], (1, 0, 0, 1, ab[0] - pb[0], ab[1] - pb[1]))],
              anchors=acute.anchors)

    j, tilde = s('j'), s('tildeoverlaycomb')
    yc = 0.49 * group.xheight(weight)
    jx, jy = j.anchors['top']
    tx, ty = tilde.anchors['_center']
    stem_x = jx - (jy - yc) * slant
    add('j_uni0334', j.width,
              components=[('j', (1, 0, 0, 1, 0, 0)),
                          ('tildeoverlaycomb', (1, 0, 0, 1, stem_x - tx, yc - ty))],
              anchors=j.anchors)

    dieresis = s('dieresiscomb')
    left, right = sorted(dieresis.contours, key=lambda c: min(p[0] for p in c))
    raise_by = 120
    shift = lambda c, dx, dy: [(x + dx, y + dy, typ, sm) for x, y, typ, sm in c]
    anchors = {'_top': dieresis.anchors['_top']}
    x, y = dieresis.anchors['top']
    anchors['top'] = (x + raise_by * slant, y + raise_by)
    add('uni0307_uni0307', 0,
              contours=[shift(left, 10, 0),
                        shift(right, -10 + raise_by * slant, raise_by)],
              anchors=anchors)
    return glyphs


def patch_designspace(path):
    doc = DesignSpaceDocument.fromfile(path)
    fonts = {}
    groups = defaultdict(list)
    for src in doc.sources:
        font = fonts.setdefault(src.path, ufoLib2.Font.open(src.path))
        layer = font.layers[src.layerName] if src.layerName else font.layers.defaultLayer
        groups[src.location['Width']].append((src.location['Weight'], layer, font))

    pending = []
    for members in groups.values():
        group = WidthGroup(
            [(w, l) for w, l, _ in members],
            [(w, f.info.xHeight) for w, l, f in members
             if l is f.layers.defaultLayer])
        for weight, layer, font in members:
            slant = math.tan(math.radians(-(font.info.italicAngle or 0)))
            cmap = {u: g.name for g in font for u in g.unicodes}
            letter_weights = COMBINING_LETTER_WEIGHTS[font.info.familyName]
            pending.append((layer, build_glyphs(group, weight, slant, cmap,
                                                letter_weights)))

    for layer, glyphs in pending:
        for name, width, kwargs in glyphs:
            set_glyph(layer, name, width, **kwargs)

    for font in fonts.values():
        patch_font(font)
        font.save(overwrite=True)


def patch_font(font):
    font.info.copyright = COPYRIGHT
    font['uniECAC'].unicodes = [0xECAC]

    order = font.lib.setdefault('public.glyphOrder', [])
    for name in ['uniECAC', 'uni1D43_uni1D49', 'j_uni0334', 'uni0307_uni0307',
                 'uni0313_acutecomb'] + [n for n, *_ in MOD_LIGATURES]:
        if name not in order:
            order.append(name)
    font.lib.setdefault('public.openTypeCategories', {}).update(CATEGORIES)

    rules = '\n'.join(f'    sub {seq} by {lig};' for seq, lig in LIGATURES)
    marker = '# Nossikon ligatures'
    if marker not in font.features.text:
        font.features.text += (
            f'\n{marker}\nlookup NossikonLigatures {{\n{rules}\n}} NossikonLigatures;\n'
            'feature liga {\n    lookup NossikonLigatures;\n} liga;\n')


def main():
    parser = argparse.ArgumentParser(
        description='apply the Nossikon modifications to Noto UFO sources')
    parser.add_argument('designspaces', nargs='+')
    for path in parser.parse_args().designspaces:
        patch_designspace(path)


if __name__ == '__main__':
    main()
