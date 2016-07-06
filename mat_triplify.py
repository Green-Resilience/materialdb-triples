#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dfs

Usage:
  dfs  FILE
  dfs -h | --help
  dfs --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from __future__ import unicode_literals, print_function
from docopt import docopt
import csv
import rdflib
from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import uuid

__version__ = "0.1.0"
__author__ = "Charles Vardeman"
__license__ = "MIT"






def main():
    """Main entry point for the dfs CLI."""
    args = docopt(__doc__, version=__version__)
    csvfile = args["FILE"]

    PROV = Namespace("http://www.w3.org/ns/prov#")
    QUDT = Namespace("http://qudt.org/schema/qudt#")
    COMPONENT = Namespace("http://crc.nd.edu/schema/component#")


    ds = rdflib.Dataset(default_union=True)
    ds.bind("prov", PROV)
    ds.bind("qudt", QUDT)
    ds.bind("component", COMPONENT)


    with open(csvfile, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
          # generate new uuid for component
            componentid = 'urn:green-matdb:' + str(uuid.uuid4())
            ds.add((URIRef(componentid), RDF.type, COMPONENT.Component))
            ds.add((URIRef(componentid), COMPONENT.gbxmlname, Literal(row[1])))
            ds.add((URIRef(componentid), COMPONENT.archname, Literal(row[2])))
            if (row[3] == '1'):
                ds.add((URIRef(componentid), RDF.type, COMPONENT.Window))
    print(ds.serialize(format="turtle"))


if __name__ == '__main__':
    main()
