import json
import os
import hashlib
import time

CACHE_FILE = "data/precomputed_features.json"
CACHE_TTL = 7 * 24 * 60 * 60  # 7 days


# in-memory cache (fast access)
_memory_cache = {}


def _load_disk_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def _save_disk_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def generate_cache_key(data):
    # stable hash from input
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached_result(key):
    # check memory first
    if key in _memory_cache:
        entry = _memory_cache[key]
        if time.time() - entry["timestamp"] < CACHE_TTL:
            return entry["value"]

    # fallback to disk
    disk_cache = _load_disk_cache()
    if key in disk_cache:
        entry = disk_cache[key]

        if time.time() - entry["timestamp"] < CACHE_TTL:
            _memory_cache[key] = entry
            return entry["value"]

    return None


def store_cached_result(key, value):
    entry = {
        "value": value,
        "timestamp": time.time()
    }

    # update memory
    _memory_cache[key] = entry

    # update disk
    disk_cache = _load_disk_cache()
    disk_cache[key] = entry
    _save_disk_cache(disk_cache)