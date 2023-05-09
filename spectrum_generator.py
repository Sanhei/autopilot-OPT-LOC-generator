import os
import numpy as np

cumulate = np.array([0,0])
# initial 

for subdir, dirs, files in os.walk("./"):
    print("dirs is",dirs)
    print("subdirs is", subdir)
    for filename in files:
        name_index = filename.split(".abs.")
        print(filename)
        if len(name_index)==2:
            # Find all filename contains .abs.stk
            if name_index[1] == 'stk':
                temp = np.loadtxt(subdir+os.sep+filename)
                print(temp[0])
                cumulate = np.vstack((cumulate, temp) )

# Put all the data into one long array

# We sum all the repeat array, and delete it.
# Idea:
#    1. sort the whole array by the first column.
#    2. sum over all the repeat elements.
#     3. delete the repeat elements
# Sort the array:
# delete the initial value
np.delete(cumulate, 0)
cumulate[cumulate[:, 0].argsort()]

spectrum = []
count = False

index = 0
spectrum.append([cumulate[0][0], cumulate[0][1]])
for i in range(1,len(cumulate)):
    if cumulate[i-1][0]==cumulate[i][0]:
        count=True
    else:
        count=False
    if count:
        spectrum[index][1] += cumulate[i][1]
        continue
    else:
        spectrum.append([cumulate[i][0], cumulate[i][1]])
        index += 1

np.savetxt("Spectrum.txt", spectrum)




# Spectrum Plot
import matplotlib.pyplot as plt

data = np.loadtxt("./Spectrum.txt")
energies = data.T[0]
osc      = data.T[1]

print(osc)

def spectrum(E,osc,sigma,x):
    gE=[]
    for Ei in x:
        tot=0
        for Ej,os in zip(E,osc):
            tot+=os*np.exp(-((((Ej-Ei)/sigma)**2)))
        gE.append(tot)
    return gE

x=np.linspace(280, 300, num=1000, endpoint=True)

sigma=0.4
gE=spectrum(energies,osc,sigma,x)

fig,ax=plt.subplots(figsize=(6,4))
ax.plot(x,gE,"--k", label="sigma: 0.4")


sigma=0.8
gE=spectrum(energies,osc,sigma,x)


ax.plot(x,gE,"--k", label="sigma: 0.8")

gE=spectrum(energies,osc, 1, x)
ax.plot(x,gE,"--r", label="sigma: 1")




for energy,osc_strength in zip(energies,osc):
    ax.plot((energy,energy),(0,osc_strength),c="r")
ax.set_xlabel("Energy (eV)",fontsize=16)
ax.xaxis.set_tick_params(labelsize=14,width=1.5)
ax.yaxis.set_tick_params(labelsize=14,width=1.5)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.5)
ax.set_xlim(280,300)

ax.set_ylabel("Osc. Strength",fontsize=16)
plt.xticks(np.arange(280, 300, 4.0))
plt.tight_layout()
plt.legend()
plt.savefig("Spectrum_PBE0.svg")
