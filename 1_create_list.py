import glob
import pprint

vaultLocation = r'D:\_Vault\**\*.md' # <= CHANGE THIS

# Please avert your eyes from this monstrosity

# search all files inside a specific folder
# *.* means file name with any extension

with open("list.txt",'w') as file:
    pass
file.close()
file = open("list.txt", "a", encoding='utf-8')

for list in glob.glob(vaultLocation, recursive=True):
    file.writelines(list + "\n")
    pprint.pprint(list)

file.close()