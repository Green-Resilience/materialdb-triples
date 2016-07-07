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
        # id[0],namegbxml[1],namearch[2],iswindow[3],
        # thickness[4],embodiedenergy[5],eeunit_id[6],
        # matdensityarch[7],matdensitygbxml[8],densityunit_id[9],
        # unitcostmat[10],unitcostmle[11],unitcostttl[12],
        # financialunit_id[13],lifeexpectancy[14],maintenancefactor[15],
        # infosource[16],confidence[17]
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
            materialdensityArch = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasMaterialDensity, materialdensityArch))
            ds.add((materialdensityArch, COMPONENT.hasSource, COMPONENT.Archsource))
            ds.add((materialdensityArch, RDF.type, QUDT.QuantityValue))
            ds.add((materialdensityArch, QUDT.numericValue, Literal(row[7],datatype=XSD.float)))
            if (row[9] == '1'):
                ds.add((materialdensityArch, QUDT.unit, UNIT.KilogramPerCubicMeter))
            elif (row[9] == '2'):
                ds.add((materialdensityArch, QUDT.unit, UNIT.PoundPerCubicFoot))
            materialdensitygbxml = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasMaterialDensity, materialdensitygbxml))
            ds.add((materialdensityArch, COMPONENT.hasSource, COMPONENT.gbxmlsource))
            ds.add((materialdensitygbxml, RDF.type, QUDT.QuantityValue))
            ds.add((materialdensitygbxml, QUDT.numericValue, Literal(row[8],datatype=XSD.float)))
            if (row[9] == '1'):
                ds.add((materialdensitygbxml, QUDT.unit, UNIT.KilogramPerCubicMeter))
            elif (row[9] == '2'):
                ds.add((materialdensitygbxml, QUDT.unit, UNIT.PoundPerCubicFoot))
            unitcostmat = BNode()
            ds.add((URIRef(componentid), COMPONENT.hasUnitCost, unitcostmat))
            ds.add((unitcostmat, RDF.type, QUDT.QuantityValue))
            ds.add((unitcostmat, QUDT.numericValue, Literal(row[10],datatype=XSD.float)))

    print(ds.serialize(format="turtle"))


if __name__ == '__main__':
    main()
