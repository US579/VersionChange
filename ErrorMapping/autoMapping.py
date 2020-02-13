
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
    file_name = '2020IRerrors.xlsx' 
    df = read_excel(file_name, sheet_name = my_sheet,header=1)
    # print(df['minorFormType'])

    for index, row in df.iterrows():
        if 'CFC' in str(row['minorFormType']).split(','): continue
        print([i.strip() for i in str(row['minorFormType']).split(',')])
        for form in [i.strip() for i in str(row['minorFormType']).split(',')]:
            # print(form)
 
            form2mappings(dic,form.lower(),row)
            # pass
       
def form2mappings(dic,form,row):
    # print('minorFormType:',str(row['minorFormType']).split(','))
    # print('Standard codes:',row['Standard codes'])
    # print('Description:',row['Description'])
    # print('Standard message:',row['Standard message'])
    print(row['Ir3'])
    if form in ['calc','44','44e','3N+D44',]:return
    if form =='all':
        for item in dic[form]:
            with open(item ,"a", encoding="utf-8") as f1:
                # f1.write('    '+str(row['Standard codes'])+':\n')
                # f1.write('      Standard message: '+row['Standard message']+'\n')
                # f1.write('      description: '+row['Description']+'\n')
                pass
    else:
        print(form)
        print(dic[form])
        with open(dic[form], "a", encoding="utf-8") as f1:
            # f1.write('    '+str(row['Standard codes'])+':\n')
            # f1.write('      Standard message: '+row['Standard message']+'\n')
            # f1.write('      description: '+row['Description']+'\n')
            pass

def wirteTitle(file):
    for i in file:
        with open(i, "a", encoding="utf-8") as f1:
            f1.write('\n  FieldErrorMappings:\n')


if __name__ == "__main__":
    Noinclude = ['Snippets','Workpapers','Common_Releases','Calculator','Declarations']
    tags,release = findfile('/Users/steven.liu/Desktop/VersionChange/ErrorMapping/compliance-content-nz', 'mappings.yml',Noinclude)
    tags = ['/'.join(item.split('\\')) for item in tags if 'ir10' not in item]
    dic = {}
    for i in tags:
        if i.split('/')[-2][2:] == '526':
            dic['reb'] = i
        dic[i.split('/')[-2][2:]] = i
    dic['all'] = tags
    # wirteTitle(tags)
    print(dic)
    # for i in dic:
    #     print(dic[i])
    append(dic)
    
