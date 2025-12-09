import csv
import json

INPUT_CSV = "color_meanings.csv"
OUTPUT_JSON = "color_meanings.json"

data = {}

with open(INPUT_CSV, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Get headers (skip first column)
headers = [h.strip() for h in rows[0][1:]]

current_color = None

for row in rows[1:]:
    first_col = row[0].strip()
    if first_col:
        # New color
        current_color = first_col
        data[current_color] = {region: [] for region in headers}
    
    if not current_color:
        continue
    
    for i, cell in enumerate(row[1:]):
        cell = cell.strip()
        if cell:
            region = headers[i]
            data[current_color][region].append(cell)

# Save as JSON
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved color meanings to {OUTPUT_JSON}")