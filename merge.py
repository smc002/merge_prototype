import sys
import re

script, o_file = sys.argv

ops = ['at', 'dt', 'al', 'dl']
class vi():
    def __init__(self, lines):
        for op in ops:
            exec('self.{}=[]'.format(op))
        for l in lines:
            for op in ops:
                exec('if l[:3] == "{}:": self.{}.append(l[:-1])'.format(op, op))

# read file
with open(o_file, 'r') as f:
    lines = f.readlines()
s1 = lines.index('\n')
s2 = lines.index('\n', s1+1)
base_vi = vi(lines[:s1])
yours_vi = vi(lines[s1:s2])
theirs_vi = vi(lines[s2:])
result_vi = vi(lines[s1:])

same_dls = []
for y_dl in yours_vi.dl:
    if y_dl in theirs_vi.dl:
        same_dls.append(y_dl)

def fit(als, terminals):
    fits = ['', '']
    fits_terminals = ['', '']
    pattern = [None, None]

    # to match 'al:<terminal0>-xxx'
    pattern[1] = re.compile(r'(?<=\Aal:{}-).+(?=\Z)'.format(terminals[0]))
    # to match 'al:xxx-<terminal1>'
    pattern[0] = re.compile(r'(?<=\Aal:).+(?=-{}\Z)'.format(terminals[1]))
    for i in range(2):
        for al in als:
            match = pattern[i].search(al)
            if match:
                fits[i] = al
                fits_terminals[i] = match.group()
    return fits, fits_terminals

def merge(al0, al1, result_al):
    print('Merge al {} and {} to {}'.format(al0, al1, result_al))
    result_vi.al.remove(al0)
    result_vi.al.remove(al1)
    result_vi.al.append(result_al)

for s in same_dls:
    original_terminals = s[3:].split('-')
    y_fits, y_fits_terminals = fit(yours_vi.al, original_terminals)
    t_fits, t_fits_terminals = fit(theirs_vi.al, original_terminals)

    if y_fits[0] != '' and t_fits[1] != '':
        result_al = 'al:' + y_fits_terminals[0] + '-' + t_fits_terminals[1]
        merge(y_fits[0], t_fits[1], result_al)

    if y_fits[1] != '' and t_fits[0] != '':
        result_al = 'al:' + t_fits_terminals[0] + '-' + y_fits_terminals[1]
        merge(y_fits[1], t_fits[0], result_al)

def simplify(ats, dts):
    for at in ats:
        for dt in dts:
            if at[3:] == dt[3:]:
                ats.remove(at)
                dts.remove(dt)
                print('{} and {} is removed.'.format(at, dt))
                simplify(ats, dts)

simplify(base_vi.at, result_vi.dt)
simplify(base_vi.al, result_vi.dl)

# write to 'result.txt'
def write_fun(li):
    for l in li:
        f.write(l+'\n')

with open('result.txt', 'w') as f:
    write_fun(base_vi.at)
    write_fun(base_vi.al)
    write_fun(result_vi.dl)
    write_fun(result_vi.dt)
    write_fun(result_vi.at)
    write_fun(result_vi.al)
