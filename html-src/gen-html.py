#!/usr/bin/env python
from __future__ import print_function

#outdir = '../html'
pysollib_dir = '../'

import sys, os, re

try: os.mkdir('html')
except: pass
try: os.mkdir('html/rules')
except: pass

pysollib_path = os.path.join(sys.path[0], pysollib_dir)
sys.path[0] = os.path.normpath(pysollib_path)
#print sys.path

from pysollib.mygettext import fix_gettext
fix_gettext()

import pysollib.games
import pysollib.games.special
import pysollib.games.ultra
import pysollib.games.mahjongg

from pysollib.gamedb import GAME_DB
from pysollib.gamedb import GI


files = [
    ('credits.html', 'PySol Credits'),
    ('ganjifa.html', 'PySol - General Ganjifa Card Rules'),
    ('general_rules.html', 'PySol - General Rules'),
    ('glossary.html', 'PySol - Glossary'),
    ('hanafuda.html', 'PySol - Rules for General Flower Card Rules'),
    ('hexadeck.html', 'PySol - General Hex A Deck Card Rules'),
    ('howtoplay.html', 'How to play PySol'),
    ('index.html', 'PySol - a Solitaire Game Collection'),
    ('install.html', 'PySol - Installation'),
    ('intro.html', 'PySol - Introduction'),
    ('license.html', 'PySol Software License'),
    ('news.html', 'PySol - a Solitaire Game Collection'),
    #('rules_alternate.html', 'PySol - a Solitaire Game Collection'),
    #('rules.html', 'PySol - a Solitaire Game Collection'),
    ]

rules_files = [
    #('hanoipuzzle.html', ),
    ('mahjongg.html', 'PySol - Rules for Mahjongg'),
    ('matrix.html', 'PySol - Rules for Matrix'),
    ('pegged.html', 'PySol - Rules for Pegged'),
    ('shisensho.html', 'PySol - Rules for Shisen-Sho'),
    ('spider.html', 'PySol - Rules for Spider'),
    ('freecell.html', 'PySol - Rules for FreeCell'),
    ]
wikipedia_files = [
    ('houseinthewood.html', 'PySol - Rules for House in the Woods'),
    ('fourseasons.html', 'PySol - Rules for Four Seasons'),
    ]

main_header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
<head>
<title>%s</title>
<meta name="license" content="Distributed under the terms of the GNU General Public License">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<body text="#000000" bgcolor="#F7F3FF" link="#0000FF" vlink="#660099" alink="#FF0000">
<img src="images/pysollogo03.gif" alt="">
<br>
'''
main_footer = '''
<p>
<br>
%s
</body>
</html>'''

rules_header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
<head>
<title>%s</title>
<meta name="license" content="Distributed under the terms of the GNU General Public License">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<body text="#000000" bgcolor="#F7F3FF" link="#0000FF" vlink="#660099" alink="#FF0000">
<img src="../images/pysollogo03.gif" alt="">
<br>
'''
rules_footer = '''
<p>
%s
<br>
<a href="../glossary.html">Glossary</a>
<br>
<a href="../general_rules.html">General rules</a>

<p>
<a href="../index.html">Back to the index</a>
</body>
</html>'''

wikipedia_header = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<html>
<head>
<title>%s</title>
<meta name="license" content="Distributed under the terms of the  GNU Free Documentation License">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
</head>
<body text="#000000" bgcolor="#F7F3FF" link="#0000FF" vlink="#660099" alink="#FF0000">
<img src="../images/pysollogo03.gif" alt="">
<br>
'''


def getGameRulesFilename(n):
    if n.startswith('Mahjongg'): return 'mahjongg.html'
    ##n = re.sub(r"[\[\(].*$", "", n)
    n = re.sub(r"[^\w]", "", n)
    n = n.lower() + ".html"
    return n

def gen_main_html():
    for infile, title in files:
        outfile = open(os.path.join('html', infile), 'w')
        print(main_header % title, file=outfile)
        print(open(infile).read(), file=outfile)
        s = '<a href="index.html">Back to the index</a>'
        if infile == 'index.html':
            s = ''
        print(main_footer % s, file=outfile)

def gen_rules_html():
    ##ls = glob(os.path.join('rules', '*.html'))
    rules_ls = os.listdir('rules')
    rules_ls.sort()
    wikipedia_ls = os.listdir('wikipedia')
    wikipedia_ls.sort()

    games = GAME_DB.getGamesIdSortedByName()
    rules_list = []
    files_list = []
    for fn, tt in rules_files:
        rules_list.append(('rules', fn, tt, ''))
        files_list.append(fn)
    for fn, tt in wikipedia_files:
        rules_list.append(('wikipedia', fn, tt, ''))
        files_list.append(fn)
    altnames = []

    # open file of list of all rules
    out_rules = open(os.path.join('html', 'rules.html'), 'w')
    print(main_header % 'PySol - a Solitaire Game Collection', file=out_rules)
    print(open('rules.html').read(), file=out_rules)

    for id in games:
        # create list of rules

        gi = GAME_DB.get(id)

        rules_fn = gi.rules_filename
        if not rules_fn:
            rules_fn = getGameRulesFilename(gi.name)

        if rules_fn in files_list:
            continue

        if rules_fn in rules_ls:
            rules_dir = 'rules'
        elif rules_fn in wikipedia_ls:
            rules_dir = 'wikipedia'
        else:
            print('missing rules for %s (file: %s)' \
                  % (gi.name, rules_fn))
            continue

        ##print '>>>', rules_fn

        title = 'PySol - Rules for ' + gi.name
        s = ''
        if gi.si.game_type == GI.GT_HANAFUDA:
            s = '<a href="../hanafuda.html">General Flower Card rules</a>'
        elif gi.si.game_type == GI.GT_DASHAVATARA_GANJIFA:
            s = '<a href="../ganjifa.html">About Ganjifa</a>'
        elif gi.si.game_type == GI.GT_HEXADECK:
            s = '<a href="../hexadeck.html">General Hex A Deck rules</a>'
        elif gi.si.game_type == GI.GT_MUGHAL_GANJIFA:
            s = '<a href="../ganjifa.html">About Ganjifa</a>'
            #print '***', gi.name, '***'

        rules_list.append((rules_dir, rules_fn, title, s))
        files_list.append(rules_fn)
        #rules_list.append((rules_fn, gi.name))
        print('<li><a href="rules/%s">%s</a>' \
              % (rules_fn, gi.name), file=out_rules)
        for n in gi.altnames:
            altnames.append((n, rules_fn))

    print('</ul>\n' + \
          main_footer % '<a href="index.html">Back to the index</a>', file=out_rules)

    # create file of altnames
    out_rules_alt = open(os.path.join('html', 'rules_alternate.html'), 'w')
    print(main_header % 'PySol - a Solitaire Game Collection', file=out_rules_alt)
    print(open('rules_alternate.html').read(), file=out_rules_alt)
    altnames.sort()
    for name, fn in altnames:
        print('<li> <a href="rules/%s">%s</a>' \
              % (fn, name), file=out_rules_alt)
    print('</ul>\n' + \
          main_footer % '<a href="index.html">Back to the index</a>', file=out_rules_alt)

    # create rules
    for dir, filename, title, footer in rules_list:
        outfile = open(os.path.join('html', 'rules', filename), 'w')
        if dir == 'rules':
            print((rules_header % title), file=outfile)
        else: # d == 'wikipedia'
            print((wikipedia_header % title), file=outfile)
        print(open(os.path.join(dir, filename)).read(), file=outfile)
        print(rules_footer % footer, file=outfile)


gen_main_html()
gen_rules_html()



