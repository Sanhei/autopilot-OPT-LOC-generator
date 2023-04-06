#!/bin/bash
#SBATCH --job-name=ORCA_test    ### CHANGE ###   # Job name, will show up in squeue Out-put
#SBATCH --ntasks=1                               # Number of cores
#SBATCH --nodes=1                                # Ensure that all cores are on one machine
#SBATCH --time=00:30:00                        # Runtime in DAYS-HH:MM:SS format
#SBATCH --mem-per-cpu=1400                        # Memory per cpu in MB (see also --mem)
#SBATCH --output=outputfile.dat    ### CHANGE ###   # File to which standard Out- will be written
#SBATCH --error=errorfile.dat      ### CHANGE ###   # File to which standard err will be written
#SBATCH --mail-type=NONE                          # Type of email notification- NONE,BEGIN,END,FAIL,ALL
#SBATCH --qos=standard

srun python XAS_sh_inp_DFT_maker.py
