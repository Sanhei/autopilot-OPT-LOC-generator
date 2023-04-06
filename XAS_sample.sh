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
currentdir=${currentdir:-/} 
cd ..
lastdir="${PWD##*/}"
lastdir=${lastdir:-/} 
cd $currentdir
rootdir="/scratch/fu5030ky/$lastdir"

if [ -d "$rootdir" ]; then
    echo "$rootdir exits"
else
    mkdir /scratch/fu5030ky/$lastdir
    echo "/scratch/fu5030ky/$lastdir created"
fi

tempdir="/scratch/fu5030ky/$lastdir/$currentdir"
if [ -d "$tempdir" ]; then
    echo "$tempdir exits"
else
    mkdir /scratch/fu5030ky/$lastdir/$currentdir
    echo "/scratch/fu5030ky/$lastdir/$currentdir created"
fi




echo "$tempdir"
cd $workdir
cp * $tempdir
cd $tempdir

/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca 2125.inp > 2125.out 
/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca_mapspc 2125.out ABSQ -eV 0270 -1300 -n500 -w0.5
pwd
cp *.stk $workdir
cp *.xyz $workdir
cp *.dat $workdir
cp *.out $workdir
cp *.loc $workdir
rm -rf $tempdir


