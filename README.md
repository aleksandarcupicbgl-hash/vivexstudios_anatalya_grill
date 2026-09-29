# Antalya Grill – One-Page-Website

Statische Seite ohne Build-Schritt: `index.html` im Browser öffnen oder den Ordner auf einen beliebigen Webspace hochladen.

```
index.html              Seite (alle Sektionen)
assets/css/styles.css   Design (mobile first)
assets/js/main.js       Intro, Navigation, Scroll-Effekte, Speisekarten-Filter
assets/img/             komprimierte WebP-Bilder (+ freigestelltes Logo)
tools/menu.py           Quelle der Speisekarte (Namen, Zusatzstoffe, Preise)
```

## Speisekarte / Preise ändern

Preise und Gerichte stehen in `tools/menu.py` (`None` = „Preis folgt“). Nach einer Änderung:

```
python3 tools/menu.py
```

Das schreibt den Speisekarten-Block in `index.html` neu (zwischen `<!-- MENU:START -->` und `<!-- MENU:END -->`).

## Platzhalter

Alle Platzhalter sind im HTML mit `<!-- PLATZHALTER -->` kommentiert und tragen ein `data-placeholder`-Attribut
(`grep -n PLATZHALTER index.html`). Auf der Seite sind sie gelb gestreift markiert (Klasse `ph`) – nach dem Ausfüllen die Klasse `ph` entfernen.

| Was | Wo |
|---|---|
| Straße, PLZ, Ort (Hausnr. 23 ist gesetzt) | Kontakt, Footer, JSON-LD im `<head>` |
| Telefonnummer | Nav-Button „Anrufen“, Kontakt, Footer, JSON-LD |
| Öffnungszeiten (Mo–So) | Kontakt |
| Google-Maps-Einbettung (`<iframe>`) + Link „Route planen“ | Kontakt |
| Direkter Link zum Google-Eintrag | Button „Alle Bewertungen auf Google“ |
| 3. Bewertungstext (Englisch, wörtlich) – 2 von 3 sind eingetragen | Bewertungen |
| Impressum- und Datenschutz-Seiten/Links | Footer |
| Domain für `canonical` | `<head>` |
