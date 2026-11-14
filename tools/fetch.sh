#!/bin/sh
# Uso: tools/fetch.sh TRT-XXXX NIVEL  -> baja guía (json+md) y zip a material/nivel-N/
set -e
CODE="$1"; N="$2"; API=https://api.tertulia.ai
OUT="material/nivel-$N"; mkdir -p "$OUT/archivos"
curl -sf -H "X-Team-Code: $CODE" "$API/material/$N/guia" -o "$OUT/guia.json"
curl -sf -m 300 -H "X-Team-Code: $CODE" "$API/material/$N/zip" -o "$OUT/archivos.zip"
unzip -oq "$OUT/archivos.zip" -d "$OUT/archivos"
python3 -I - "$OUT/guia.json" > "$OUT/guia.md" <<'PY'
import json,sys
g=json.load(open(sys.argv[1]))
print(f"# {g.get('titulo')}\n\n**Misión:** {g.get('mision')}\n\n**Qué reciben:** {g.get('material')}\n")
print("**Qué suben al repo:**"); [print(f"- `{e}`") for e in g.get('entrega',[])]
print(f"\n**Qué revisa el juez:** {g.get('evalua')}\n\n## Enunciado\n\n{g.get('enunciado')}\n")
for l in g.get('lecturas',[]): print(f"\n## Lectura: {l['titulo']} ({l['archivo']})\n\n{l['texto']}\n")
PY
echo "== $OUT"; find "$OUT/archivos" -type f | head -50
