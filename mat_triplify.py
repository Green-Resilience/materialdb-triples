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


# QUDT usage
# :myQuantityValue        rdf:type                qudt:QuantityValue.
# :myQuantityValue        qudt:numericValue       "1.057"^^xsd:double.
# :myQuantityValue        qudt:unit               unit:ElectronVolt.



def main():
    """Main entry point for the dfs CLI."""
    args = docopt(__doc__, version=__version__)
    csvfile = args["FILE"]

    PROV = Namespace("http://www.w3.org/ns/prov#")
    QUDT = Namespace("http://qudt.org/schema/qudt#")
    UNIT = Namespace("http://qudt.org/1.1/vocab/unit#")
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
            # Check to see if this guy is a window
            if (row[3] == '1'):
                ds.add((URIRef(componentid), RDF.type, COMPONENT.Window))
            # Check to see if we have a thickness
            # thicknessid = 'urn:green-matdb:' + str(uuid.uuid4())
            thicknessid = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasThickness, thicknessid))
            ds.add((thicknessid, RDF.type, QUDT.QuantityValue))
            ds.add((thicknessid, QUDT.numericValue, Literal(row[4],datatype=XSD.float)))
            ds.add((thicknessid, QUDT.unit, UNIT.Inch))
            embodiedenergy = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasEmbodiedEnergy, embodiedenergy))
            ds.add((embodiedenergy, RDF.type, QUDT.QuantityValue))
            ds.add((embodiedenergy, QUDT.numericValue, Literal(row[5],datatype=XSD.float)))
            if (row[6] == '1'):
                ds.add((embodiedenergy, QUDT.unit, UNIT.BtuPerPound))
            elif (row[6] == '2'):
                # This QUDT unit doesn't exist. Unit is JoulePerKilogram.
                # Need to create new derived unit.
                ds.add((embodiedenergy, QUDT.unit, UNIT.MegaJoulePerKilogram))
            materialdensity = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasMaterialDensity, materialdensity))
            ds.add((materialdensity, RDF.type, QUDT.QuantityValue))
            ds.add((materialdensity, QUDT.numericValue, Literal(row[7],datatype=XSD.float)))
            if (row[8] == '1'):
                ds.add((materialdensity, QUDT.unit, UNIT.KilogramPerCubicMeter))
            elif (row[8] == '2'):
                ds.add((materialdensity, QUDT.unit, UNIT.PoundPerCubicFoot))


    print(ds.serialize(format="turtle"))


if __name__ == '__main__':
    main()
