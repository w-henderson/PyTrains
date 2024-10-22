# Author: Christian Stefanescu (http://0chris.com)
# License: MIT License - http://www.opensource.org/licenses/mit-license.php

# I've modified this to fit the needs of this project, the original can be found at https://github.com/stchris/untangle

import os
import keyword
from xml.sax import make_parser, handler

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    from types import StringTypes

    def is_string(x):
        return isinstance(x, StringTypes)


except ImportError:

    def is_string(x):
        return isinstance(x, str)


__version__ = "1.1.1"


class Element(object):
    """
    Representation of an XML element.
    """

    def __init__(self, name, attributes):
        self._name = name
        self._attributes = attributes
        self.children = []
        self.is_root = False
        self.cdata = ""

    def add_child(self, element):
        """
        Store child elements.
        """
        self.children.append(element)

    def add_cdata(self, cdata):
        """
        Store cdata
        """
        self.cdata = self.cdata + cdata

    def get_attribute(self, key):
        """
        Get attributes by key
        """
        return self._attributes.get(key)

    def get_elements(self, name=None):
        """
        Find a child element by name
        """
        if name:
            return [e for e in self.children if e._name == name]
        else:
            return self.children

    def __getitem__(self, key):
        return self.get_attribute(key)

    def __getattr__(self, key):
        matching_children = [x for x in self.children if x._name == key]
        if matching_children:
            if len(matching_children) == 1:
                self.__dict__[key] = matching_children[0]
                return matching_children[0]
            else:
                self.__dict__[key] = matching_children
                return matching_children
        else:
            raise AttributeError("'%s' has no attribute '%s'" % (self._name, key))

    def __hasattribute__(self, name):
        if name in self.__dict__:
            return True
        return any(x._name == name for x in self.children)

    def __iter__(self):
        yield self

    def __str__(self):
        return "Element <%s> with attributes %s, children %s and cdata %s" % (
            self._name,
            self._attributes,
            self.children,
            self.cdata,
        )

    def __repr__(self):
        return "Element(name = %s, attributes = %s, cdata = %s)" % (
            self._name,
            self._attributes,
            self.cdata,
        )

    def __nonzero__(self):
        return self.is_root or self._name is not None

    def __eq__(self, val):
        return self.cdata == val

    def __dir__(self):
        children_names = [x._name for x in self.children]
        return children_names

    def __len__(self):
        return len(self.children)

    def __contains__(self, key):
        return key in dir(self)


class Handler(handler.ContentHandler):
    """
    SAX handler which creates the Python object structure out of ``Element``s
    """

    def __init__(self):
        self.root = Element(None, None)
        self.root.is_root = True
        self.elements = []

    def startElement(self, name, attributes):
        name = name.replace("-", "_")
        name = name.replace(".", "_")
        name = name.replace(":", "_")

        # adding trailing _ for keywords
        if keyword.iskeyword(name):
            name += "_"

        attrs = dict()
        for k, v in attributes.items():
            attrs[k] = v
        element = Element(name, attrs)
        if len(self.elements) > 0:
            self.elements[-1].add_child(element)
        else:
            self.root.add_child(element)
        self.elements.append(element)

    def endElement(self, name):
        self.elements.pop()

    def characters(self, cdata):
        self.elements[-1].add_cdata(cdata)


def parse(string, **parser_features):
    parser = make_parser()
    for feature, value in parser_features.items():
        parser.setFeature(getattr(handler, feature), value)
    sax_handler = Handler()
    parser.setContentHandler(sax_handler)

    if string[0] != "<": string = string[3:] # Fix weird request bug where 3 invalid chars are sometimes at the start

    parser.parse(StringIO(string))

    return sax_handler.root