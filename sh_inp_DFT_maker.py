'''
Copyright from AG Banda,

Helmholtz Zentral Berlin.
'''


import sys
import fileinput
import os
import shutil
'''
For Usage:
    1. the output path is in output_path.
    2. The copy script filename is OPT_sample.sh and OPT_sampe.inp. 
       OPT simply implies the optimization.

Process:
    1. Find all the input files with format .xyz.
    2. create a corsponding directory with pre-index of .xyz file 
       (e.g. C_OH.xyz, will create a C_OH dir in output_path).
    3. copy the OPT_sample.sh and OPT_sample.inp to the directory.
    4. substitude the text in the .sh and .inp files.
    5. repeat 3, 4 for Localization calculation.
    ################################################################
    OPT_sample.sh is the cluster input.
    OPT_sample.inp is ORCA input.
    as well as LOC_sample
    #################################################################

'''

global output_path
output_path = "./OPT_output/"

# Create new directory
def new_dirctory(directory):
    if os.path.isdir(directory) == False:
        os.mkdir(directory)

new_dirctory(output_path)
# This will save the document for later DFT calculation on cluster


# Copy files

def copy_files(file_name):
    shutil.copy('OPT_sample.sh',  output_path+file_name+"/"+file_name+'.sh') 
    shutil.copy('OPT_sample.inp', output_path+file_name+"/"+file_name+'.inp') 

# This will change a whole line text to another
def replace_line_text(file_name_format, original_line, change_line):
    for i, line in enumerate(fileinput.input(file_name_format, inplace=1)):
        # inplace = 1 means write into the file.
        sys.stdout.write(line.replace(original_line, change_line))


dir_input = "./xas_input/"
new_dirctory(dir_input)

# Add label for different LOC and OPT
LOC = "LOC_"
OPT = "OPT_"




for subdir, dirs, files in os.walk(dir_input+"xyzfile"):
    for file_name in files:
        name_input = file_name.split(".")[0]
        # e.g. file name abc.xyz, then, name_input = "abc"
        new_dirctory(output_path+name_input)
        # Create directory
        print(output_path+file_name)
        input_xyz  = dir_input+'xyzfile/'+file_name
        output_dir = output_path+name_input+"/"
        print(output_dir+name_input)
        new_dirctory(output_dir)

        orbital_dir = output_path+name_input
        new_dirctory(orbital_dir)
        # Generate files for each orbital
        shutil.copy(input_xyz, orbital_dir+"/"+file_name)
        # Copy .xyz file
        generate_sh = orbital_dir+"/"+ OPT + name_input+'.sh'
        shutil.copy('OPT_sample.sh', generate_sh ) 
        # Copy .sh file
        generate_inp = orbital_dir+"/"+OPT+ name_input+'.inp'
        shutil.copy('OPT_sample.inp', generate_inp )
        # Copy .inp file 
        sample_line =    '* xyzfile 0 1 sample.xyz'

        subtitude_line = '* xyzfile 0 1 ' +name_input+'.xyz'
        replace_line_text(generate_inp, sample_line, subtitude_line)


        sample_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca OPT_sample.inp > OPT_sample.out'
        subtitude_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca ' +OPT+ name_input +'.inp' + ' > '+name_input+'.out'
        replace_line_text(generate_sh, sample_line, subtitude_line)

        ############################################
        # For Localization .sh and .inp            #
        ############################################
        generate_sh =  orbital_dir+"/"+ LOC + name_input+'.sh'
        generate_inp = orbital_dir+"/"+ LOC + name_input+'.inp'
        # Copy .sh file
        # Copy .inp file 
        shutil.copy('LOC_sample.sh', generate_sh ) 
        shutil.copy('LOC_sample.inp', generate_inp )
        sample_line =    '* xyzfile 0 1 sample.xyz'

        subtitude_line = '* xyzfile 0 1 ' +OPT+name_input+'_trj.xyz'
        replace_line_text(generate_inp, sample_line, subtitude_line)


        sample_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca LOC_sample.inp > LOC_sample.out'
        subtitude_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca ' + LOC +name_input +'.inp' + ' > '+name_input+'.out'
        replace_line_text(generate_sh, sample_line, subtitude_line)

