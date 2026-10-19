import json, sys, numpy as np

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
