#!/usr/bin/env python
import os
import pdb
import re
import sys
import toolframe
import xml.etree.ElementTree as ET

from optparse import *

# ---------------------------------------------------------------------------
def xml_attredit(argv):
    """attredit - edit attribute values in XML files

    usage: xmltool attredit [-d] -a attrib -e ... <filename> <filename> ...

    -a     which attribute to edit
    -d     run under python debugger
    -e     edits to make

    Result is written to stdout.
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    p.add_option('-a', '--attr',
                 action='store', default=None, dest='attrib',
                 help='attribute to edit')
    p.add_option('-e', '--edit',
                 action='append', default=None, dest='edits',
                 help='edit(s) to make on the input')
    p.add_option('-o', '--output',
                 action='store', default=None, dest='output',
                 help='write to file OUTPUT')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()

    ehash = {}
    for e in o.edits:
        q = e.split(e[1])
        ehash[q[1]] = q[2]

    for filename in a:
        X = ET.parse(filename)
        for el in X.iter():
            if o.attrib in el.attrib.keys():
                # -- do the edit
                ebuf = el.attrib[o.attrib]
                for eval in ehash.keys():
                    ebuf = ebuf.replace(eval, ehash[eval])

                el.attrib[o.attrib] = ebuf

        X.write(sys.stdout)
        print("")
    # pass
    

# ---------------------------------------------------------------------------
def xml_attrlist(argv):
    """attrlist - list the occurences of a specified attribute

    usage: xmltool attrlist [-d] -a attrib <filename> <filename> ...

    -a     which attribute to list
    -d     run under python debugger

    Matching attributes are listed.
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    p.add_option('-a', '--attr',
                 action='store', default=None, dest='attrib',
                 help='attribute to edit')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()

    for filename in a:
        X = ET.parse(filename)
        elements = []
        for el in X.iter():
            elements.append(el)
            
        for el in X.iter():
            if o.attrib in el.attrib.keys():
                path = geneaology(el, elements, X)
                print("%s -> %s: %s" % (path, o.attrib, el.attrib[o.attrib]))


# ---------------------------------------------------------------------------
def geneaology(el, elements, root):
    rval = ''
    p = find_parent(el, elements)
    while p not in root._children:
        rval = '%s > ' % (p.tag) + rval
        p = find_parent(p, elements)
    return rval

# ---------------------------------------------------------------------------
def find_parent(el, elements):
    for elm in elements:
        if el in elm._children:
            return elm

# ---------------------------------------------------------------------------
toolframe.tf_launch("xml")
