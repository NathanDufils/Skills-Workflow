#!/usr/bin/env python3
"""
benchmark.py — Mesure la performance des skills urgence-*.

Métriques :
  - Temps d'exécution (ms)
  - Tokens de sortie (len(output) / 4, estimation GPT standard)
  - Tokens bruts API (taille payload non-filtré = ce qu'un MCP enverrait)
  - Ratio de réduction tokens
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import time
import subprocess
import urllib.request
import urllib.parse

# ── Coordonnées de test (Marseille centre) ────────────────────────────────
LAT, LON, DEPT, RAYON = 43.2965, 5.3811, "13", 2.0

SKILLS_DIR = os.path.dirname(os.path.abspath(__file__))

SKILL_CONFIGS = {
    "urgence-meteo": {
        "args": ["--dept", DEPT],
        "label": "Vigilance météo (dept 13)",
        "raw_api": f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=windspeed_10m,windgusts_10m,precipitation,temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,rain,showers,snowfall,weathercode,pressure_msl,surface_pressure,cloudcover,cloudcover_low,cloudcover_mid,cloudcover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapor_pressure_deficit,soil_temperature_0cm,soil_moisture_0_1cm&forecast_days=7&timezone=Europe/Paris&windspeed_unit=kmh",
    },
    "urgence-demographie": {
        "args": ["--lat", str(LAT), "--lon", str(LON), "--rayon", str(RAYON)],
        "label": f"Population r={RAYON}km Marseille",
        "raw_api": f"https://geo.api.gouv.fr/communes?lat={LAT}&lon={LON}&distance={int(RAYON*1000)}&fields=nom,code,population,codesPostaux,centre,contour,codeDepartement,codeRegion,codeEpci,surface",
    },
    "urgence-hopitaux": {
        "args": ["--lat", str(LAT), "--lon", str(LON)],
        "label": "Hôpitaux 50km Marseille",
        "raw_api": None,  # Overpass measured separately
        "raw_api_fn": "overpass_hopitaux",
    },
    "urgence-reseaux": {
        "args": ["--commune", "Marseille"],
        "label": "Réseaux Marseille",
        "raw_api": f"https://geo.api.gouv.fr/communes?nom=Marseille&fields=nom,code,population,codesPostaux,centre,contour,codeDepartement,codeRegion,codeEpci,surface,departement&format=json&boost=population&limit=5",
    },
    "urgence-risques-industriels": {
        "args": ["--lat", str(LAT), "--lon", str(LON), "--rayon", "5"],
        "label": "ICPE/SEVESO r=5km Marseille",
        "raw_api": f"https://georisques.gouv.fr/api/v1/installations_classees?latlon={LON},{LAT}&rayon=5000&page=1&page_size=100",
    },
    "urgence-briefing": {
        "args": ["--lat", str(LAT), "--lon", str(LON), "--rayon", str(RAYON), "--dept", DEPT],
        "label": "Briefing complet Marseille",
        "raw_api": None,
    },
}


def fetch_raw_size(url, timeout=12):
    """Fetch URL and return raw response size in bytes."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "benchmark/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            return len(data)
    except Exception:
        return None


def overpass_hopitaux():
    """Fetch raw Overpass response for hospitals."""
    query = f"""[out:json][timeout:25];
(
  node["amenity"~"hospital|clinic"](around:50000,{LAT},{LON});
  way["amenity"~"hospital|clinic"](around:50000,{LAT},{LON});
);
out center tags;"""
    data = urllib.parse.urlencode({"data": query}).encode()
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "benchmark/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return len(resp.read())
    except Exception:
        return None


def run_skill(name, args, timeout=60):
    """Run a skill and return (output_text, elapsed_ms)."""
    script = os.path.join(SKILLS_DIR, name, "main.py")
    if not os.path.exists(script):
        return None, None

    cmd = [sys.executable, script] + args
    t0 = time.perf_counter()
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        timeout=timeout, encoding="utf-8", errors="replace",
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000
    output = result.stdout.strip()
    return output, elapsed_ms


def estimate_tokens(text_or_bytes):
    """Rough token estimate: len / 4 (GPT-4 standard approximation)."""
    if isinstance(text_or_bytes, int):
        return max(1, text_or_bytes // 4)  # raw bytes / 4 ≈ tokens
    return max(1, len(text_or_bytes) // 4)


def bar(value, max_value, width=20):
    filled = int(value / max_value * width) if max_value > 0 else 0
    return "█" * filled + "░" * (width - filled)


def main():
    print("# Benchmark des Skills Urgence")
    print(f"**Zone de test** : {LAT}, {LON} (Marseille) · Rayon {RAYON} km · Dept {DEPT}\n")
    print("Collecte des métriques en cours...\n")

    results = {}

    # 1. Run all skills
    for name, cfg in SKILL_CONFIGS.items():
        if name == "urgence-briefing":
            continue  # run last
        print(f"  → {cfg['label']}...", end=" ", flush=True)
        output, elapsed = run_skill(name, cfg["args"])
        results[name] = {
            "output": output or "",
            "elapsed_ms": elapsed or 0,
            "label": cfg["label"],
        }
        tok = estimate_tokens(output or "")
        print(f"{elapsed:.0f}ms · {tok} tokens")

    # Run briefing last (depends on others being installed)
    print(f"  → Briefing complet (tous skills en parallèle)...", end=" ", flush=True)
    cfg = SKILL_CONFIGS["urgence-briefing"]
    output, elapsed = run_skill("urgence-briefing", cfg["args"], timeout=90)
    results["urgence-briefing"] = {
        "output": output or "",
        "elapsed_ms": elapsed or 0,
        "label": cfg["label"],
    }
    tok = estimate_tokens(output or "")
    print(f"{elapsed:.0f}ms · {tok} tokens")

    # 2. Fetch raw API sizes
    print("\n  Mesure des payloads API bruts (simulation MCP)...")
    raw_sizes = {}
    for name, cfg in SKILL_CONFIGS.items():
        if name in ("urgence-briefing",):
            continue
        raw_url = cfg.get("raw_api")
        raw_fn = cfg.get("raw_api_fn")
        if raw_fn == "overpass_hopitaux":
            print(f"  → Overpass hôpitaux (50km)...", end=" ", flush=True)
            sz = overpass_hopitaux()
        elif raw_url:
            print(f"  → {name} API brute...", end=" ", flush=True)
            sz = fetch_raw_size(raw_url)
        else:
            sz = None
        raw_sizes[name] = sz
        print(f"{sz//1024 if sz else '?'} KB" if sz else "N/A")

    # 3. Results table
    print("\n\n## Résultats\n")
    print("| Skill | Temps (ms) | Output (tokens) | API brute (tokens) | Réduction |")
    print("|-------|-----------|-----------------|-------------------|-----------|")

    max_elapsed = max((r["elapsed_ms"] for r in results.values()), default=1)

    for name, r in results.items():
        if name == "urgence-briefing":
            continue
        out_tokens = estimate_tokens(r["output"])
        raw_bytes = raw_sizes.get(name)
        raw_tokens = estimate_tokens(raw_bytes if raw_bytes else 0)
        if raw_bytes:
            raw_tokens_display = f"~{raw_tokens:,}".replace(",", " ")
            ratio = raw_tokens / out_tokens if out_tokens > 0 else 0
            ratio_str = f"**÷{ratio:.0f}**" if ratio >= 2 else f"÷{ratio:.1f}"
        else:
            raw_tokens_display = "N/A"
            ratio_str = "—"

        elapsed_str = f"{r['elapsed_ms']:.0f}"
        print(f"| `{name}` | {elapsed_str} | **{out_tokens:,}**".replace(",", " ") +
              f" | {raw_tokens_display} | {ratio_str} |")

    # Briefing row
    r = results["urgence-briefing"]
    out_tokens = estimate_tokens(r["output"])
    print(f"| `urgence-briefing` | **{r['elapsed_ms']:.0f}** | **{out_tokens:,}**".replace(",", " ") +
          f" | *(agrégé)* | — |")

    print("\n## Détail des performances\n")

    # Time chart
    print("### ⏱️ Temps d'exécution\n")
    for name, r in results.items():
        label = r["label"][:35]
        b = bar(r["elapsed_ms"], max(r["elapsed_ms"] for r in results.values()))
        print(f"`{b}` **{r['elapsed_ms']:.0f}ms** — {label}")

    print("\n### 📉 Réduction tokens vs MCP (payload brut)\n")
    for name, r in results.items():
        if name == "urgence-briefing":
            continue
        out_tokens = estimate_tokens(r["output"])
        raw_bytes = raw_sizes.get(name)
        if not raw_bytes:
            continue
        raw_tokens = estimate_tokens(raw_bytes)
        ratio = raw_tokens / out_tokens if out_tokens > 0 else 0
        b = bar(out_tokens, raw_tokens)
        print(f"`{b}` **÷{ratio:.0f}** réduction — `{name}`")
        print(f"  → MCP brut : ~{raw_tokens:,} tokens | Skill filtré : **{out_tokens:,} tokens**\n".replace(",", " "))

    print("---")
    print("*Token estimé = len(texte) / 4 (approximation GPT-4 standard)*")
    print("*API brute = payload JSON complet sans filtrage, tel qu'un serveur MCP l'enverrait au LLM*")


if __name__ == "__main__":
    main()
