import json

# Load the original database, handling potential BOM
with open('./database.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Ensure every "bild" field is an array
for entry in data.get('eintraege', {}).get('eintrag', []):
    bild_value = entry.get('bild')
    if isinstance(bild_value, list):
        # Already an array, leave as is
        continue
    elif isinstance(bild_value, str):
        # Split on commas, strip whitespace
        parts = [s.strip() for s in bild_value.split(',') if s.strip()]
        entry['bild'] = parts
    else:
        # For missing or null, set empty array
        entry['bild'] = []

# Save the transformed database to a new file
output_path = './database_fixed_all.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Die aktualisierte Datei wurde gespeichert unter: {output_path}")
