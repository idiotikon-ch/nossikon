# Zeichen-Mapping

## Mapping-Tabellen

Für die folgenden Fonts liegen [Mapping-Tabellen](https://github.com/idiotikon-ch/nossikon/tree/master/mappings) als *tab-separated values* (TSV) vor:

- *Adlikon* (Zürcher Namenbuch)
- *Andhausen* (phonetische, historische und indogermanische Zeichen; diverse Projekte)
- *DidotItal-GPSR15* (fichier Muret)
- *Nidwalda* (Nidwaldner Orts- und Flurnamen, Schwyzer Namenbuch, Zuger Ortsnamen)
- *PhoneticBERN* (Ortsnamenbuch des Kantons Bern)
- *TimesSDS_LNB* (Luzerner Namenbuch)
- *TimesSDSPhonetic* (Die Orts- und Flurnamen des Kantons Basel-Landschaft)

Die Tabellen enthalten in der ersten Spalte jeweils die dezimalen Codepoints des Ausgangsfonts und in den folgenden Spalten die entsprechende Codepoint-Sequenz in Nossikon ([NFD-normalisiert](https://unicode.org/reports/tr15/#Norm_Forms)). Hier ein paar Beispiele aus den Mappings für *Nidwalda*:

```
[Nidwalda]  [Nossikon]
305         105
8800        111  803
710         772
8721        117  815  776
216         del
57          null
```

Der Wert `del` bedeutet, dass das Zeichen ersatzlos gelöscht werden soll, `null` bezeichnet explizit nicht gemappte Zeichen (z.B. weil sie scheinbar unbenutzt sind).

## Skript für die Umwandlung

Unter [`scripts/`](https://github.com/idiotikon-ch/nossikon/tree/master/scripts) ist ein Python3-Skript `map.py` zu finden, das die Umkodierung von Text erleichtern soll:

```bash
$ scripts/map.py mappings/Adlikon.tsv < my_adlikon_file.txt
```

```bash
$ scripts/map.py --to-files mappings/Nidwalda.tsv \
      my_nidwalda_file1.txt my_nidwalda_file2.txt
$ ls
my_nidwalda_file1.txt         my_nidwalda_file2.txt
my_nidwalda_file1.txt.mapped  my_nidwalda_file2.txt.mapped
```
