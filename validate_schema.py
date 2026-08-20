"""
Validar el schema JSON de aylesva-recursos.liquid para asegurar que no tenga errores de sintaxis.
"""
import json

file_path = "theme/sections/aylesva-recursos.liquid"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extraer el bloque del schema
start_tag = "{% schema %}"
end_tag = "{% endschema %}"

start_idx = content.find(start_tag)
end_idx = content.find(end_tag)

if start_idx != -1 and end_idx != -1:
    schema_text = content[start_idx + len(start_tag) : end_idx].strip()
    try:
        schema_json = json.loads(schema_text)
        print("✅ Schema JSON es 100% VÁLIDO.")
    except Exception as e:
        print("❌ Error de sintaxis en el Schema JSON:")
        print(e)
        # Mostrar el error exacto
        lines = schema_text.split("\n")
        print("\n".join(lines[:20])) # Mostrar primeras lineas
else:
    print("❌ No se encontró el bloque {% schema %}")
