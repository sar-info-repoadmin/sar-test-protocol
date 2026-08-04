import csv, re, os, sys, glob
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "Washing Machine Accessibility Reporting Template.csv")

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")

rows = []
with open(SRC, newline="", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    all_rows = list(reader)

# find header row (the one starting with "Category")
header_idx = None
for i, r in enumerate(all_rows):
    if r and r[0].strip() == "Category":
        header_idx = i
        break
assert header_idx is not None, "header not found"
header = all_rows[header_idx]

for r in all_rows[header_idx + 1:]:
    if not r or not r[0].strip():
        continue
    if r[0].strip().lower() == "notes":
        break
    category, requirement, expected, passfail, reference = (r + [""] * 5)[:5]
    rows.append({
        "category": category.strip(),
        "requirement": requirement.strip(),
        "expected": expected.strip(),
        "passfail": passfail.strip(),
        "reference": reference.strip(),
    })

print(f"Parsed {len(rows)} criteria rows", file=sys.stderr)

# ordered unique categories, by first appearance
categories = []
for r in rows:
    if r["category"] not in categories:
        categories.append(r["category"])

os.makedirs(os.path.join(ROOT, "_data"), exist_ok=True)
with open(os.path.join(ROOT, "_data", "categories.yml"), "w") as f:
    yaml.safe_dump(categories, f, sort_keys=False, allow_unicode=True)

os.makedirs(os.path.join(ROOT, "_criteria"), exist_ok=True)
for f in glob.glob(os.path.join(ROOT, "_criteria", "*.md")):
    os.remove(f)

# track slug counts per category to disambiguate
seen_slugs = {}
for idx, r in enumerate(rows):
    cat_slug = slugify(r["category"])
    req_slug = slugify(r["requirement"])
    slug = f"{cat_slug}-{req_slug}"
    if slug in seen_slugs:
        seen_slugs[slug] += 1
        slug = f"{slug}-{seen_slugs[slug]}"
    else:
        seen_slugs[slug] = 1

    front_matter = {
        "layout": "criterion",
        "title": r["requirement"],
        "category": r["category"],
        "order": idx,
        "expected_behavior": r["expected"],
        "pass_fail_criteria": r["passfail"],
        "reference": r["reference"],
        "slug": slug,
    }
    fname = os.path.join(ROOT, "_criteria", f"{idx:02d}-{slug}.md")
    with open(fname, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(front_matter, f, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
        f.write("---\n")

print("Categories:", categories, file=sys.stderr)
print("Done.", file=sys.stderr)
