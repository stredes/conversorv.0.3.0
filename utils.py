
import logging
import json
from pathlib import Path
from typing import Dict, Set

LOG_FILE = Path("app.log")
CONFIG_FILE = Path("excel_printer_config.json")
DEFAULT_CONFIG = {
    "listados": ["Columna1", "Columna5", "Columna6", "Columna7", "Columna8", "Columna10"],
    "urbano": ["Columna0", "Columna2"],
    "fedex": ["Columna3", "Columna4"]
}

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def load_config() -> Dict[str, Dict[str, Set[str]]]:
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            config = json.load(f)
            new_config = {}
            for mode, conf in config.items():
                new_config[mode] = {
                    "eliminar": set(conf.get("eliminar", [])),
                    "sumar": set(conf.get("sumar", [])),
                    "mantener_formato": set(conf.get("mantener_formato", []))
                }
            return new_config
    except FileNotFoundError:
        return {mode: {"eliminar": set(DEFAULT_CONFIG.get(mode, [])), "sumar": set(), "mantener_formato": set()} for mode in DEFAULT_CONFIG}

def save_config(config: Dict[str, Dict[str, Set[str]]]) -> None:
    serializable_config = {
        mode: {
            "eliminar": list(conf["eliminar"]),
            "sumar": list(conf["sumar"]),
            "mantener_formato": list(conf["mantener_formato"])
        }
        for mode, conf in config.items()
    }
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(serializable_config, f, indent=4)
