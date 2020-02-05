import re
import os
import sys

def changeVersion(filename):
    file_data = ""
    flag = 1
    pas = 0
    with open(filename, "r", encoding="utf-8") as f1:
        for line in f1:
            # add ##ignore below will not change the code under this sign
            workpaper = re.search('##ignore below',line)
            if workpaper or pas:
                file_data += line
                pas = 1
                continue
            ignore = re.search('^#.*',line.strip())
            if ignore: 
                file_data += line
                continue
            versionNumber = re.search('version: .*',line)
            if flag and versionNumber:
                old = versionNumber.group()
                oldList = old.split(' ')[-1].split('.')
                old = old.split(' ')[-1]
                oldList[-1] = str(int(oldList[-1])+1)
                new = '.'.join(oldList)
                line = line.replace(old, new).strip()+'\n'
                file_data += line
                flag = 0
                continue
            if versionNumber:
                string = versionNumber.group()
                string = string.split(' ')
                oldVersion = string[-1]
                string = string[-1].strip('\'').split('.')
                string[-1] = str(int(string[-1]) + 1)
                newVersion = "'" + '.'.join(string) + "'"
                line = line.replace(oldVersion, newVersion)
            file_data += line
    with open(filename,"w",encoding="utf-8") as f:
        f.write(file_data)


def findfile(start, name, Noinclude):
    lis = []
    lis2 = []
    for relpath, dirs, files in os.walk(start):
        flag = 1 
        for i in Noinclude:
            if flag and i in str(relpath):
                flag = 0
        if flag and name in files:
            full_path = os.path.join(start, relpath, name)
            lis.append(os.path.normpath(os.path.abspath(full_path)))
        if flag:
            if os.path.basename(relpath) == 'Releases':
                lis2.extend([os.path.normpath(os.path.join(start, relpath, i)) for i in files])
    return lis,lis2

    
if __name__ == "__main__":
    try:
        sys.argv[1]
    except:
        print("usage: ./changeVersion_windows <the root absoulte path of compliance-content-nz>")
        print('for example:')
        print('             ./changeVersion_windows /Users/steven.liu/Desktop/MYOB/compliance-content-nz')
        sys.exit()
    Noinclude = ['Snippets','Workpapers','Common_Releases','Calculator','Declarations']
    tags,release = findfile(sys.argv[1], 'tags.yml',Noinclude)
    allpath = tags + release
    try:
        for path in allpath:
            changeVersion(path)
        print('bump version successfully')
    except:
        print('bump version failed')
    
