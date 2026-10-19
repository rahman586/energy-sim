#!/bin/bash
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
