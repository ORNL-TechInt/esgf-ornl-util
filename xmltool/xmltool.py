#!/usr/bin/env python
import os
import pdb
import re
import sys
import toolframe
import traceback as tb
import xml.etree.ElementTree as ET

from optparse import *

# ---------------------------------------------------------------------------
def xml_add(argv):
    """add - add information to an xml file

    usage: xmltool add [-d] -f input-info-file <filename> <filename> ...

    -d     run under python debugger
    -f     filename containing info to be added

    Result is written to stdout.
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    p.add_option('-f', '--input-file',
                 action='store', default=None, dest='infile',
                 help='name of file containing info to be added')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()

    add = ET.parse(o.infile)

    for filename in a:
        # X = parse_map1(filename)
        X = ET.parse(filename)
        set_global_namespace(X)
                              
        for el in X.iter():
            if o.attrib in el.attrib.keys():
                # -- do the edit
                ebuf = el.attrib[o.attrib]
                for eval in ehash.keys():
                    ebuf = ebuf.replace(eval, ehash[eval])

                el.attrib[o.attrib] = ebuf

        p = ET.ProcessingInstruction('xml', 'version="1.0" encoding="UTF-8"')
        sys.stdout.write(ET.tostring(p) + "\n")
        X.write(sys.stdout)
        print("")
    
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
        # X = parse_map1(filename)
        X = ET.parse(filename)
        set_global_namespace(X)
                              
        for el in X.iter():
            if o.attrib in el.attrib.keys():
                # -- do the edit
                ebuf = el.attrib[o.attrib]
                for eval in ehash.keys():
                    ebuf = ebuf.replace(eval, ehash[eval])

                el.attrib[o.attrib] = ebuf

        p = ET.ProcessingInstruction('xml', 'version="1.0" encoding="UTF-8"')
        sys.stdout.write(ET.tostring(p) + "\n")
        X.write(sys.stdout)
        print("")
    
# ---------------------------------------------------------------------------
def xml_attrlist(argv):
    """attrlist - list the occurences of a specified attribute

    usage: xmltool attrlist [-d] -a attrib <filename> <filename> ...

    -a     which attribute to list
    -d     run under python debugger

    Matching attributes are listed.
    """
    try:
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

            tagl = [e.tag for e in elements]
            pfx = os.path.commonprefix(tagl)
            for el in X.iter():
                if o.attrib in el.attrib.keys():
                    path = geneaology(el, elements, X, pfx)
                    print("%s ( %s: %s )" % (path, o.attrib, el.attrib[o.attrib]))
    except Exception, e:
        tb.print_exc(e)

# ---------------------------------------------------------------------------
def xml_iterate(argv):
    """iterate - iterate an xml file and report what we get

    usage: xmltool iterate [-d] <filename> <filename> ...

    -d     run under python debugger

    This routine is for iterating the contents of an xml file
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()


    for filename in a:
        tree = ET.parse(filename)
        elements = [el for el in tree.iter()]
        pfx = os.path.commonprefix([e.tag for e in tree.iter()])
        for el in tree.iter():
            tagstr = geneaology(el, elements, tree, pfx)
            print tagstr
            for atr in el.attrib.keys():
                print '   %s -> %s' % (atr, el.attrib[atr])
            if el.text != None and el.text.strip() != '':
                print '   TEXT: %s' % (el.text)
            
# ---------------------------------------------------------------------------
def xml_tree(argv):
    """tree - traverse the xml structure as a tree

    usage: xmltool tree [-d] <filename> <filename> ...

    -d     run under python debugger

    This routine is for tree-traversing the contents of an xml file
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()

    for filename in a:
        tree = ET.parse(filename)
        traverse_r(tree._root, "")
            
# ---------------------------------------------------------------------------
def traverse_r(element, indent):
    print("%s%s" % (indent, element.tag))
    for child in element:
        traverse_r(child, indent + ">")

# ---------------------------------------------------------------------------
def xml_tparse(argv):
    """tparse - test parsing

    usage: xmltool tparse [-d] <filename> <filename> ...

    -d     run under python debugger

    This routine is for trying out various parsing strategies.
    """
    p = OptionParser()
    p.add_option('-d', '--debug',
                 action='store_true', default=False, dest='debug',
                 help='run the debugger')
    (o, a) = p.parse_args(argv)

    if o.debug: pdb.set_trace()

    for filename in a:
        tree = parse_map1(filename)
        tree.write(sys.stdout)
        
# ---------------------------------------------------------------------------
def find_parent(el, elements):
    for elm in elements:
        if el in elm._children:
            return elm
    return None

# ---------------------------------------------------------------------------
def geneaology(el, elements, root, pfx):
    rval = el.tag.replace(pfx, '')
    p = find_parent(el, elements)
    while p != None:
        tag = p.tag.replace(pfx, '')
        rval = '%s > ' % (tag) + rval
        p = find_parent(p, elements)
    return rval

# ---------------------------------------------------------------------------
def parse_map1(file):
    events = "start", "start-ns", "end-ns"

    root = None
    ns_map = {}

    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            ns_map[elem[0]] = elem[1]
        elif event == "start":
            if root is None:
                root = elem
    rval = ET.ElementTree(root)
    rval.ns_map = ns_map
            
    return rval

# ---------------------------------------------------------------------------
def parse_map2(file):
    events = "start", "start-ns", "end-ns"

    root = None
    ns_map = []

    for event, elem in ET.iterparse(file, events):
        if event == "start-ns":
            ns_map.append(elem)
        elif event == 'end-ns':
            ns_map.pop()
        elif event == "start":
            if root is None:
                root = elem
            elem.ns_map = dict(ns_map)
            
    rval = ET.ElementTree(root)
    return rval

# ---------------------------------------------------------------------------
def set_global_namespace(tree):
    tagl = [e.tag for e in tree.iter()]
    pfx = os.path.commonprefix(tagl)
    ET.register_namespace('', pfx.strip('{}'))
    
# ---------------------------------------------------------------------------
toolframe.tf_launch("xml")
