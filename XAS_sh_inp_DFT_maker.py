import sys
import fileinput
import os
import shutil


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
    shutil.copy('sample.sh',  output_path+file_name+"/"+file_name+'.sh') 
    shutil.copy('sample.inp', output_path+file_name+"/"+file_name+'.inp') 

# This will change a whole line text to another
def replace_line_text(file_name_format, original_line, change_line):
    for i, line in enumerate(fileinput.input(file_name_format, inplace=1)):
        # inplace = 1 means write into the file.
        sys.stdout.write(line.replace(original_line, change_line))


# Calculate orbital numbers
def get_num_carbon_oxgygen(xyz_filename):
    # Get the number of Carbon and oxygen atoms.
    num_orbital = 0
    non_hydrogen = []
    for i, line in enumerate(fileinput.input(xyz_filename)):
        for string in line:
            if string=="C" or string=="O":
                num_orbital += 1
                non_hydrogen.append(i-2)
                #********************************************************************
                # HERE you should keep in mind there are two lines for the number of atoms
                # and the enery output, and the atom index start from 0
                #*********************************************************************
            else:
                continue
    # return an integer
    return num_orbital-1, non_hydrogen
    # Orbital number start from 0;

dir_input = "./xas_input/"
new_dirctory(dir_input)

for subdir, dirs, files in os.walk(dir_input+"reference"):
    for file_name in files:
        name_input = file_name.split(".")[0]        
        # e.g. file name abc.xyz, then, name_input = "abc"
        new_dirctory(output_path+name_input)
        # Create directory
        print(output_path+file_name)
        input_xyz  = dir_input+'reference/'+file_name
        output_dir = output_path+name_input+"/"
        print(output_dir+name_input)
        new_dirctory(output_dir)
        # shutil.copy(dir_input+'xyzfile/'+file_name, output_dir+file_name)
        # copy_files(name_input)
        # Now the file contain .xyz .sh and .inp
        #copy xyz file
        num_orb, orb_index = get_num_carbon_oxgygen(input_xyz)
        # Get the number of orbitals in DFT calculation


        for i in range(num_orb):
            orbital_dir = output_path+name_input+"/"+str(i)
            new_dirctory(orbital_dir)
            # Generate files for each orbital
            shutil.copy(input_xyz, orbital_dir+"/"+file_name)
            # Copy .xyz file
            generate_sh = orbital_dir+"/"+name_input+"_"+str(i)+'.sh'
            shutil.copy('XAS_sample.sh', generate_sh ) 
            # Copy .sh file
            generate_inp = orbital_dir+"/"+name_input+"_"+str(i)+'.inp'
            shutil.copy('XAS_sample.inp', generate_inp )
            # Copy .inp file 

            sample_line =    '*xyzfile 0 1 GEOM_OPT.xyz'
            subtitude_line = '* xyzfile 0 1 ' +name_input+'.xyz'
            replace_line_text(generate_inp, sample_line, subtitude_line)
            
            sample_line =    '%moinp "sample.loc" #Change to the loc file we generate'
            subtitude_line = '%moinp "' +'LOC_'+name_input+'"'
            replace_line_text(generate_inp, sample_line, subtitude_line)

            sample_line =    'orbwin[0] = 0,0,-1,-1'
            subtitude_line = 'OrbWin[0] = '+ str(i) +","+ str(i) +',-1,-1'
            replace_line_text(generate_inp, sample_line, subtitude_line)

            sample_line =    'orbwin[1] = 0,0,-1,-1'
            subtitude_line = 'OrbWin[1] = '+ str(i) +","+ str(i)+',-1,-1'

            replace_line_text(generate_inp, sample_line, subtitude_line)

            sample_line =    'XASLoc[0] = 0,1 '
            subtitude_line = 'XASLoc[0] = '+ str(i)+","+ str(i)

            replace_line_text(generate_inp, sample_line, subtitude_line)

            sample_line =    'XASLoc[1] = 0,1 '
            subtitude_line = 'XASLoc[1] = '+ str(i) +","+ str(i)

            replace_line_text(generate_inp, sample_line, subtitude_line)



            sample_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca 2125.inp > 2125.out '
            subtitude_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca ' + name_input +"_"+str(i)+'.inp' +' > '+name_input+'.out'
            replace_line_text(generate_sh, sample_line, subtitude_line)

            sample_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca_mapspc 2125.out ABSQ -eV 0270 -1300 -n500 -w0.5'
            subtitude_line = '/trinity/shared/easybuild/software/ORCA/5.0.0-gompi-2021a/orca_mapspc ' + name_input+'.out' +' ABS -eV 0270 -1300 -n500 -w0.5'

            replace_line_text(generate_sh, sample_line, subtitude_line)



