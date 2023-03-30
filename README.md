# autopilot-OPT-LOC-generator
This is used for generating DFT input files

## Sample's Copyright

The sample files input copyrights are from Fabian's paper (For clearly citation: https://pubs.rsc.org/en/content/articlelanding/2019/CP/C8CP06620E). 

## Instruction
### Environment
1. Default python environment and bash shell to create DFT (ORCA) calculation script.
2. The script running environment is based on slurm.

### Procedure
For the DFT calculation:
1. Optimize the molecular structure by OPT_sample.inp. In the sample, the author give a ratio to nearest neighbor interaction for better optimization.
2. Localize the molecular orbital excitation by LOC_sample.inp.
Any other change to the DFT calculation should change these two files.
*******************************************
KEEP IN MIND,
DFT calculation will take tons of disk space,
change the both .sh file where KEYWORDS:/scratch/fu5030ky/ to your $own/scratch/path$.
********************************************



The input files should be format of xyz, adding to the directory: xas_input/xyzfile/
After setting up the input, run the python script. ( The package includes: sys, fileinput, os and shutil, all these should include in the default python).
```bash
python sh_inp_DFT_maker.py
```
The generate scripts will be in the OPT_output, it contains structure as follow:
1. According to the xyz input file, the program will generate a dir which is named by the xyz file. (e.g. C_H3CH2_OH.xyz, will create a dir ./OPT_output/C_H3CH2_OH)
2. Each generated file includes five files. OPT_$FILENAME$.sh, OPT_$FILENAME$.inp, LOC_$FILENAME$.inp, LOC_$FILENAME$.sh and $FILENAME$.xyz.

On the cluster (slurm), should do the optimization first then localize in ./OPT_output
```bash
bash OPT_run.sh
```
Until it has done, run localization.
```bash
bash LOC_run.sh
```
### Notice
Each calculation will use 8 cores as default. They are parallel runing do not share buffer.



