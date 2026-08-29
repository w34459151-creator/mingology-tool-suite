"""Update the WORLD birthplace records from the GeoNames public dump.

The updater is deliberately transactional: the existing address_library.json is
only replaced after the downloaded data and generated records pass validation.
Set GEONAMES_DATASET=allCountries for maximum coverage; cities500 is the
practical default for a GUI selector.
"""
import csv
import io
import json
import os
import shutil
import tempfile
import time
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIBRARY_PATH = ROOT / "address_library.json"
GEONAMES_BASE = "https://download.geonames.org/export/dump"
DATASET = os.environ.get("GEONAMES_DATASET", "cities500")
MIN_WORLD_ENTRIES = 1000


def download_bytes(name):
    url = f"{GEONAMES_BASE}/{name}.zip"
    request = urllib.request.Request(url, headers={"User-Agent": "MyBookAnalysis-address-updater/1.0"})
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read()
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Download failed after 3 attempts: {url}") from last_error


def download_text(name):
    url = f"{GEONAMES_BASE}/{name}"
    request = urllib.request.Request(url, headers={"User-Agent": "MyBookAnalysis-address-updater/1.0"})
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Download failed after 3 attempts: {url}") from last_error


def read_zip_text(payload, filename):
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        with archive.open(filename) as stream:
            content = stream.read().decode("utf-8", errors="replace")
    return io.StringIO(content)


def load_country_names():
    names = {}
    for row in csv.reader(io.StringIO(download_text("countryInfo.txt")), delimiter="\t"):
        if not row or row[0].startswith("#") or len(row) < 5:
            continue
        names[row[0]] = row[4] or row[0]
    return names


def load_admin1_names():
    names = {}
    for row in csv.reader(io.StringIO(download_text("admin1CodesASCII.txt")), delimiter="\t"):
        if len(row) >= 2:
            names[row[0]] = row[1] or row[0].split(".", 1)[-1]
    return names


def make_world_entries(country_names, admin1_names):
    entries = []
    seen = set()
    filename = f"{DATASET}.txt"
    with read_zip_text(download_bytes(DATASET), filename) as stream:
        for row in csv.reader(stream, delimiter="\t"):
            if len(row) < 15 or row[6] != "P":
                continue
            geoname_id, name, ascii_name = row[0], row[1], row[2]
            country_code, admin1_code = row[8], row[10]
            try:
                latitude = float(row[4])
                longitude = float(row[5])
            except ValueError:
                continue
            if not country_code or not name or not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                continue
            state = admin1_names.get(f"{country_code}.{admin1_code}", admin1_code or country_code)
            country = country_names.get(country_code, country_code)
            key = (country, state, name, latitude, longitude)
            if key in seen:
                continue
            seen.add(key)
            aliases = [ascii_name] if ascii_name and ascii_name != name else []
            entries.append({
                "region": "WORLD",
                "name": f"{country} {state} {name}",
                "country": country,
                "state": state,
                "city": name,
                "latitude": latitude,
                "longitude": longitude,
                "aliases": aliases,
                "geonames_id": int(geoname_id),
            })
    return entries


def validate(entries):
    if len(entries) < MIN_WORLD_ENTRIES:
        raise ValueError(f"GeoNames result too small: {len(entries)} records")
    for entry in entries:
        if entry.get("region") != "WORLD" or not entry.get("country") or not entry.get("city"):
            raise ValueError("WORLD record has missing hierarchy fields")
        if not isinstance(entry.get("latitude"), float) or not isinstance(entry.get("longitude"), float):
            raise ValueError("WORLD record has invalid coordinates")


def atomic_write(path, payload):
    fd, temp_name = tempfile.mkstemp(prefix=f"{path.stem}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def main():
    with LIBRARY_PATH.open("r", encoding="utf-8") as stream:
        current = json.load(stream)
    current_entries = current.get("entries")
    if not isinstance(current_entries, list):
        raise ValueError("address_library.json has no entries list")

    world_entries = make_world_entries(load_country_names(), load_admin1_names())
    validate(world_entries)
    cn_entries = [entry for entry in current_entries if str(entry.get("region", "")).upper() == "CN"]
    updated = dict(current)
    updated["version"] = date.today().isoformat()
    updated["description"] = (
        "本地出生地地址库。CN 由中国行政区数据维护；WORLD 由 GeoNames populated places 定期更新，"
        "所有有坐标记录均可用于真太阳时。"
    )
    updated["world_source"] = {
        "provider": "GeoNames",
        "dataset": DATASET,
        "updated_at": date.today().isoformat(),
        "license": "CC BY 4.0",
    }
    updated["entries"] = cn_entries + world_entries
    atomic_write(LIBRARY_PATH, updated)
    print(f"Updated WORLD entries: {len(world_entries)}")
    print(f"Preserved CN entries: {len(cn_entries)}")
    print(f"Dataset: {DATASET}")


if __name__ == "__main__":
    main()
