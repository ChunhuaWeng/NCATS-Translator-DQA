"""Computes computational metrics for linked open datasets.
"""

import os
from ncats_translator_dqa import config
from ncats_translator_dqa.computational_metrics.GraphDBWrapper import GraphDBWrapper
from ncats_translator_dqa.computational_metrics.RDFUnitWrapper import RDFUnitWrapper


def computational_metrics(dataset_uri, sparql_endpoint=None, sparql_graph=None, schema=''):
    """Computes computational metrics for linked open datasets.

    Runs RDFUnit on datasets and generates reports in W3C Data Quality Vocabulary (DQV). Creates a new GraphDB
    repository and imports results for visualization.

    Please update config.py prior to using this function.

    Note: the function starts the data import on GraphDB, but does not wait for the import to finish. GraphDB may take some
    time to finish importing and generating diagrams depending on the size of the data.

    :param dataset_uri: Absolute path to dataset
    :param schema: URI to schema to perform validation against or defined schema prefix. Leave empty for automatic
     detection of ontologies by rdfunit (String) [optional]
    :return: None
    """
    # RDFUnitWrapper object for running rdfunit and dqv-report
    rdfunit = RDFUnitWrapper()

    # Run rdfunit on data
    file_rdfunit_output = rdfunit.rdfunit(dataset_uri, sparql_endpoint, sparql_graph, schema)

    # GraphDB object for interacting with GraphDB REST API
    graphdb = GraphDBWrapper(config.url_graphdb, config.verbose)

    # Use the dataset name as the GraphDB repository ID
    filename_dataset = os.path.split(dataset_uri)[1]
    repo_id = GraphDBWrapper.sanitize_repo_id(filename_dataset)

    # Delete any existing repository with the same repository ID
    graphdb.delete_repo(repo_id)

    # Create a new repository
    repo_title = filename_dataset + ' - Data Quality Computational Metrics'
    graphdb.create_repo(repo_id, repo_title)

    # Upload results to repository
    url_output = 'file://' + file_rdfunit_output
    graphdb.upload_data_url(repo_id, url_output)
