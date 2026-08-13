import json
import os
import urllib.request
from collections import defaultdict
from datetime import date


ROOT = os.path.dirname(__file__)
LIB_PATH = os.path.join(ROOT, "address_library.json")
OUT_AUDIT_PATH = os.path.join(ROOT, "output", "cn_address_audit_latest.json")
PCA_URL = "https://raw.githubusercontent.com/modood/Administrative-divisions-of-China/master/dist/pca-code.json"

EXCLUDE_PROVINCES = {
    "台湾省",
    "香港特别行政区",
    "澳門特別行政區",
    "香港特別行政區",
    "澳门特别行政区",
}

SKIP_CITY_BUCKETS = {
    "省直辖县级行政区划",
    "自治区直辖县级行政区划",
}


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def fetch_pca_data():
    req = urllib.request.Request(
        PCA_URL,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")
    payload = json.loads(content)
    if not isinstance(payload, list):
        raise ValueError("Unexpected PCA payload format")
    return payload


def normalize_text(v):
    return str(v or "").strip()


def key_of(entry):
    return (
        normalize_text(entry.get("province")),
        normalize_text(entry.get("city")),
        normalize_text(entry.get("district")),
    )


def build_existing_cn_index(entries):
    idx = {}
    for e in entries:
        if normalize_text(e.get("region")).upper() != "CN":
            continue
        k = key_of(e)
        if all(k):
            idx[k] = e
    return idx


def build_cn_from_pca(pca_data, existing_cn_index):
    source_set = set()
    city_to_districts = defaultdict(list)

    for prov in pca_data:
        province = normalize_text(prov.get("name"))
        if not province or province in EXCLUDE_PROVINCES:
            continue
        cities = prov.get("children") or []
        for city_item in cities:
            city = normalize_text(city_item.get("name"))
            if not city:
                continue
            if city in SKIP_CITY_BUCKETS:
                # 仅覆盖地级市口径，跳过“省直辖县级行政区划”等县级占位桶。
                continue
            districts_raw = [
                normalize_text(d.get("name"))
                for d in (city_item.get("children") or [])
                if normalize_text(d.get("name"))
            ]
            # 如果同城有更细区县，去掉泛化“市辖区”。
            if len(districts_raw) > 1:
                districts = [d for d in districts_raw if d != "市辖区"]
            else:
                districts = districts_raw

            if not districts:
                districts = ["市辖区"]

            for district in districts:
                source_set.add((province, city, district))
                city_to_districts[(province, city)].append(district)

    cn_entries = []
    seen = set()

    for province, city, district in sorted(source_set):
        k = (province, city, district)
        if k in seen:
            continue
        seen.add(k)

        existing = existing_cn_index.get(k, {})
        name = normalize_text(existing.get("name")) or f"{province}{city}{district}"

        aliases = existing.get("aliases") if isinstance(existing.get("aliases"), list) else []
        aliases = [normalize_text(x) for x in aliases if normalize_text(x)]
        # 默认别名：城市+区县、区县本名
        if district != "市辖区":
            for alias in (f"{city}{district}", district):
                if alias and alias not in aliases:
                    aliases.append(alias)
        else:
            for alias in (city,):
                if alias and alias not in aliases:
                    aliases.append(alias)

        entry = {
            "region": "CN",
            "name": name,
            "province": province,
            "city": city,
            "district": district,
            "aliases": aliases,
        }

        if "latitude" in existing and "longitude" in existing:
            entry["latitude"] = existing["latitude"]
            entry["longitude"] = existing["longitude"]

        cn_entries.append(entry)

    return cn_entries, source_set


def build_audit(cn_entries, source_set):
    city_groups = defaultdict(set)
    counts = defaultdict(int)
    for e in cn_entries:
        p = normalize_text(e.get("province"))
        c = normalize_text(e.get("city"))
        d = normalize_text(e.get("district"))
        counts[(p, c, d)] += 1
        city_groups[(p, c)].add(d)

    duplicate_items = [
        {"province": p, "city": c, "district": d, "count": n}
        for (p, c, d), n in sorted(counts.items()) if n > 1
    ]

    city_single_district = [
        {"province": p, "city": c, "districts": sorted(list(ds))}
        for (p, c), ds in sorted(city_groups.items())
        if len(ds) == 1
    ]

    generated_set = {
        (
            normalize_text(e.get("province")),
            normalize_text(e.get("city")),
            normalize_text(e.get("district")),
        )
        for e in cn_entries
    }
    missing_from_generated = [
        {"province": p, "city": c, "district": d}
        for (p, c, d) in sorted(source_set - generated_set)
    ]

    provinces = sorted({normalize_text(e.get("province")) for e in cn_entries if normalize_text(e.get("province"))})
    cities = sorted({(normalize_text(e.get("province")), normalize_text(e.get("city"))) for e in cn_entries if normalize_text(e.get("province")) and normalize_text(e.get("city"))})

    return {
        "generated_at": date.today().isoformat(),
        "cn_entry_count": len(cn_entries),
        "province_count": len(provinces),
        "city_count": len(cities),
        "duplicate_items": duplicate_items,
        "missing_from_generated": missing_from_generated,
        "single_district_cities": city_single_district,
    }


def main():
    data = read_json(LIB_PATH)
    entries = data.get("entries") or []

    existing_cn_index = build_existing_cn_index(entries)
    world_entries = [e for e in entries if normalize_text(e.get("region")).upper() != "CN"]

    pca_data = fetch_pca_data()
    cn_entries, source_set = build_cn_from_pca(pca_data, existing_cn_index)

    data["version"] = date.today().isoformat()
    data["description"] = "本地出生地地址库（可扩展）。CN 按省/地级市/区县完整覆盖；有坐标可直接启用真太阳时，无坐标由在线 geocode 兜底。"
    data["entries"] = cn_entries + world_entries

    write_json(LIB_PATH, data)

    audit = build_audit(cn_entries, source_set)
    write_json(OUT_AUDIT_PATH, audit)

    print("CN entries:", audit["cn_entry_count"])
    print("Provinces:", audit["province_count"])
    print("Cities:", audit["city_count"])
    print("Duplicates:", len(audit["duplicate_items"]))
    print("Missing:", len(audit["missing_from_generated"]))
    print("Single-district cities:", len(audit["single_district_cities"]))
    print("Audit file:", OUT_AUDIT_PATH)


if __name__ == "__main__":
    main()
