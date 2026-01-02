import os
import requests
import yaml

os.makedirs("data/raw", exist_ok=True)

with open("config/sources.yaml") as f:
    SOURCES = yaml.safe_load(f)

# ---------- PDB: real API ----------
def download_pdb_ids():
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "struct_keywords.pdbx_keywords",
                "operator": "contains_phrase",
                "value": "antibody"
            }
        },
        "return_type": "entry"
    }

    r = requests.post(SOURCES["PDB"]["search_api"], json=query)
    r.raise_for_status()
    ids = [x["identifier"] for x in r.json()["result_set"]]

    with open("data/raw/pdb_ids.txt", "w") as f:
        f.write("\n".join(ids))

    print(f"[PDB] Retrieved {len(ids)} PDB IDs")

def download_uniprot():
    params = {
        "query": "(antibody OR nanobody) NOT \"T-cell receptor\"",
        "format": "tsv",
        "fields": "accession,sequence,protein_name,organism_name",
        "size": 500
    }
    r = requests.get(SOURCES["UniProt"]["api"], params=params)
    r.raise_for_status()

    with open("data/raw/uniprot.tsv", "w") as f:
        f.write(r.text)

    print("[UniProt] Downloaded")

def create_release_placeholder(name):
    path = f"data/raw/{name}.txt"
    with open(path, "w") as f:
        f.write(f"{name} official release to be placed here\n")
    print(f"[{name}] Placeholder created")

if __name__ == "__main__":
    download_pdb_ids()
    download_uniprot()

    for k in SOURCES:
        if k not in ["PDB", "UniProt"]:
            create_release_placeholder(k)
