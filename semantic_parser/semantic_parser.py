from string import lower
from re import sub
import csv

def _alphanum(x):
    """
    Given a string of arbitrary characters x, returns a string containing 
    only alphanumeric characters.
    >>> _alphanum("Hello World2!")
    'helloworld2'
    """
    return lower(sub(r'\W+', '', str(x)))

def _alphanum_list(x):
    """
    Given a list of strings containing arbitrary characters x, returns a
    list of strings containing only alphanumeric characters.
    >>> _alphanum_list(["Hello World!", "Hello World2!"])
    ['helloworld', 'helloworld2']
    """
    return [_alphanum(y) for y in x]

def _silent_idx(x, y):
    """
    Given a list x and an object y, returns the index of y in x. Otherwise
    return a None without raising any exceptions.
    >>> _silent_idx([1,2,3,4], 2)
    1
    >>> _silent_idx([1,2,3,4], 5)
    """
    if y in x:
        return x.index(y) 
    else:
        return None

def _soft_in(x, y):
    """
    Given a list x and an object y, checks if y is in x ignoring case
    as well as non-alphanumeric characters.
    >>> _soft_in(["Hello World!", "Hello Joe!"], "hello joe")
    True
    >>> _soft_in(["Hello World!", "Hello Joe!"], "hello moe")
    False
    """
    return _alphanum(y) in _alphanum_list(x)

def _soft_idx(x, y):
    """
    Given a list x and an object y, returns the index of y in x ignoring
    case as well as non-alphanumeric characters.
    >>> _soft_idx(["Hello World!", "Hello Joe!"], "hello joe")
    1
    >>> _soft_idx(["Hello World!", "Hello Joe!"], "hello moe")
    """
    return _silent_idx(_alphanum_list(x), _alphanum(y))

def _silent_get(x, i):
    """
    Given a list x and an index i, returns the element from the list
    at index i if i is valid. Otherwise, return empty string - ''.
    >>> _silent_get([1,2,3,4], 2)
    3
    >>> _silent_get([1,2,3,4], 5)
    ''
    """
    if i < len(x):
        return x[i]
    else:
        return ''

def _find_alias(line, aliases):
    """
    Given a line and a list of aliases, returns the index of first
    occurrence of any of the alias in the list.
    >>> _find_alias(["A", "B", "C", "D"], ["b", "bee", "B"])
    1
    >>> _find_alias(["A", "B", "C", "D"], ["e", "eee", "E"])
    """
    for alias in aliases:
        if _soft_in(line, alias):
            return _soft_idx(line, alias)

def reader(fname, sd):
    """
    Given a csv file and a semantic dictionary, yields valid data lines.
    Valid data lines are anything under a valid header and the end of the
    given csv file and contain all of the mandatory fields as defined in 
    the semantic dictionary. Header is a line somewhere near the beginning 
    of the csv file that comprises of fields as defined in the semantic 
    dictionary. A field can be mandatory or optional, has a unique identifier 
    and as many aliases. For instance "price", "price($)", "rates", "cost" 
    and anything else that a real-world invoice in csv format dares to throw
    at you.

    Set everything up: ::

        >>> from semantic_parser import reader
        >>> i = (("item", True), ["item", "type", "flavour"])
        >>> p = (("price", True), ["rate", "price", "unit price"])
        >>> q = (("quantity", False), ["quantity"])
        >>> t = (("total", True), ["total", "sum"])
        >>> r = (("remarks", False), ["remarks", "comments"])
        >>> sd = dict([i, p, q, t, r])

    Set-up the pretty printer: ::

        >>> import pprint
        >>> pp = pprint.PrettyPrinter(indent=4)

    Parse Acme Sweets: ::

        >>> lines = [line for line in reader("test/acme_sweets.csv", sd)]
        >>> pp.pprint(lines)
        [   {   ('item', True): 'A',
                ('price', True): '0.15',
                ('quantity', False): '5',
                ('remarks', False): 'Promotion',
                ('total', True): '0.75'},
            {   ('item', True): 'B',
                ('price', True): '2',
                ('quantity', False): '',
                ('remarks', False): '',
                ('total', True): '0'},
            {   ('item', True): 'C',
                ('price', True): '20',
                ('quantity', False): '1',
                ('remarks', False): '',
                ('total', True): '20'}]

    Parse Acme Pies: ::

        >>> lines = [line for line in reader("test/acme_pies.csv", sd)]
        >>> pp.pprint(lines)
        [   {   ('item', True): 'A',
                ('price', True): '0.15',
                ('quantity', False): '5',
                ('remarks', False): 'Promotion',
                ('total', True): '0.75'},
            {   ('item', True): 'B',
                ('price', True): '2',
                ('quantity', False): '',
                ('remarks', False): '',
                ('total', True): '0'},
            {   ('item', True): 'C',
                ('price', True): '20',
                ('quantity', False): '1',
                ('remarks', False): '',
                ('total', True): '20'}]

    Parse Acme Drinks: ::

        >>> lines = [line for line in reader("test/acme_drinks.csv", sd)]
        >>> pp.pprint(lines)
        [   {   ('item', True): 'X',
                ('price', True): '0.15',
                ('quantity', False): '5',
                ('total', True): '0.75'},
            {   ('item', True): 'Y',
                ('price', True): '2',
                ('quantity', False): '3',
                ('total', True): '6'}]
    """
    with open(fname, 'rb') as f:
        rdr = csv.reader(f)
        hdr = None
        for l in rdr:
            # header has not been found
            if not hdr:
                # for each field defined in the semantic dictionary,
                # search for one of the aliases to be present in the line
                x = {k: _find_alias(l,sd[k]) for k in sd}
                # have we found a header? essentially: have we found a
                # match for one of the aliases of each mandatory field?
                if all([x[k] is not None for k in x if k[1]]):
                    hdr = x
                    continue
            # header has been found
            else:
                # check of one or more mandatory columns are missing?
                if any([_silent_get(l,hdr[k]) is '' for k in hdr if k[1]]):
                    continue
                # yields a dictionary with field identifier as keys
                yield {k: l[hdr[k]] for k in hdr if hdr[k] is not None}
