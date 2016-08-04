from test import sim_finder, ground_country_mapping
from collections import OrderedDict as od

def rm_spcl(string):
    out_string = ''
    for c in string:
        if not c.isalnum():
            out_string += ' '
        else:
            out_string += c
    out_string = out_string.strip().split()
    return out_string

def delete_unwanted():
    lis = ['WOMEN', 'XI', 'U19']
    for val in table[:]:
        for value in lis:
            if value in val[3].upper().strip() or value in val[4].upper().strip():
                table.remove(val)

def ground_match(name, mapping):
    ret = 0
    for key, value in mapping.items():
        ratio = sim_finder(key, name)
        if ratio >= 0.6:
            ret += 1
            res = value
    if ret:
        return [ret, res]
    else:
        return 0

def delete_incon(selraws):
    #removing games such is D/L result, or abandoned or tied
    checker = 0
    out = []
    for val in selraws:
        value = val.upper()
        if value in baseframe.keys():
            out.append(baseframe[value])
        else:
            checker = 1
    if checker == 1:
        return 0
    else:
        return out



table = []
counter = 0
try:
    with open('pre_tabular.txt', 'r') as f:
        for line in f:
            raw = line.split('==')
            raw += [str(counter)]
            counter += 1
            table.append(list(map(str.strip, raw)))
except IOError:
    print('file pre_tabular.txt not found')

print('size of table before delete_unwanted', len(table))
delete_unwanted()
print('size of table after delete_unwanted', len(table))

with open('val_required.txt', 'r') as f:
    baseframe = {}
    for line in f:
        baseframe[line.split(':')[0].strip()] = line.split(':')[1].strip()


print('size of table before loop for ratio', len(table))
mapping = ground_country_mapping()
for raw in table[:]:
    res = ground_match(raw[5], mapping)
    assert res
    if not res:
        table.remove(raw)
    else:
        raw[5] = res[1].upper()
        out = delete_incon([raw[5], raw[10], raw[11]])
        if not out:
            table.remove(raw)
        else:
            raw[5], raw[10], raw[11] = out
            a = rm_spcl(raw[8])
            b = rm_spcl(raw[9])
            if len(a) >= 5 and len(b) >= 5:
                raw[8] = delete_incon([a[0].strip()]) + [a[1], a[2], a[3]]
                raw[8] = '=='.join(raw[8])
                raw[9] = delete_incon([b[0].strip()]) + [b[1], b[2], b[3]]
                raw[9] = '=='.join(raw[9])
            else:
                table.remove(raw)



print('size of table after ratio', len(table))

#tabular data generation starts here
X = []
for raw in table:
    #every game generate two raws of data
    temp = []
    temp.append([])
    temp.append([])

    #variables for readabiltiy
    t1 = raw[3]
    t2 = raw[4]
    ground = raw[5]
    toss_winner = raw[10]
    match_winner = raw[11]

    #variables for debugging
    toss_winner_d = 0
    match_winner_d = 0

    #doing the cases saperatly to avoid errors
    
    #################################
    #CASE TEAM 1
    if t1 == match_winner:
        temp[0].append(1)
        match_winner_d = 1
    else:
        temp[0].append(0)

    if t1 == ground:
        temp[0].append(1)
    else:
        temp[0].append(0)

    if t1 == toss_winner:
        temp[0].append(1)
        toss_winner_d = 1
    else:
        temp[0].append(0)

    ################################
    #CASE TEAM 2
    if t2 == match_winner:
        temp[1].append(1)
        match_winner_d = 1
    else:
        temp[1].append(0)

    if t2 == ground:
        temp[1].append(1)
    else:
        temp[1].append(0)

    if t2 == toss_winner:
        toss_winner_d = 1
        temp[1].append(1)
    else:
        temp[1].append(0)

    temp[0] += raw
    temp[1] += raw
    #debugging
    if toss_winner_d != 1:
        print('error with toss winner')
    if match_winner_d != 1:
        print('error with match winner')

    X.append(temp[0])
    X.append(temp[1])


with open('tabular.txt', 'w+') as f:
    for val in X:
        string = ''
        #f.write(str(val[0]) + ' ' + str(val[1]) + ' ' + str(val[2]) + '\n')
        for v in val:
            string += str(v) + '=='
        f.write(string + '\n')
