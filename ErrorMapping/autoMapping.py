from pandas import read_excel
import re
import os
import sys

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

def append(dic):
    my_sheet = 'errors'
    file_name = 'errors.xlsx' 
    df = read_excel(file_name, sheet_name = my_sheet,header=1,keep_default_na=False,)
    for index, row in df.iterrows():
        if 'CFC' in str(row['minorFormType']).split(','): continue
        for form in [i.strip() for i in str(row['minorFormType']).split(',')]:
            form2mappings(dic,form.lower(),row)
       
def form2mappings(dic,form,row):
    colDic = {'3':'Ir3','3nr':'IR3NR','4':'IR4','6':'IR6','7':'IR7','8':'IR8','9':'IR9','833':'IR833','526':'REB - IR526','reb':'REB - IR526','215':'IR215'}
    if form in ['calc','44','44e','3N+D44',]:return
    if form =='all':
        for item, v in dic[form]:
            with open(item ,"a", encoding="utf-8") as f2:
                f2.write('    '+str(row['Standard codes'])+':\n')
                f2.write('      standardMessage: '+'"'+row['Standard message']+'"'+'\n')
                f2.write('      description: '+'"'+row['Description']+'"'+'\n')
                if not row[colDic[v]] or row[colDic[v]] =='NA':
                    continue
                f2.write('      formsengineField: '+'"'+row[colDic[v]]+'"'+'\n')
    else:
        with open(dic[form], "a", encoding="utf-8") as f1:
            f1.write('    '+str(row['Standard codes'])+':\n')
            f1.write('      standardMessage: '+'"'+row['Standard message']+'"'+'\n')
            f1.write('      description: '+'"'+row['Description']+'"'+'\n')
            if not row[colDic[form]] or row[colDic[form]] =='NA':
                return 
            f1.write('      formsengineField: '+'"'+row[colDic[form]]+'"'+'\n')


def wirteTitle(file):
    for i in file:
        with open(i, "a", encoding="utf-8") as f1:
            f1.write('\n  FieldErrorMappings:\n')


if __name__ == "__main__":
    try:
        sys.argv[1]
        sys.argv[2]
    except:
        print('usage: python3 autoMapping.py <year> <the absoult path to your compliance-content-nz>')
        sys.exit()
    Noinclude = ['Snippets','Workpapers','Common_Releases','Calculator','Declarations']
    tags,release = findfile(sys.argv[2], 'mappings.yml',Noinclude)
    #compatible to windows path
    tags = ['/'.join(item.split('\\')) for item in tags if 'ir10' not in item]
    dic = {}
    minorForm = ['4j','8j']
    for i in tags:
        name = i.split('/')[-2][2:]
        if name == '526':dic['reb'] = i
        if name not in minorForm and sys.argv[1] in i:dic[name] = i
    dic['all'] = [[i,i.split('/')[-2][2:]] for i in tags if i.split('/')[-2][2:] not in minorForm and sys.argv[1] in i]
    wirteTitle(tags)
    append(dic)

