import json
from pathlib import Path

idl_path = Path("target/idl/diagraph_provenance.json")
with open(idl_path, "r") as f:
    idl = json.load(f)

# Move version and name to top level
fixed_idl = {
    "version": idl["metadata"]["version"],
    "name": idl["metadata"]["name"],
    "instructions": idl["instructions"],
    "metadata": {
        "address": idl["address"],
        "spec": idl["metadata"]["spec"],
        "description": idl["metadata"]["description"]
    }
}

with open(idl_path, "w") as f:
    json.dump(fixed_idl, f, indent=2)
