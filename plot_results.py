import glob, json, matplotlib.pyplot as plt
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
