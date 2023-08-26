import pandas as pd

#data import from xls
df = pd.read_excel(r'proper_names_dict.xls')
print(df)

diction = []

#create dict
rowsnum = df.count()[0]
for i in range(0,rowsnum):
    diction.append({'PL':df.iloc[i]['PL'],'EN':df.iloc[i]['EN']})

sample = 'Żywia to bogini Zimy'

for i in diction:
    if i['PL'] in sample:
        sample = sample.replace(i['PL'],i['EN'])
        print(sample)

  
