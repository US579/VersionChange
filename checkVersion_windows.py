import re
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def changeVersion(filename):
    file_data = ""
    flag = 1
    pas = 0
    with open(filename, "r", encoding="utf-8") as f1:
        for line in f1:
            # add "##ignore below" will not change the code under this comment
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


def compare(release,tags):
    tags = [i for i in tags if '2020' in i]
    release = [i for i in release if '2020' in i]
    flag = 0
    for i in release:
        if readFile(i,tags) == False:
            flag = 1
            print(f"{bcolors.OKGREEN}{i}{bcolors.ENDC}")

    if flag:
        return False
    return True


def readFile(file,tags):
    map = {}
    flag = 1
    with open(file,'r', encoding="utf-8") as f:
        lis = list(f)
        for i in range(len(lis)):
            version = re.search('^    version: .*',lis[i])
            if version:
                form = re.search('tax-forms-nz.*',lis[i-1])
                if form:
                    formV = lis[i-1].strip('\n').split('.')[-1][:-1]
                    v = lis[i].strip('\n').strip().replace("'",'')
                    map[formV] = v
    # print(map)
    # store = []
    for key in map:
        for j in tags:
            if key+'/' in j:
                if 'ir3' in map and 'ir3nr' in map and 'IR3NR/' in j and 'ir3nr/' in j: continue
                if 'ir3' not in map and 'ir3nr' in map and'IR3/' in j and 'ir3nr/' in j: continue
                # print(j)
                with open(j,'r',encoding='utf-8') as f:
                    fi = list(f)[-1].strip('\n')
                    tags_file = ''.join(fi.split(' '))
                    release_file = ''.join(map[key].split(' '))
                    # if key in store:
                    #     continue
                    if tags_file == release_file: continue
                    flag = 0
                    print()
                    print(f"{bcolors.OKBLUE}tags version:    {bcolors.ENDC}",tags_file)
                    print(f"{bcolors.OKGREEN}release version: {bcolors.ENDC}",release_file)
                    print(f"{bcolors.OKBLUE}{j}{bcolors.ENDC}")
    # print(store)
    if not flag:
        return False
    return True
                    

if __name__ == "__main__":
    try:
        sys.argv[1]
    except:
        print(f"{bcolors.OKBLUE}USEAGE:{bcolors.ENDC}",' python3 version.py <the root absoulte path of compliance-content-nz>"')
        print('For example:')
        print('python3 checkVersion_windows.py /Users/steven.liu/Desktop/MYOB/compliance-content-nz')
        print('If your want to increament all version by 1 add `-i` behind above command')
        sys.exit()

    if not os.path.exists(sys.argv[1]):
        print(f"{bcolors.FAIL}Path is not exists {bcolors.ENDC}")
        sys.exit()

    Noinclude = ['Snippets','Workpapers','Common_Releases','Calculator','Declarations']
    tags,release = findfile(sys.argv[1], 'tags.yml',Noinclude)
    # ******
    tags = ['/'.join(item.split('\\')) for item in tags]
    release = ['/'.join(item.split('\\')) for item in release]
    allpath = tags + release

    try:
        increament = sys.argv[2]
        if increament == '-i':
            for path in allpath:
                changeVersion(path)
        print(f"{bcolors.HEADER}Bump version successfully🚀 🚀 🚀 🚀 🚀{bcolors.ENDC}")
    except:
        pass
    if compare(release,tags):
        print(f"{bcolors.OKGREEN}Pass All Comparison ✅{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}Comparison Failed{bcolors.ENDC}")

