from __future__ import annotations
import json, csv, io, re
from typing import List, Tuple, Optional
import yaml

FINDINGS = [
    (r"\b(?:password|passwd|secret|api[_-]?key|token)\b", "Possible sensitive field name", "high"),
    (r"\b(?:null|none|nan)\b", "Null-like literal present", "low"),
]

def scan_json_text(name: str, text: str) -> List[Tuple[str, str, Optional[int], str, str]]:
    findings = []
    try:
        obj = json.loads(text)
    except Exception as e:
        findings.append((name, "", None, "invalid_json", str(e)))
        return findings
    def walk(o, path="root"):
        if isinstance(o, dict):
            for k,v in o.items():
                for pattern, desc, sev in FINDINGS:
                    if re.search(pattern, str(k), re.I):
                        findings.append((name, f"{path}.{k}", None, desc, sev))
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, it in enumerate(o):
                walk(it, f"{path}[{i}]")
        else:
            s = str(o)
            for pattern, desc, sev in FINDINGS:
                if re.search(pattern, s, re.I):
                    findings.append((name, path, None, desc, sev))
    walk(obj)
    return findings

def scan_yaml_text(name: str, text: str):
    try:
        obj = yaml.safe_load(text)
    except Exception as e:
        return [(name, "", None, "invalid_yaml", str(e))]
    return scan_json_text(name, json.dumps(obj))

def scan_csv_text(name: str, text: str):
    findings = []
    try:
        buf = io.StringIO(text)
        reader = csv.DictReader(buf)
        for rnum, row in enumerate(reader, start=2):
            for k,v in row.items():
                for pattern, desc, sev in FINDINGS:
                    if re.search(pattern, str(k), re.I) or re.search(pattern, str(v), re.I):
                        findings.append((name, f"row:{rnum}.{k}", rnum, desc, sev))
    except Exception as e:
        findings.append((name, "", None, "invalid_csv", str(e)))
    return findings
