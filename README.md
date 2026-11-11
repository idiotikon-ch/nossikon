# Nossikon

Unicode-Fonts mit phonetischen und historischen Zeichen für die schweizerische Ortsnamenforschung und die deutschsprachige Dialektologie (u.a. Unterstützung für Teuthonista), basierend auf [Noto](https://github.com/notofonts/latin-greek-cyrillic).

## Dokumentation

[idiotikon-ch.github.io/nossikon](https://idiotikon-ch.github.io/nossikon/)

## Build

Die Fonts *Nossikon Sans* und *Nossikon Serif* werden aus den Quellen von [Noto Sans und Noto Serif](https://github.com/notofonts/latin-greek-cyrillic) gebaut (Version in [`scripts/build.sh`](scripts/build.sh)). [`scripts/patch_noto.py`](scripts/patch_noto.py) fügt dabei in allen Mastern die Nossikon-Zeichen und -Ligaturen ein:

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
PATH=$PWD/venv/bin:$PATH scripts/build.sh
```

Das Skript legt die Variable Fonts in `fonts/` und `docs/assets/css/fonts/` ab. Die statischen Schnitte landen in `build/fonts/ttf/`.

## Release

```bash
scripts/release.sh v2.0
```

erzeugt aus dem letzten Build drei Pakete in `build/release/v2.0/`:

- `Nossikon-v2.0-static.zip`: alle statischen TrueType-Schnitte (für Programme ohne Variable-Font-Unterstützung)
- `Nossikon-v2.0-variable.zip`: die Variable Fonts als TrueType
- `Nossikon-v2.0-web.zip`: WOFF2-Webfonts, `nossikon.css` und `sample.html`

Diese Pakete werden auf GitHub an das Release angehängt, z.B. mit `gh release create v2.0 build/release/v2.0/*.zip`.

## Lizenz

Die Nossikon-Fonts basieren auf [Noto-Fonts](https://github.com/notofonts/latin-greek-cyrillic), die unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) veröffentlicht sind. Alle Nossikon-Fonts sind ebenfalls unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) verfügbar.
