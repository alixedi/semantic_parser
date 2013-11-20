.. Semantic Parser documentation master file, created by
   sphinx-quickstart on Wed Nov 20 10:43:13 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Semantic Parser's documentation!
===========================================

Introduction
------------

Get tabular data out of real-world spreadsheets.


Problem Statement
-----------------

So you need to parse spreadsheets lets say invoices from snack vendors - lots of them if you happen to have an open pantry at your startup. Invariably, the first step would be to convert these spreadsheets in CSV resulting in specimen such as:

Specimen-A: ::

    'Acme Sweets'                                        ''      ''          ''       ''
    'Shop No. 12, ABC Road.'                             ''      ''          ''       ''
    ''                                                   ''      ''          ''       ''
    'Item'                                               'Rate'  'Quantity'  'Total'  'Remarks'
    'A'                                                  '0.15'  '5'         '0.75'   'Promotion'
    'B'                                                  '2'     ''          '0'      ''
    'C'                                                  '20'    '1'         '20'     ''
    ''                                                   ''      ''          ''       ''
    '* all rates are in USD unless otherwise specified'  ''      ''          ''       ''

Specimen-B: ::

    'Acme Pies'                                          ''          ''       ''       ''
    'Shop No. 121, XYZ Road.'                            ''          ''       ''       ''
    ''                                                   ''          ''       ''       ''
    'Type'                                               'Quantity'  'Price'  'Total'  'Comments'
    'A'                                                  '5'         '0.15'   '0.75'   'Promotion'
    'B'                                                  ''          '2'      '0'      ''
    'C'                                                  '1'         '20'     '20'     ''
    ''                                                   ''          ''       ''       ''
    '* all rates are in USD unless otherwise specified'  ''          ''       ''       ''

Specimen-C: ::

    'Acme Drinks'             ''          ''            ''
    'Shop No. 21, ZZZ Road.'  ''          ''            ''
    ''                        ''          ''            ''
    'Flavour'                 'Quantity'  'Unit Price'  'Sum'
    'X'                       '5'         '0.15'        '0.75'
    'Y'                       '3'         '2'           '6'


Following observation holds true about these spreadsheets from the wild:

1. Valid data lies between the header and the footer or between the header and the end of file.
2. Header as well as data comprises fields that can be mandatory (e.g. Rate) or optional (e.g. Remarks).
3. Each unique field can have many aliases (e.g. Rate, Price for the same field).
4. Order of the fields may vary from spreadsheet to spreadsheet.


Solution
--------

Setting up:

	>>> from semantic_parser import reader
	>>> semantic_dictionary = {("item", True):      ["item", "type", "flavour"],\
	                           ("price", True):     ["rate", "price", "unit price"],\
	                           ("quantity", False): ["quantity"],\
	                           ("total", True):     ["total", "sum"],\
	                           ("remarks", False):  ["remarks", "comments"]}
	>>> import pprint
	>>> pp = pprint.PrettyPrinter(indent=4)

Specimen-A:

	>>> lines = [line for line in reader("test/acme_sweets.csv", semantic_dictionary)]
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

Specimen-B:

	>>> lines = [line for line in reader("test/acme_pies.csv", semantic_dictionary)]
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

Specimen-C:

	>>> lines = [line for line in reader("test/acme_drinks.csv", semantic_dictionary)]
	>>> pp.pprint(lines)
	[   {   ('item', True): 'X',
	        ('price', True): '0.15',
	        ('quantity', False): '5',
	        ('total', True): '0.75'},
	    {   ('item', True): 'Y',
	        ('price', True): '2',
	        ('quantity', False): '3',
	        ('total', True): '6'}]

Installation
------------
I am still working on the pip setup for this project. Meanwhile, the installation is still super-simple. Just put semantic_parser.py somewhere on your PYTHON_PATH and you should be good to go.

Future Work
-----------
Lost of ideas on how to take this forward. The most intriguing one: In order to make this true to the word "semantic", there is value in talking to a thesaurus API in order to populate the semantic dictionary (semi?)automatically.


.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

