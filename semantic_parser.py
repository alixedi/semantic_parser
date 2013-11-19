from string import lower
from re import sub
import csv

# remove non-alphanumeric characters
fa = lambda x: lower(sub(r'\W+', '', str(x)))
fas = lambda x: [fa(y) for y in x]

# list index sans exception
fi = lambda l,x: l.index(x) if x in l else None

# case-insensitive, alphanumeric in and index
fx = lambda l,x: fi(fas(l), fa(x))
fin = lambda l,x: fa(x) in fas(l)

# list access that defaults to ''
fl = lambda l,x: l[x] if x < len(l) else ''


def idx(line,vals):
    '''
    Take a line and a list of valid values returns the index of first
    occurrence of any of the values in the list.
    '''
    for val in vals:
        if fin(line, val):
            return fx(line, val)

def datareader(fname, sd):
    '''
    Takes a file and semantic dictionary and yields data lines.
    'Data' here is whatever lies underneath a header whereas a header 
    is a line that contains one of the valid titles of all mandatory 
    columns as defined in the semantic dict.
    '''
    with open(fname, 'rb') as f:
        rdr = csv.reader(f)
        hdr = None
        for l in rdr:
            if not hdr:
                x = {k: idx(l,sd[k]) for k in sd}
                # have we found a header?
                if all([x[k] is not None for k in x if k[1]]):
                    hdr = x
                    continue
            else:
                # one or more mandatory columns are missing?
                if any([fl(l,hdr[k]) is '' for k in hdr if k[1]]):
                    continue
                yield {k: l[hdr[k]] for k in hdr if hdr[k] is not None}
