# Beispiele

Die folgenden Beispiele stammen aus der [Datenbank des Portals der schweizerischen Ortsnamenforschung](https://search.ortsnamen.ch/).

## Nossikon Sans

{:.nossikon}
*əm tu᪷rən ọbə, vọm rọ̄utətúrᵃᵉ*{:.char-display}  
*í᪷n̄dərlaχχə*{:.char-display}  
*[ivɛʀdɔ̃], [ɛ̃ vɛrˈdɔ̃]*{:style="font-style: normal"}{:.char-display}  
*\*podjo > \*püög̓́ > \*púog̓́ > \*púəg̓́*{:.char-display}  
*de Schoͤngoͤwe, apud Schongoͧwe*{:.char-display}  

## Nossikon Sans SemiCondensed

{:.nossikon-condensed}
*əm tu᪷rən ọbə, vọm rọ̄utətúrᵃᵉ*{:.char-display}  
*í᪷n̄dərlaχχə*{:.char-display}  
*[ivɛʀdɔ̃], [ɛ̃ vɛrˈdɔ̃]*{:style="font-style: normal"}{:.char-display}  
*\*podjo > \*püög̓́ > \*púog̓́ > \*púəg̓́*{:.char-display}  
*de Schoͤngoͤwe, apud Schongoͧwe*{:.char-display}  

## Nossikon Serif

{:.nossikon-serif}
*əm tu᪷rən ọbə, vọm rọ̄utətúrᵃᵉ*{:.char-display}  
*í᪷n̄dərlaχχə*{:.char-display}  
*[ivɛʀdɔ̃], [ɛ̃ vɛrˈdɔ̃]*{:style="font-style: normal"}{:.char-display}  
*\*podjo > \*püög̓́ > \*púog̓́ > \*púəg̓́*{:.char-display}  
*de Schoͤngoͤwe, apud Schongoͧwe*{:.char-display}  

## Gewichte und Breiten

<div class="axis-controls">
  <label>Familie <select id="family"><option>Nossikon Sans</option><option>Nossikon Serif</option></select></label>
  <label>Gewicht <input type="range" id="wght" min="100" max="900" value="400"> <output id="wght-value">400</output></label>
  <label>Breite <input type="range" id="wdth" min="62.5" max="100" step="0.5" value="100"> <output id="wdth-value">100</output> %</label>
  <label><input type="checkbox" id="ital"> kursiv</label>
</div>

<p class="nossikon char-display" id="axis-sample" contenteditable="true">əm tu᪷rən ọbə, vọm rọ̄utətúrᵃᵉ, de Schoͤngoͤwe</p>

<script>
  (function () {
    var sample = document.getElementById('axis-sample');
    var wght = document.getElementById('wght');
    var wdth = document.getElementById('wdth');
    var ital = document.getElementById('ital');
    var family = document.getElementById('family');
    function update() {
      sample.style.fontFamily = "'" + family.value + "'";
      sample.style.fontWeight = wght.value;
      sample.style.fontStretch = wdth.value + '%';
      sample.style.fontStyle = ital.checked ? 'italic' : 'normal';
      document.getElementById('wght-value').textContent = wght.value;
      document.getElementById('wdth-value').textContent = wdth.value;
    }
    [family, wght, wdth, ital].forEach(function (el) { el.addEventListener('input', update); });
    update();
  })();
</script>

{:.nossikon}
<span style="font-weight: 100">Thin</span> · <span style="font-weight: 200">ExtraLight</span> · <span style="font-weight: 300">Light</span> · <span style="font-weight: 400">Regular</span> · <span style="font-weight: 500">Medium</span> · <span style="font-weight: 600">SemiBold</span> · <span style="font-weight: 700">Bold</span> · <span style="font-weight: 800">ExtraBold</span> · <span style="font-weight: 900">Black</span>
