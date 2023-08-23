#################################################
# It zips a list of files in a given directory. #
# It is used on a Windows OS. It could be used  #
# on Linux distro as well just the folder path  #
# var. should be changed.                       #
#################################################

import zipfile, os
from sys import exit

zip_list = ['bacon.txt', 'test.txt', 'sonet29.txt']
folder = 'C:\\Users\\User\\Desktop\\'
zipname = 'test_archive.zip'
os.chdir(folder)

for file in zip_list:
    if zipname:
        new_zip = zipfile.ZipFile('{}'.format(zipname), 'a')
        new_zip.write('{}'.format(file), compress_type=zipfile.ZIP_DEFLATED)

    new_zip = zipfile.ZipFile('{}'.format(zipname), 'w')
    new_zip.write('{}'.format(file), compress_type=zipfile.ZIP_DEFLATED)

new_zip.close()

show_zip_files = zipfile.ZipFile('{}'.format(zipname))
print(show_zip_files.namelist())

exit(0)
