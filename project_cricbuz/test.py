def rm_spcl(string):
    out_string = ''
    for c in string:
        if not c.isalnum():
            out_string += ' '
        else:
            out_string += c
    out_string = out_string.strip().split()
    temp = out_string
    for val in out_string[:]:
        if val.upper() in ['STADIUM', 'ASSOCIATION', 'GROUND', 'CLUB', 'CRICKET', 'SPORTS', 'PARK', 'NATIONAL', 'THE']:
            out_string.remove(val)
    return out_string

import difflib
def sim_finder(*args):
    name_list = []
    for name in args:
        name_list.append(rm_spcl(name))
    sim = difflib.SequenceMatcher(None, name_list[0], name_list[1])
    return sim.ratio()

def ground_country_mapping():
    try:
        with open('ground_country_mapping.txt', 'r') as f:
            ground_contry = {}
            for line in f:
                pair = line.split(':')
                try:
                    ground_contry[pair[1].strip()] = pair[0].strip()
                except IndexError:
                    print('indexing is not handling efficiently')
    except IOError:
        print('file not found')
    return ground_contry

'''ground = []
country = []
for i in range(1,200):
    s1 = '//table/tr[' + str(i) + ']/td[2]/a/text()'
    s2 = '//table/tr[' + str(i) + ']/td[4]/a/text()'
    temp = response.xpath(s1).extract()
    if not temp:
        s1 = '//table/tr[' + str(i) + ']/td[2]/text()'
    ground.append(response.xpath(s1).extract())
    country.append(response.xpath(s2).extract())

with open('ground_country_mapping.txt', 'a+') as f:
    for key, val in zip(country, ground):
        try:
            f.write(key[0] + ':' + val[0] + '\n')
        except IndexError:
            pass
'''