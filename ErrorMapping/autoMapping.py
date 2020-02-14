
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
    df = read_excel(file_name, sheet_name = my_sheet,header=1,keep_default_na=False,)
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
    colDic = {'3':'Ir3','3nr':'IR3NR','4':'IR4','6':'IR6','7':'IR7','8':'IR8','9':'IR9','833':'IR833','reb':'REB - IR526','215':'IR215'}
    # print(row['REB - IR526'])
    # if form == 'all':
    #      print('[[[[[[[[[[[[]]]]]]]]]]]]')
    #     #  print(row['Ir3'])
    # if not row['Ir3'] or row['REB - IR526'] !='NA':
    #     print('==========================')
    # if row['REB - IR526'] !='NA':
    #     print(row['REB - IR526'])
    #     print('[[[[[[[[[[[[]]]]]]]]]]]]')
    if form in ['calc','44','44e','3N+D44',]:return
    if form =='all':
        for item, v in dic[form]:
            # if not row['Ir3'] or row['REB - IR526'] !='NA':
            #     print('==========================')
            with open(item ,"a", encoding="utf-8") as f1:
                f1.write('    '+str(row['Standard codes'])+':\n')
                f1.write('      Standard message: '+row['Standard message']+'\n')
                f1.write('      description: '+row['Description']+'\n')
                if not row[colDic[v]] or row[colDic[v]] !='NA':
                    f1.write('      formsengineField: '+row[colDic[form]]+'\n')
    else:
        # print(form)
        # print(dic[form])
        with open(dic[form], "a", encoding="utf-8") as f1:
            f1.write('    '+str(row['Standard codes'])+':\n')
            f1.write('      Standard message: '+row['Standard message']+'\n')
            f1.write('      description: '+row['Description']+'\n')
            if not row[colDic[v]] or row[colDic[v]] !='NA':
                    f1.write('      formsengineField: '+row[colDic[form]]+'\n')


def wirteTitle(file):
    for i in file:
        with open(i, "a", encoding="utf-8") as f1:
            f1.write('\n  FieldErrorMappings:\n')


if __name__ == "__main__":
    Noinclude = ['Snippets','Workpapers','Common_Releases','Calculator','Declarations']
    tags,release = findfile('/Users/steven.liu/Desktop/VersionChange/ErrorMapping/compliance-content-nz', 'mappings.yml',Noinclude)
    tags = ['/'.join(item.split('\\')) for item in tags if 'ir10' not in item]
    dic = {}
    minorForm = ['4j','8j']
    for i in tags:
        name = i.split('/')[-2][2:]
        if name == '526':dic['reb'] = i
        if name not in minorForm:dic[name] = i
    dic['all'] = [[i,i.split('/')[-2][2:]] for i in tags if i.split('/')[-2][2:] not in minorForm ]
    # wirteTitle(tags)
    print(dic)
    # for i in dic:
    #     print(dic[i])
    # append(dic)
    
