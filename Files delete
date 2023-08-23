#####################################################
# It searches and deletes a list.                   #
# It is used on a Windows OS. It could be used      #
# on Linux distros as well just the os.chdir method #
# value and desktop var. should be changed          #
#####################################################

import shutil, os

os.chdir('C:\\')

list = ['bacon.txt', 'test.txt', 'sonet29.txt']

desktop = 'C:\\Users\\User\\Desktop\\'

for i in list:
    os.unlink('{}{}'.format(desktop,i))
    a = os.path.exists('{}{}'.format(desktop,i))
    if not a:
        print(f"{i} is deleted !")
    else:
        print(f"Error, nothing was deleted !")
