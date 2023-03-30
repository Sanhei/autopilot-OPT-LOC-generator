#!/bin/bash
#SBATCH --job-name=ORCA_test    ### CHANGE ###   # Job name, will show up in squeue Out-put
#SBATCH --ntasks=8                               # Number of cores
#SBATCH --nodes=1                                # Ensure that all cores are on one machine
#SBATCH --time=06:00:00                        # Runtime in DAYS-HH:MM:SS format
#SBATCH --mem-per-cpu=1400                        # Memory per cpu in MB (see also --mem)
#SBATCH --output=outputfile.dat    ### CHANGE ###   # File to which standard Out- will be written
#SBATCH --error=errorfile.dat      ### CHANGE ###   # File to which standard err will be written
#SBATCH --mail-type=NONE                          # Type of email notification- NONE,BEGIN,END,FAIL,ALL
#SBATCH --qos=standard


module add ORCA/5.0.0-gompi-2021a


# name and path of the output file
workdir="$(pwd)"
currentdir="${PWD##*/}"
# This contains molecular name

tempdir="/scratch/fu5030ky/$currentdir"
if [ -d "$tempdir" ]; then
    echo "$tempdir exits"
else
    mkdir /scratch/fu5030ky/$currentdir
    echo "/scratch/fu5030ky/$currentdir created"
fi




echo "$tempdir"
cd $workdir
cp * $tempdir
cd $tempdir

/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca OPT_R_5_KETO4.inp > R_5_KETO4.out
pwd

cp *.xyz $workdir

rm -rf /scratch/fu5030ky/$currentdir


