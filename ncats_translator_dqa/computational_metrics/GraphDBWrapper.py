"""Wrapper for interacting with GraphDB REST API
"""
import requests
import json


class GraphDBWrapper:
    """Wrapper for interacting with GraphDB REST API
    """
    __api_delete_repo = 'rest/repositories/'
    __api_create_repo = 'rest/repositories/'
    __api_upload_url = 'rest/data/import/url/'

    def __init__(self, url_graphdb="http://localhost:7200", verbose=False):
        """Constructor

        :param url_graphdb: URL to GraphDB
        :param verbose: True if you want to print status messages
        """
        # Make sure the url to graphdb ends with a '/'
        if url_graphdb[-1] != '/':
            url_graphdb += '/'
        self.url_graphdb = url_graphdb
        self.verbose = verbose

    def delete_repo(self, repo_id):
        """Deletes the repository with the given ID.

        This will be successful even if the repository doesn't exist.

        :param repo_id: repository ID to delete
        :return: requests.response
        """
        if self.verbose:
            print('GraphDB: deleting repository ' + repo_id)

        headers = {'Accept': '*/*'}
        url_delete = self.url_graphdb + GraphDBWrapper.__api_delete_repo + repo_id
        response = requests.delete(url_delete, headers=headers)
        response.raise_for_status()

        if self.verbose:
            if response.status_code == requests.codes.ok:
                print('GraphDB: delete successful')
            else:
                GraphDBWrapper.print_response(response)

        return response

    def create_repo(self, repo_id, title):
        """Creates a repository with the given ID.

        This will fail if the repository already exists.

        :param repo_id: A new repository ID
        :param title: Title for the new repository
        :return: requests.response
        """
        if self.verbose:
            print('GraphDB: creating repository ' + repo_id)

        # Make sure the repo ID is safe
        repo_id = GraphDBWrapper.sanitize_repo_id(repo_id)

        # Repository configuration
        repo_config = {
            'id': repo_id,
            'params': {},
            'title': title,
            'type': 'free'
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }

        url_create = self.url_graphdb + GraphDBWrapper.__api_create_repo
        response = requests.put(url_create, headers=headers, data=json.dumps(repo_config))
        response.raise_for_status()

        if self.verbose:
            if response.status_code == requests.codes.created:
                print('GraphDB: ' + repo_id + ' created successfully')
            else:
                GraphDBWrapper.print_response(response)

        return response

    def upload_data_url(self, repo_id, url_data):
        """Initiates a data URL upload to the specified repository

        This method initiates an upload. It does not wait for the upload to complete.

        :param repo_id: Repository to upload to
        :param url_data: URL of data to upload
        :return: requests.response
        """
        if self.verbose:
            print('GraphDB: importing into ' + repo_id + ': ' + url_data)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        url_import = self.url_graphdb + GraphDBWrapper.__api_upload_url + repo_id + '?url=' + url_data
        response = requests.post(url_import, headers=headers)
        response.raise_for_status()

        if self.verbose:
            if response.status_code == requests.codes.accepted:
                print('GraphDB: data import successfully started')
            else:
                GraphDBWrapper.print_response(response)

        return response

    @staticmethod
    def print_response(response):
        """Prints basic information from a requests.response object

        :param response: A requests.response object
        :return: None
        """
        print('GraphDB response status ' + response.status_code + ': ' + response.content.decode())

    @staticmethod
    def sanitize_repo_id(suggested_id):
        """Sanitizes the suggested repository name so that it meets the requirements for a GraphDB repository name

        :param suggested_name: The suggested name (String)
        :return: The sanitized name (String)
        """
        return ''.join([c if c.isalnum() else '_' for c in suggested_id])