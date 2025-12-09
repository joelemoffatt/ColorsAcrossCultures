import xml.etree.ElementTree as ET
import copy

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

# --- Define regions/groups ---
# --- Updated regions with extra countries ---
REGIONS = {
    "north_america": {"US", "CA", "MX", "GT", "BZ", "SV", "HN", "NI", "CR", "PA", "AG",
                      "AI", "AW", "BB", "BM", "BS", "BQ", "CU", "CW", "DM", "DO",
                      "GD", "GL", "GP", "HT", "JM", "KN", "KY", "LC", "MF", "MS",
                      "PR", "SX", "TC", "TT", "VC", "VG", "VI"},
    "south_america": {"AR", "CL", "BO", "PE", "EC", "CO", "VE", "GY", "SR", "BR", "UY", "PY", 
                      "FK", "GF", "GY", "GS"},
    "europe": {"FR","DE","ES","IT","PT","GB","IE","NL","BE","CH","AT","PL","CZ","SK","HU",
               "RO","BG","GR","SE","NO","FI","DK","IS","AD","AL","AX","BA","BY","BL","FO",
               "GI","GG","HR","IM","JE","LI","LT","LU","LV","MC","MD","ME","MK","MT","SM",
               "RS","SI","SJ","UA","VA","XK", "CY", "EE"},
    "russia": {"RU"},
    "china": {"CN","HK","MO","TW"},
    "japan": {"JP"},
    "india": {"IN"},
    "africa": {
        "DZ","AO","BJ","BW","BF","BI","CM","CV","CF","TD","KM","CG","CD","DJ","EG","GQ","ER",
        "SZ","ET","GA","GM","GH","GN","GW","CI","KE","LS","LR","LY","MG","MW","ML","MR","MU",
        "MA","MZ","NA","NE","NG","RW","ST","SN","SC","SL","SO","ZA","SS","SD","TZ","TG","TN",
        "UG","ZM","ZW"
    },
    "asia": {"AE","LB","KR","KP","MN","VN","KH","TH","LA","MM","BD","PK","AF","IR","IQ","SA","YE","JO",
             "SY","TR","GE","AM","AZ","LK","NP","BT","BN","KH","ID","IL","IO","KZ","KG","KW",
             "LA","MY","MV","NP","OM","PH","QA","SG","TJ","TM","UZ","TL","VN","PS","CC","CX",
             "FJ","FM","GU","HK","HM","ID","JP","KR","KI","MH","MP","NF","NR","NU","NC","PW",
             "PG","PF","SB","TW","TH","TV","VU","WF","WS","YT"},
    "australia_oceania": {"AU","NZ","FJ","PG","SB","VU","NC","WS","TO","KI","TV","NR","NU"},    
}

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