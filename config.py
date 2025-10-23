import json
import os


def _config_path() -> str:
    return os.path.join(os.path.dirname(__file__), "config.json")


DEFAULT_CONFIG = {
    "sources": {
        "musicbrainz": True,
        "lastfm": {"enabled": False, "api_key": ""},
        "spotify": {"enabled": False, "token": ""},
        "google": {"enabled": False, "key": "", "cx": ""},
    },
    "search_mode": "artist_title",  # artist_title | artist_only
    "translate": {
        "enabled": False,
        "provider": "libretranslate",  # libretranslate | none
        "endpoint": "https://libretranslate.de/translate",
        "api_key": "",
    },
}


def load_config() -> dict:
    path = _config_path()
    if not os.path.exists(path):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # merge defaults for missing keys
        cfg = DEFAULT_CONFIG.copy()
        cfg["sources"].update(data.get("sources", {}))
        cfg["search_mode"] = data.get("search_mode", cfg["search_mode"])
        cfg["translate"].update(data.get("translate", {}))
        return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(cfg: dict) -> None:
    path = _config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)