import json
from pathlib import Path

with Path("../data/pokemon.json").open() as f:
    data = json.load(f)

ids = [
    i["speciesId"] for i in data
    if i["released"]
]
space_dash_names = [
    "bulu",  # Tapu Bulu
    "koko",  # Tapu Koko
    "fini",  # Tapu Fini
    "lele",  # Tapu Lele
    'jr',    # Mime Jr
    'mime',  # Mr. Mime
    "rime",  # Mr. Rime
    'oh',    # ho-oh
    'o',     # Jangmo-o, Hakamo-o, Kommo-o
    'z',     # Porygon-z
]

forms = set()
for i in ids:
    splt = i.split("_")
    
    if len(splt) <= 1:
        continue

    splt = [s for s in splt[1:] if s not in space_dash_names]
    if not splt:
        continue

    n = "_".join(splt)
    forms.add(n)
    

print(forms)
print(len(forms))