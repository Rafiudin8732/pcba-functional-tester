import csv
import json
from pathlib import Path
from typing import Iterable, Dict, Any


def export_results(results: Iterable[Dict[str, Any]], base_path: str) -> Dict[str, str]:
    base = Path(base_path)
    base.parent.mkdir(parents=True, exist_ok=True)

    csv_path = base.with_suffix(".csv")
    json_path = base.with_suffix(".json")

    result_list = list(results)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        if result_list:
            writer = csv.DictWriter(csv_file, fieldnames=result_list[0].keys())
            writer.writeheader()
            writer.writerows(result_list)
        else:
            csv_file.write("timestamp,status,details\n")

    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(result_list, json_file, indent=2)

    return {"csv": str(csv_path), "json": str(json_path)}
