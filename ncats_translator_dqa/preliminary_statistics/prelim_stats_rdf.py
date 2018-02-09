import sys
import os
from rdflib import Graph, Literal, URIRef, Namespace, RDF
from rdflib.namespace import DCTERMS, XSD
from ncats_translator_dqa import config


class PrelimStatsRDF:
    def __init__(self, dataset_id, fps=None, down_url='', byte_size=-1):
        """Write out dataset data quality metrics in RDF using W3C data vocabulary.

            :param dataset_id: ID to be used in URI for this data set (String)
            :param fps: FAIRsharing preliminary stats (FAIRPrelimStats) [optional]
            :param down_url: Download URL of dataset (String) [optional]
            :param byte_size: Size of dataset in bytes [optional]
            :return: None
            """
        # Output message
        if config.verbose:
            print('Converting preliminary statistics to W3C DQV')

        self.dataset_id = dataset_id

        # Define namespaces
        self.__ns_local = Namespace("http://ncats.nih.gov/")
        self.__ns_dcat = Namespace("http://www.w3.org/ns/dcat#")
        self.__ns_dqv = Namespace("http://www.w3.org/ns/dqv#")

        # Create a new graph
        self.g = Graph()

        # Read in the pre-defined turtle file from resources
        file_predefined = os.path.join(config.resource_path, "dqv_definitions.ttl")
        self.g.parse(file_predefined, format="ttl")

        # Create new resources for the data set and distribution
        self.__dataset = self.__ns_local[self.dataset_id]
        self.__distribution = self.__ns_local[self.dataset_id + 'Distribution']

        # Add information about the data set
        self.g.add((self.__dataset, RDF.type, self.__ns_dcat.Dataset))
        self.g.add((self.__dataset, self.__ns_dcat.distribution, self.__distribution))

        # Add information about the distribution
        self.g.add((self.__distribution, RDF.type, self.__ns_dcat.Distribution))
        self.g.add((self.__distribution, self.__ns_dcat.mediaType, Literal("application/rdf")))

        # Set the download URL
        self.add_download_url(down_url)

        # Set the byte size
        self.add_byte_size(byte_size)

        # Measurement count
        self.__n_measurements = 0

        # Add licensing information
        if fps is not None:
            self.add_fair_prelim_stats(fps)

    def add_title(self, title):
        """Adds dcterms:title to dataset and distribution nodes

        :param title: Title (String)
        """
        self.g.add((self.__dataset, DCTERMS.title, Literal(title, lang="en")))
        self.g.add((self.__distribution, DCTERMS.title, Literal(title)))

    def add_download_url(self, url):
        """Adds dcat:downloadURL to distribution

        :param url: URL to the data set download (String)
        """
        if len(url) > 0:
            self.g.add((self.__distribution, self.__ns_dcat.downloadURL, URIRef(url)))

    def add_byte_size(self, byte_size):
        """Adds dcat:byteSize to distribution

        :param byte_size: Size of the data set in bytes (Float)
        """
        if byte_size >= 0:
            self.g.add((self.__distribution, self.__ns_dcat.byteSize, Literal(str(byte_size), datatype=XSD.decimal)))

    def __add_measurement(self, measurement_label=''):
        """Creates and adds a new measurement to the graph

        :param measurement_label: A unique label for the measurement. Leave empty for auto naming.
        :return: The new measurement node
        """
        if len(measurement_label) == 0:
            # Create a new measurement label
            self.__n_measurements += 1
            measurement_label = 'measurement' + '%04d' % self.__n_measurements

        # Create a new measurement node and add it to the graph
        measurement = self.__ns_local[measurement_label]
        self.g.add((measurement, RDF.type, self.__ns_dqv.QualityMeasurement))
        self.g.add((measurement, self.__ns_dqv.computedOn, self.__distribution))
        self.g.add((self.__distribution, self.__ns_dqv.hasQualityMeasurement, measurement))

        return measurement

    def add_licensing_metric(self, license_string):
        """Adds a licensingMetric measurement

        :param license_string: String representing the license
        """
        if len(license_string) > 0:
            measurement = self.__add_measurement()
            self.g.add((measurement, self.__ns_dqv.isMeasurementOf, self.__ns_local.licensingMetric))
            self.g.add((measurement, self.__ns_dqv.value, Literal(license_string, datatype=XSD.string)))

    def add_scopes_and_data_types(self, sads):
        """Adds a list of scopes and data types to the graph as scopeAndDatatypesMetric

        :param sads: List of strings representing the scopes and data types
        """
        if sads is None:
            return

        for sad in sads:
            measurement = self.__add_measurement()
            self.g.add((measurement, self.__ns_dqv.isMeasurementOf, self.__ns_local.scopeAndDatatypesMetric))
            self.g.add((measurement, self.__ns_dqv.value, Literal(sad, datatype=XSD.string)))

    def add_terminology_artifacts(self, tas):
        """Adds a list of terminology artifacts to the graph as terminologyArtifactsMetric

        :param tas: List of strings representing the terminology artifacts
        :return:
        """
        if tas is None:
            return

        for ta in tas:
            measurement = self.__add_measurement()
            self.g.add((measurement, self.__ns_dqv.isMeasurementOf, self.__ns_local.terminologyArtifactsMetric))
            self.g.add((measurement, self.__ns_dqv.value, Literal(ta, datatype=XSD.string)))

    def add_fair_prelim_stats(self, fps):
        """Adds preliminary statistics scraped from FAIRsharing.org to the graph

        :param fps: FAIRPrelimStats object
        :return:
        """
        if fps is None:
            return

        # Add title
        if len(fps.title) > 0:
            self.add_title(fps.title)

        # Add license
        if len(fps.license) > 0:
            # Convert the license data structure into a string
            lic_string = fps.get_license_string()
            self.add_licensing_metric(lic_string)

        # Add information on scopes and data types
        self.add_scopes_and_data_types(fps.scope_and_data_types)

        # Add information on terminology artifacts
        self.add_terminology_artifacts(fps.terminology_artifacts)

    def serialize(self, file, format='ttl'):
        """Writes the RDF graph to file in the specified format

        :param file: Path to the file to write to (String)
        :param format: RDF format (default: 'ttl')
        :return:
        """
        try:
            # Write out turtle file
            self.g.serialize(destination=file, format=format)

            # Output message
            if config.verbose:
                print('Preliminary statistics in W3C DQV written to: ' + file)
        except IOError:
            sys.stderr.write('Error while trying to serialize preliminary stats RDF graph to file: ' + file + '\n')

