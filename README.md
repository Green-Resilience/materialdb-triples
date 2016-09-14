# material-triples
Python Script to generate RDF Triples for Construction component and Material Database

This python script converts the materials.csv sqlite3 database to triples to publish as linked data. Also included is the set of triples to define the metadata for a linked data platform container.

## Docker instructions
A Marmotta image exits in the docker hub repository. To retrieve the docker image.
```bash
docker pull apache/marmotta
```

To start the Marmotta image:
```bash
docker run -p 8080:8080 apache/marmotta
```

##Linked Data Platform
A tutorial on using Marmotta Linked Data Platform functionality can be found is in a [github](https://github.com/wikier/apache-marmotta-tutorial-iswc2014/tree/master/ldp) repository. Relevant parts cribbed from that repositories README.md.


*NOTE*: The abrevitions used here are defined in the [LDP 1.0 Specification](http://www.w3.org/TR/ldp/) 
which is currently a working draft. Let's revisit the most important briefly:

* **LDPR**: Linked Data Platform Resource
* **LDP-RS**: Linked Data Platform RDF Source <br>
    An LDPR whose state is fully represented in RDF, corresponding to an RDF graph.
* **LDP-NR**: Linked Data Platform Non-RDF Source <br>
    For example, these can be binary or text documents that do not have useful RDF representations.
* **LDPC**: Linked Data Platform Container
* **LDP-BC**: Linked Data Platform Basic Container <br>
    An LDPC that defines a simple link to its contained documents using the `ldp:contains` property.

The prefix `ldp` for RDF is resolved to `http://www.w3.org/ns/ldp#`.

```bash
  curl -iX POST -H "Content-Type: text/turtle" \
        -H "Slug: Apache Marmotta" \
        --data @data/blog.ttl \
        http://localhost:8080/ldp
```
Using [httpie](https://github.com/jkbrzt/httpie) [cheatsheet](http://ricostacruz.com/cheatsheets/httpie.html)
```bash
   http POST http://localhost:8080/marmotta/ldp \ 
   "Content-Type:text/turtle" \
   "Slug:Materials"
```

Attach the data set to the ldp container.
```bash
   curl -iX POST -H "Content-Type: text/turtle" \
        -H "Slug: ISWC2014 Tutorial" \
        --data @data/post.ttl \
        http://localhost:8080/ldp/Apache-Marmotta
```

Using httpie
```bash
    http POST http://localhost:8080/marmotta/ldp/Materials \
    "Content-Type:text/turtle" \
    "Slug:GreenscaleDB" \
    < building_components.ttl
```

Validate the data is correct:
```bash
    curl -i -H "Accept: text/turtle" \
        http://localhost:8080/ldp/Apache-Marmotta

    curl -i -H "Accept: text/turtle" \
        http://localhost:8080/ldp/Apache-Marmotta/ISWC2014-Tutorial
```


