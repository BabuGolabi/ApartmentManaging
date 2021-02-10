# -*- coding: utf-8 -*-
"""
    Babu Golabi Team ;)
"""

# Libraries

from khayyam import *
import csv, os
import pandas as pd

# Initial Config

div_method = {
    'equal': 'one',
    'number of residents': 'residents',
    'size of area': 'area',
    'number of parkings': 'parkings',
    }

question_list = {
    'admin id': [],
    'id for taraz mali': [],
    'query': [
        'append',
        'mojoodi',
        'Taraz Mali',
        'soorat hesab',
        'sahm bakhshha',
        'cumsum plot',
        'forecast',
        'exit',
        ],
    'time': [],
    'category': [
        'Ghabz',
        'asansor',
        'nezafat',
        'parking',
        'tamirat',
        'other',
        'sharj',
        ],
    'sahm bakhshha':['by category','by sub category'],
    'cumsum plot': ['normal', 'comparable'],
    'sub category': ['Water', 'gaz', 'bargh', 'avarez'],
    'amount': [],
    'related unit': [],
    'div': list(div_method.keys()),
    'description': [],
    'amount of sharj': [],
    'unit': [],
    'start time': [],
    'end time': [],
    'related idS': [],
    'related category': [],
    'Start time': [],
    'End time': [],
    'Start Time':[],
    'End Time':[],
    'Related category':[]
    }

question_next = {
    'admin id': 'query',
    'query': {
        'append': 'time',
        'Taraz Mali': 'id for taraz mali',
        'mojoodi':'query',
        'soorat hesab': 'start time',
        'sahm bakhshha': 'sahm bakhshha',
        'cumsum plot': 'cumsum plot',
        'forecast':'query',
        },
    'amount of sharj': 'unit',
    'id for taraz mali': 'query',
    'time': 'category',
    'start time': 'end time',
    'end time': 'query',
    'category': {
        'asansor': 'amount',
        'nezafat': 'amount',
        'parking': 'amount',
        'tamirat': 'amount',
        'other': 'amount',
        'Ghabz': 'sub category',
        'sharj': 'amount of sharj',
        },
    'unit': 'description',
    'sub category': 'amount',
    'amount': 'related unit',
    'related unit': 'div',
    'div': 'description',
    'description': 'query',
    'cumsum plot': {'normal': 'Start time', 'comparable': 'Start Time'},
    'sahm bakhshha':{'by category': 'query', 'by sub category': 'query'},
    'Start Time': 'End Time',
    'Start time': 'End time',
    'End Time':'Related category',
    'End time': 'related idS',
    'related idS': 'related category',
    'related category': 'query',
    'Related category': 'query'
    }

question_function = {
    'query': {
        'exit': 'break',
        'forecast': 'forecast()',
        'mojoodi': 'mojoodi()'
        },
    'sahm bakhshha': {'by category': 'sahm_bakhshha()',
                      'by sub category': 'sahm_bakhshha2()'},
    'admin id': 'data["admin id"]=x',
    'time': 'time(x)',
    'start time': 'tmp["start"]=x',
    'Start Time': 'tmp["start"]=x',
    'end time': 'tmp["end"]=x;soorat_hesab(tmp["start"],tmp["end"])',
    'category': 'data["category"]=x',
    'sub category': 'data["sub category"]=x',
    'amount': 'data["amount"]=-int(x)',
    'amount of sharj': 'data["amount"]=x',
    'related unit': 'related_unit(x)',
    'description': 'data["description"]=x;save()',
    'id for taraz mali': 'taraz_mali(x)',
    'div': 'data["div"] = x',
    'unit': "data['related unit']=[x]",
    'Start time': 'tmp["start"]=x',
    'End time': 'tmp["end"]=x',
    'End Time': 'tmp["end"]=x',
    'Related category':'related_category(x);cumsum_plot2(tmp["start"],tmp["end"],tmp["related category"])',
    'related idS': 'related_idS(x)',
    'related category': 'related_category(x);cumsum_plot(tmp["start"]'
    ',tmp["end"],tmp["related idS"],tmp["related category"])'
    }

q = 'admin id'  # First Question

data = {
    'admin id': '',
    'time': '',
    'category': '',
    'sub category': '###',
    'amount': '',
    'related unit': '',
    'div': 'equal',
    'description': ''
    }
# tmp for using temporary datas
tmp = {}

# Functions

def time(x):
    global data
    if x == 'now':
        x = JalaliDate.today()
    data['time'] = x


def taraz_mali(x):
    d2 = pd.read_csv('sahm.csv')
    suum = d2.groupby('id').aggregate({'sahm': 'sum'})
    print("\n→ " + str(suum.loc[x, 'sahm']))


def soorat_hesab(start, end):
    d2 = pd.read_csv('data.csv')
    d2 = d2.sort_values('time')
    choisen = d2[(d2.time >= start) & (d2.time <= end)]
    choisen.to_csv('soorathesab__'+start+"__"+end+'.csv')


def sahm_bakhshha():
    d1 = pd.read_csv('data.csv')
    d1 = d1[d1['category'] != 'sharj']
    part = d1.groupby('category').aggregate({'amount': 'sum'})
    m = part.sum(axis=0)[0]
    part['part'] = part['amount'] / m
    part = part.reset_index()
    print()
    print(part[['category', 'part']])


def sahm_bakhshha2():
    d1 = pd.read_csv('data.csv')
    d1 = d1[d1['sub category'] != '###']
    part = d1.groupby('sub category').aggregate({'amount': 'sum'})
    m = part.sum(axis=0)[0]
    part['part'] = part['amount'] / m
    part = part.reset_index()
    print()
    print( part[['sub category', 'part']])


def mojoodi():
    df = pd.read_csv("data.csv")
    print("\n→ " + str(sum(df['amount'])))


def cumsum_plot(start, end,
        i = ['id1', 'id2', 'id3', 'id4', 'id5', 'id6', 'id7', 'id8', 'id9'],
        category = ['Ghabz', 'asansor', 'nezafat', 'parking', 'tamirat', 'other']
        ):
    import matplotlib.pyplot as plt
    d1 = pd.read_csv('sahm.csv')
    data_filtered = d1.loc[d1['category'].isin(category)]
    data_filtered = data_filtered.loc[data_filtered['id'].isin(i)]
    data_filtered = data_filtered[(data_filtered.time >= start)
                                  & (data_filtered.time <= end)]
    #making costs all posttive 
    data_filtered['sahm']=data_filtered['sahm'].apply(lambda x:-x)
    data_filtered['cumsum'] = data_filtered['sahm'].cumsum()
    (fig, ax) = plt.subplots()
    data_filtered.plot(x='time', y='cumsum', ax=ax, figsize=(10, 10))
    plt.show()


def cumsum_plot2(start,end,category):
    import matplotlib.pyplot as plt
    df = pd.read_csv('data.csv')
    data_filtered = df[(df.time >= start) & (df.time <= end)]
    #making costs all posttive 
    data_filtered['amount'] = data_filtered['amount'].apply(lambda x: -x)
    part = data_filtered.groupby("category").aggregate({"amount":"cumsum"})
    part["time"] = df["time"]
    part["category"] = df["category"]
    fig, ax = plt.subplots()
    for i in category:
        x = part[part["category"]==i]
        x = x.rename(columns={'amount':i})
        x.plot(x = "time", y = i, ax = ax, figsize = (10, 10), title = "cumsum")
    plt.show()


def forecast():
    df = pd.read_csv("data.csv")
    df = df[df['category'] != 'sharj']
    from datetime import datetime
    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d") 
        return abs((d2 - d1).days)
    #h=date of last cost
    h = (len(df['time']))
    #z=days between dayts
    z = days_between(df.iloc[0, 1], df.iloc[h - 1, 1])
    #c=months
    c = z / 30
    #count_id=all ids 
    count_id=len(pd.read_csv("init.csv")['name'])
    #a=sum of costs/months/count of ids
    a = (sum(df['amount']) / c /count_id)
    #t=tavarom chnd sal ghbl
    t = (12, 22, 31, 35, 16, 12, 9, 10, 21, 41)
    n = (((sum(t) / len(t)) + 100) / 100)
    m = round(-(a * n),2)
    print("\n→ " + str(m))


def related_unit(n):
    global data
    a = []
    for i in range(int(n)):
        x = input()
        a.append(x)
    data['related unit'] = a


def related_idS(n):
    global tmp
    a = []
    for i in range(int(n)):
        x = input()
        a.append(x)
    tmp['related idS'] = a


def related_category(n):
    global tmp
    a = []
    for i in range(int(n)):
        x = input()
        a.append(x)
    tmp['related category'] = a


def div(name, amount, method, d):
    d = d[div_method[method]]
    return float(d[name]) / sum(d) * float(amount)


def save_csv(path, d):
    path = './' + path
    if not os.path.isfile(path):
        with open(path, 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile, dialect = 'excel')
            writer.writerow(list(d.keys()))
    with open(path, 'a', newline = '') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = d.keys())
        writer.writerow(d)


def save():
    global data
    save_csv('data.csv', data)
    df = pd.read_csv('init.csv')
    all_name = df[df['name'].isin(data['related unit'])].to_dict(orient = 'list')
    all_name['one'] = [1] * len(all_name['name'])
    i = 0
    # creating sahm.csv
    for name in data['related unit']:
        save_csv('sahm.csv', {
            'id': name,
            'time': data['time'],
            'category': data['category'],
            'sub category': data['sub category'],
            'amount': data['amount'],
            'sahm': div(i, data['amount'], data['div'], all_name)
            })
        i = i + 1
        #reseting data
    data = {
        'admin id': data['admin id'],
        'time': '',
        'category': '',
        'sub category': '###',
        'amount': '',
        'related unit': '',
        'div': 'equal',
        'description': ''
        }   

# Get Input

while True:
    print('\n-------------------------')
    i = 1
    for t in question_list[q]:
        if i == 1:
            print()
        print(str(i) + ' - ' + t.title())
        i = i + 1
    x = input('Enter ' + q.title() + ': ')
    if len(question_list[q]) > 0:
        x = question_list[q][int(x) - 1]
        if q in question_function:
            if x in question_function[q]:
                if question_function[q][x] == 'break':
                    break
                else:
                    exec(question_function[q][x])
            elif type(question_function[q]) == type(''):
                exec(question_function[q])
    else:
        if q in question_function:
            exec(question_function[q])
    if type(question_next[q]) == type(''):
        q = question_next[q]
    else:
        q = question_next[q][x]