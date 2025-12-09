import xml.etree.ElementTree as ET
import copy
import re
from regions import REGIONS

INPUT_SVG = "world.svg"
OUTPUT_SVG = "world_grouped.svg"

# --- Parse SVG ---
tree = ET.parse(INPUT_SVG)
root = tree.getroot()

# --- Remove namespace prefixes ---
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]

# --- Remove non-SVG namespaced attributes ---
for elem in root.iter():
    for attr in list(elem.attrib):
        if ':' in attr:
            del elem.attrib[attr]

# --- Create empty group elements ---
groups = {region: ET.Element("g", id=region) for region in REGIONS}

# --- Collect ungrouped countries ---
ungrouped = []

# --- Loop over all paths and copy into groups ---
for path in root.findall(".//path"):
    cid = path.get("id", "").upper()
    found = False
    for region, countries in REGIONS.items():
        if cid in countries:
            groups[region].append(copy.deepcopy(path))
            found = True
            break  # Stop after first matching group
    if not found:
        ungrouped.append(cid)

# --- Append all non-empty groups to root ---
for g in groups.values():
    if len(g):
        root.append(g)

# --- Save the cleaned and grouped SVG ---
tree.write(OUTPUT_SVG, encoding="utf-8", xml_declaration=True)
print("Saved grouped SVG:", OUTPUT_SVG)

# --- Print ungrouped countries ---
print("Ungrouped countries:", ungrouped)