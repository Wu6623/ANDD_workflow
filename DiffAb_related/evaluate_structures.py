import glob
import numpy as np
from Bio.PDB import PDBParser, Superimposer
import matplotlib.pyplot as plt
import numpy as np

def compute_rmsd(ref_pdb, gen_pdb):
    parser = PDBParser(QUIET=True)
    ref = parser.get_structure("ref", ref_pdb)
    gen = parser.get_structure("gen", gen_pdb)

    ref_atoms = [a for a in ref.get_atoms() if a.get_id() == "CA"]
    gen_atoms = [a for a in gen.get_atoms() if a.get_id() == "CA"]

    sup = Superimposer()
    sup.set_atoms(ref_atoms, gen_atoms)
    return sup.rms

def evaluate_rmsd(ref_dir, gen_dir):
    rmsds = []
    for ref_pdb in glob.glob(f"{ref_dir}/*.pdb"):
        name = ref_pdb.split("/")[-1]
        gen_pdb = f"{gen_dir}/{name}"
        if not Path(gen_pdb).exists():
            continue
        rmsds.append(compute_rmsd(ref_pdb, gen_pdb))

    return np.array(rmsds)

if __name__ == "__main__":
    rmsds = evaluate_rmsd("data/reference_pdbs", "outputs/generated")
    print("Mean RMSD:", rmsds.mean())


plt.hist(rmsds, bins=40)
plt.xlabel("Backbone RMSD (Å)")
plt.ylabel("Count")
plt.title("Illustrative RMSD distribution (DiffAb fine-tuned on ANDD)")
plt.show()
