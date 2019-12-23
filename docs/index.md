# Nossikon

Unicode-Fonts mit phonetischen und historischen Zeichen für die schweizerische Ortsnamenforschung, basierend auf [Noto](https://github.com/googlefonts/noto-fonts).

Aktuell sind zwei Variationen (*Sans*, *Sans SemiCondensed*) in drei Stilen (*Regular*, *Italic*, *Bold*) verfügbar.

{:.click-me}
[Beispiele](./samples.html)

## Ziele

- Kodierung aller Zeichen, die konventionell in der schweizerischen Ortsnamenforschung verwendet werden
- möglichst vollständige Abdeckung und Mappings von Zeichensätzen in bisher verwendeten Fonts
- (wo immer möglich) Kompatibilität mit dem aktuellen [Unicode-Standard](https://unicode.org/main.html)
- Benutzung als Webfont für die [Online-Datenbank](https://search.ortsnamen.ch/) des [Portals der schweizerischen Ortsnamenforschung](https://www.ortsnamen.ch/)

## Installation und Nutzung

Die aktuelle Version ist unter [Releases](https://github.com/idiotikon-ch/nossikon/releases) zum Download erhältlich. Für die lokale Verwendung sind TrueType-Fonts verfügbar, für die Verwendung auf Websites verschiedene Webfont-Formate, inkl. CSS-Stylesheet für den Import:

```css
@import url('nossikon.css');

.nossikon {
    font-family: 'Nossikon Sans';
}
```

oder Einbindung in HTML:

```html
<link rel="stylesheet" type="text/css" href="nossikon.css">

<span style="font-family: 'Nossikon Sans'">nó̤ſſsi᪷kχᵃᵉ</span>
```

Resultat:

> <span style="font-family: 'Nossikon Sans'">nó̤ſſsi᪷kχᵃᵉ</span>

## Unterstützte Zeichen

Zusätzlich zur umfangreichen Unicode-Abdeckung durch [Noto](https://github.com/googlefonts/noto-fonts) sind in Nossikon zusätzliche Zeichen und Ligaturen enthalten.

{:.click-me}
[mehr Informationen zum Zeichensatz](./charset.html)

## Umkodierung von Daten in anderen Fonts

Für zahlreiche (nicht Unicode-kompatible) Fonts aus regionalen Forschungsprojekten liegen [Mapping-Tabellen](https://github.com/idiotikon-ch/nossikon/tree/master/mappings) vor. In diesen ist jeweils notiert, welche Codepoints im Ursprungs-Font welcher Codepoint-Sequenz in Nossikon entspricht.

{:.click-me}
[mehr Informationen zum Zeichen-Mapping](./mapping.html)

## Lizenz

Die Nossikon-Fonts basieren auf [Noto-Fonts](https://github.com/googlefonts/noto-fonts), die unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) veröffentlicht sind. Alle Nossikon-Fonts sind ebenfalls unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) verfügbar.
