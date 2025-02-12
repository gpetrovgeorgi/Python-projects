##########################################################
# It walks through a given directory, sub-dirs and files #
# printing the file names and their content.             #  
#                                                        #
# It is used on a Windows OS. It could be used           #
# on Linux distro as well just the showin and            #
# dir_to_walkin vars. should be changed.                 #      
##########################################################

import os

dir_to_walkin = 'Some random local directory'
showin = 'C:\\Users\\User\\Downloads\\'+ dir_to_walkin

for folder,subfolder,filename in os.walk(showin):
    print(f"The current folder is {folder} ...")
    for subfolder in subfolder:
        print(f"Subfolder of {folder}: {subfolder} ...")

    for file in filename:
        print(f"This file - {file} is in {folder} ...")

    print('')
