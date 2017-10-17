import sys
import os
from rdflib import Graph, Literal, URIRef, Namespace, RDF
from rdflib.namespace import DC, DCTERMS, XSD
from fair_scraper import FAIRPrelimStats

def data_quality_rdf(file, fps=FAIRPrelimStats(), downURL='', byteSize=-1):
    """Write out dataset data quality metrics in RDF using W3C data vocabulary.

    :param file: Output file location (String)
    :param fps: FAIRsharing preliminary stats (FAIRPrelimStats)
    :param downURL: Download URL of dataset (String) [optional]
    :param byteSize: Size of dataset in bytes [optional]
    :return: None
    """

    # Define namespaces
    ns_local = Namespace("http://ncats.nih.gov/")
    ns_dcat = Namespace("http://www.w3.org/ns/dcat#")
    ns_dqv = Namespace("http://www.w3.org/ns/dqv#")

    # Create a new graph
    g = Graph()

    # Read in the pre-defined turtle file from the directory where the code resides
    dir_code = sys.path[0]
    file_predefined = os.path.join(dir_code, "dqv_definitions.ttl")
    g.parse(file_predefined, format="ttl")

    # Use the dataset title as the local identifier
    if len(fps.url) > 0:
        # Get rid of any non alphanumeric characters
        datasetID = "".join([c for c in fps.title if c.isalnum()]) + 'Dataset'
    else:
        # Use a generic name
        datasetID = 'myDataset'

    # Create new resources for the dataset and distribution
    dataset = ns_local[datasetID]
    distribution = ns_local[datasetID + 'Distribution']

    # Add information about the dataset
    g.add((dataset, RDF.type, ns_dcat.Dataset))
    g.add((dataset, DCTERMS.title, Literal(fps.title, lang="en")))
    g.add((dataset, ns_dcat.distribution, distribution))

    # Add information about the distribution
    g.add((distribution, RDF.type, ns_dcat.Distribution))
    g.add((distribution, DCTERMS.title, Literal(fps.title)))
    g.add((distribution, ns_dcat.mediaType, Literal("application/rdf")))
    if len(downURL) > 0:
        g.add((distribution, ns_dcat.downloadURL, URIRef(downURL)))
    if byteSize >= 0:
        g.add((distribution, ns_dcat.byteSize, Literal(str(byteSize), datatype=XSD.decimal)))

    # Measurement count
    n_measurements = 0

    # Add licensing information
    if len(fps.license) > 0:
        n_measurements += 1
        measurement_label = 'measurement' + '%04d' % n_measurements
        measurement = ns_local[measurement_label]
        g.add((measurement, RDF.type, ns_dqv.QualityMeasurement))
        g.add((measurement, ns_dqv.computedOn, distribution))
        g.add((measurement, ns_dqv.isMeasurementOf, ns_local.licensingMetric))
        g.add((distribution, ns_dqv.hasQualityMeasurement, measurement))

        # Generate the license string
        lic_strings = []
        sep = '; '
        for lic in fps.license:
            lic_strings.append(lic[0] + " = {" + sep.join(lic[1]) + "}")
        lic_string = sep.join(lic_strings)
        g.add((ns_local[measurement_label], ns_dqv.value, Literal(lic_string, datatype=XSD.string)))

    # Add information on scopes and data types
    for sad in fps.scope_and_data_types:
        n_measurements += 1
        measurement_label = 'measurement' + '%04d' % n_measurements
        measurement = ns_local[measurement_label]
        g.add((measurement, RDF.type, ns_dqv.QualityMeasurement))
        g.add((measurement, ns_dqv.computedOn, distribution))
        g.add((measurement, ns_dqv.isMeasurementOf, ns_local.scopeAndDatatypesMetric))
        g.add((measurement, ns_dqv.value, Literal(sad, datatype=XSD.string)))
        g.add((distribution, ns_dqv.hasQualityMeasurement, measurement))

    # Add information on terminology artifacts
    for ta in fps.terminology_artifacts:
        n_measurements += 1
        measurement_label = 'measurement' + '%04d' % n_measurements
        measurement = ns_local[measurement_label]
        g.add((measurement, RDF.type, ns_dqv.QualityMeasurement))
        g.add((measurement, ns_dqv.computedOn, distribution))
        g.add((measurement, ns_dqv.isMeasurementOf, ns_local.terminologyArtifactsMetric))
        g.add((measurement, ns_dqv.value, Literal(ta, datatype=XSD.string)))
        g.add((distribution, ns_dqv.hasQualityMeasurement, measurement))

    # Write out turtle file
    g.serialize(destination=file, format="ttl")

