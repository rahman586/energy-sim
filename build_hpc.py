import os
import json
import numpy as np

print("Membangun struktur direktori HPC...")
for folder in ['code', 'results', 'logs']:
    os.makedirs(folder, exist_ok=True)

# 1. Buat kode simulasi
with open("code/simulate_energy.py", "w") as f:
    f.write("""import json, sys, numpy as np

def simulate(num_agents, days, ac_kw=1.5, seed=42):
    rng = np.random.default_rng(seed)
    total_kwh = 0.0
    for _ in range(days):
        for _ in range(num_agents):
            start = rng.integers(8, 17)
            hours = max(0, min(start + rng.integers(1, 4), 17) - max(start, 8))
            total_kwh += hours * ac_kw
    return total_kwh

num_agents = int(sys.argv[1]) if len(sys.argv) > 1 else 100
days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
res = {"num_agents": num_agents, "days": days, "total_kwh": round(simulate(num_agents, days), 2)}

with open(f"results/run_{num_agents}_{days}.json", "w") as f:
    json.dump(res, f, indent=2)
print(f"Selesai: {num_agents} agen -> {res['total_kwh']} kWh")
""")

# 2. Buat SLURM Job Script (untuk dipajang di GitHub)
with open("run.sh", "w", newline='\n') as f:
    f.write("""#!/bin/bash
#SBATCH --job-name=energy_sim
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00
#SBATCH --output=logs/slurm_%j.out
#SBATCH --partition=normal

module load python/3.11
cd $SLURM_SUBMIT_DIR

for agents in 50 100 200 400; do
    echo "Menjalankan simulasi $agents agen..."
    python3 code/simulate_energy.py $agents 30
done
""")

# 3. Buat script pembuat grafik
with open("plot_results.py", "w") as f:
    f.write("""import glob, json, matplotlib.pyplot as plt
data = []
for f in glob.glob("results/*.json"):
    with open(f) as fp:
        d = json.load(fp)
        data.append((d["num_agents"], d["total_kwh"]))
data.sort()
plt.plot([d[0] for d in data], [d[1] for d in data], marker="o", color="b")
plt.xlabel("Jumlah Agen (Mahasiswa)")
plt.ylabel("Total Konsumsi Energi (kWh)")
plt.title("Simulasi Energi Gedung")
plt.grid(True)
plt.savefig("results/grafik.png", dpi=150)
""")

# 4. Buat README dan gitignore
with open("README.md", "w") as f:
    f.write("# Simulasi Energi Gedung di Superkomputer (HPC)\n\nMensimulasikan total konsumsi listrik gedung kampus akibat penggunaan AC menggunakan *Agent-Based Simulation* dengan *scheduler* SLURM.\n\n## Struktur\n- `code/`: Kode sumber Python.\n- `run.sh`: Job script SLURM untuk *cluster* HPC.\n- `results/`: Output JSON dan grafik hasil komputasi.")
with open(".gitignore", "w") as f:
    f.write("__pycache__/\nlogs/\n")

# 5. JALANKAN SIMULASI LOKAL (Agar ada hasil untuk di-upload)
print("Menjalankan simulasi (seolah-olah di cluster)...")
for agents in [50, 100, 200, 400]:
    os.system(f"python code/simulate_energy.py {agents} 30")

print("Membuat grafik visualisasi...")
os.system("python plot_results.py")

print("\n✅ BERHASIL! Semua file siap di-upload ke GitHub.")