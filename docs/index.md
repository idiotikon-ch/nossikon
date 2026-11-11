# Nossikon

Unicode-Fonts mit phonetischen und historischen Zeichen für die schweizerische Ortsnamenforschung und die deutschsprachige Dialektologie, basierend auf [Noto](https://github.com/notofonts/latin-greek-cyrillic).

*Nossikon Sans* und *Nossikon Serif* sind als Variable Fonts verfügbar: stufenlos in allen Gewichten (100–900) und Breiten (62.5–100 %), jeweils aufrecht und kursiv.

{:.click-me}
[Beispiele](./samples.html)

## Ziele

- Kodierung aller Zeichen, die konventionell in der schweizerischen Ortsnamenforschung verwendet werden (u.a. Unterstützung für Teuthonista)
- möglichst vollständige Abdeckung und Mappings von Zeichensätzen in bisher verwendeten Fonts
- (wo immer möglich) Kompatibilität mit dem aktuellen [Unicode-Standard](https://unicode.org/main.html)
- Benutzung als Webfont für die [Online-Datenbank](https://search.ortsnamen.ch/) des [Portals der schweizerischen Ortsnamenforschung](https://www.ortsnamen.ch/)

## Installation und Nutzung

Die aktuelle Version ist unter [Releases](https://github.com/idiotikon-ch/nossikon/releases) zum Download erhältlich.

{:.click-me}
[Download](https://github.com/idiotikon-ch/nossikon/releases)

Für die lokale Verwendung gibt es die Variable Fonts als TrueType-Datei sowie ein Paket mit statischen TrueType-Fonts aller Gewichte und Breiten (für Programme, die Variable Fonts nicht oder nur eingeschränkt unterstützen). Für die Verwendung auf Websites gibt es WOFF2-Webfonts inkl. CSS-Stylesheet für den Import:

```css
@import url('nossikon.css');

.nossikon {
    font-family: 'Nossikon Sans';
}

.nossikon-semibold-condensed {
    font-family: 'Nossikon Sans';
    font-weight: 600;
    font-stretch: 87.5%;
}

.nossikon-serif {
    font-family: 'Nossikon Serif';
}
```

Gewicht und Breite lassen sich über `font-weight` (100–900) und `font-stretch` (62.5 %–100 %) beliebig einstellen. Die bisherige Familie `'Nossikon Sans SemiCondensed'` ist im Stylesheet weiterhin definiert und entspricht `'Nossikon Sans'` mit `font-stretch: 87.5%`.

oder Einbindung in HTML:

```html
<link rel="stylesheet" type="text/css" href="nossikon.css">

<span style="font-family: 'Nossikon Sans'">nó̤ſſsi᪷kχᵃᵉ</span>
```

Resultat:

> <span style="font-family: 'Nossikon Sans'">nó̤ſſsi᪷kχᵃᵉ</span>  
> <span style="font-family: 'Nossikon Serif'">nó̤ſſsi᪷kχᵃᵉ</span>

## Unterstützte Zeichen

Zusätzlich zur umfangreichen Unicode-Abdeckung durch [Noto](https://github.com/notofonts/latin-greek-cyrillic) sind in Nossikon zusätzliche Zeichen und Ligaturen enthalten.

{:.click-me}
[mehr Informationen zum Zeichensatz](./charset.html)

## Umkodierung von Daten in anderen Fonts

Für zahlreiche (nicht Unicode-kompatible) Fonts aus regionalen Forschungsprojekten liegen [Mapping-Tabellen](https://github.com/idiotikon-ch/nossikon/tree/master/mappings) vor. In diesen ist jeweils notiert, welche Codepoints im Ursprungs-Font welcher Codepoint-Sequenz in Nossikon entspricht.

{:.click-me}
[mehr Informationen zum Zeichen-Mapping](./mapping.html)

## Lizenz

Die Nossikon-Fonts basieren auf [Noto-Fonts](https://github.com/notofonts/latin-greek-cyrillic), die unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) veröffentlicht sind. Alle Nossikon-Fonts sind ebenfalls unter der [SIL Open Font License (OFL) v1.1](http://scripts.sil.org/OFL) verfügbar.
