# Erzeugt den Speisekarten-HTML-Block in index.html (zwischen den MENU-Markern).
# Preise: None = „Preis folgt“. Nur Preise, die auf den Bildschirm-Fotos lesbar sind.
import re, pathlib

CATS = [
    ("doener", "Döner & Dürüm"), ("teller", "Teller & Boxen"), ("falafel", "Falafel & Vegetarisch"),
    ("suppen", "Suppen"), ("burger", "Burger & Snacks"), ("pizza", "Pizza & Pide"),
    ("salate", "Salate"), ("kalt", "Getränke kalt"), ("heiss", "Getränke heiß"),
]

# (Nr, Name, Zusatzstoffe laut Karte, Preis, Kategorie)
ITEMS = [
    (1, "Drehspießfleisch im hausgemachten Brot", "8, 12", None, "doener"),
    (2, "Drehspießfleisch im hausgemachten Brot mit Käse", "8, 12", None, "doener"),
    (3, "Drehspießfleisch im hausgemachten Brot mit Pommes", "2, 8, 12", None, "doener"),
    (4, "Dürüm", "8, 12", None, "doener"),
    (5, "Dürüm mit Käse und Gemüse", "8, 12", None, "doener"),
    (6, "Falafel Dürüm", "eventuell 8", None, "falafel"),
    (7, "Falafel Sandwich (vegetarisch)", "eventuell 8", None, "falafel"),
    (8, "Lahmacun mit Salat", "8, 12", None, "pizza"),
    (9, "Lahmacun mit Drehspießfleisch", "8, 12", None, "pizza"),
    (10, "Drehspießfleischteller", "8, 12", None, "teller"),
    (11, "Falafel Teller", "eventuell 8", "10,00", "falafel"),
    (12, "Drehspießfleischbox mit Pommes", "2, 8, 12", "7,00", "teller"),
    (13, "Drehspießfleischbox mit Salat", "8, 12", "6,50", "teller"),
    (14, "Hähnchenschnitzel mit Pommes", "2, 8", None, "teller"),
    (15, "Hähnchenschnitzel mit Salat", "8", "9,00", "teller"),
    (16, "Currywurst mit Pommes", "2, 8, 12", "8,00", "burger"),
    (17, "Hamburger", "8, 12", None, "burger"),
    (18, "Cheeseburger", "8, 12", None, "burger"),
    (19, "Chickenburger", "8, 12", None, "burger"),
    (20, "Linsensuppe mit hausgemachtem Brot", "", None, "suppen"),
    (21, "Bohnensuppe mit hausgemachtem Brot", "", None, "suppen"),
    (22, "Drehspießfleischbox mit Reis", "8, 12", None, "teller"),
    (23, "Drehspießfleischteller mit Reis", "8, 12", None, "teller"),
    (24, "Bohnensuppe mit Reis und hausgemachtem Brot", "", None, "suppen"),
    (25, "Kuzi mit Bohnensuppe und Reis", "eventuell 8", None, "teller"),
    (26, "Halbes knuspriges Hähnchen", "8", None, "teller"),
    (27, "Knuspriges Hähnchen (Crispy-Chicken)", "2, 8", None, "teller"),
    (28, "Sac Tava", "je nach Rezept evtl. 8", None, "teller"),
    (29, "Pizza Margherita", "1, 8", None, "pizza"),
    (30, "Pizza Salami", "1, 8, 12", "9,50", "pizza"),
    (31, "Pizza Schinken", "1, 8, 12", "9,50", "pizza"),
    (32, "Pizza Funghi", "8", "9,00", "pizza"),
    (33, "Pizza Regina", "1, 8, 12", "10,00", "pizza"),
    (34, "Pizza Tonno", "1, 8", "10,50", "pizza"),
    (35, "Pizza mit frischem Gemüse", "8", "9,50", "pizza"),
    (36, "Pizza mit Drehspießfleisch", "1, 8, 12", "11,00", "pizza"),
    (37, "Familienpizza", "je nach Belag 1, 8, 12", "20,00", "pizza"),
    (38, "Calzone Pizza", "1, 8, 12", "9,50", "pizza"),
    (39, "Sucuk Pizza", "1, 8, 12", "10,00", "pizza"),
    (40, "Pide", "8", "6,00", "pizza"),
    (41, "Portion Pommes klein", "2", "3,00", "burger"),
    (42, "Portion Pommes groß", "2", "4,00", "burger"),
    (43, "Hot Dog", "1, 8, 12", "3,50", "burger"),
    (44, "Chicken Wings", "2, 8", "5,50", "burger"),
    (45, "Salat mit Drehspießfleisch", "8, 12", "6,00", "salate"),
    (46, "Salat mit Käse", "keine / evtl. 8", "4,50", "salate"),
    (47, "Fitness Salat", "keine", "7,50", "salate"),
    (48, "Cheese Box", "2, 8", "7,50", "teller"),
    (49, "Cola", "11", None, "kalt"),
    (50, "Cola Zero", "5, 6, 7, 11", None, "kalt"),
    (51, "Mezzo Mix", "10, 11", None, "kalt"),
    (52, "Fanta", "11", None, "kalt"),
    (53, "Sprite", "evtl. Farbstoff 2", None, "kalt"),
    (54, "Ayran", "keine Zusatzstoffe", None, "kalt"),
    (55, "Uludag", "Farbstoff 2, evtl. 11", None, "kalt"),
    (56, "Red Bull", "11", None, "kalt"),
    (57, "Wasser", "keine", None, "kalt"),
    (58, "Tee", "keine", None, "heiss"),
    (59, "Kaffee", "11", None, "heiss"),
    (60, "Cappuccino", "11", None, "heiss"),
    (61, "Latte Macchiato", "11", None, "heiss"),
    (62, "Espresso", "11", None, "heiss"),
]
assert [i[0] for i in ITEMS] == list(range(1, 63))

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")

out = ['<div class="menu-tabs" role="tablist" aria-label="Kategorien">',
       '  <button class="menu-tab is-active" role="tab" aria-selected="true" data-filter="all">Alle</button>']
for key, label in CATS:
    out.append(f'  <button class="menu-tab" role="tab" aria-selected="false" data-filter="{key}">{esc(label)}</button>')
out.append('</div>')
out.append('<div class="menu-groups">')
for key, label in CATS:
    items = sorted((i for i in ITEMS if i[4] == key), key=lambda i: i[0])
    out.append(f'  <section class="menu-group reveal" data-cat="{key}" aria-labelledby="mg-{key}">')
    out.append(f'    <h3 class="menu-group__title" id="mg-{key}">{esc(label)}</h3>')
    out.append('    <ul class="menu-list">')
    for nr, name, add, price, _ in items:
        addh = f' <sup class="add" title="Zusatzstoffe: {esc(add)}">({esc(add)})</sup>' if add else ""
        ph = (f'<span class="price">{price}&nbsp;€</span>' if price
              else '<span class="price price--tbd" data-placeholder="preis">Preis folgt</span>')
        out.append(f'      <li class="menu-item"><span class="nr">{nr}</span>'
                   f'<span class="name">{esc(name)}{addh}</span>'
                   f'<span class="dots" aria-hidden="true"></span>{ph}</li>')
    out.append('    </ul>')
    out.append('  </section>')
out.append('</div>')

p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
html = p.read_text(encoding="utf-8")
block = "\n".join("        " + l for l in out)
html, n = re.subn(r"(<!-- MENU:START -->).*?(\n[ \t]*<!-- MENU:END -->)", lambda m: m.group(1) + "\n" + block + m.group(2), html, flags=re.S)
assert n == 1, "MENU-Marker nicht gefunden"
p.write_text(html, encoding="utf-8")
print("ok", sum(1 for i in ITEMS if i[3] is None), "ohne Preis")
