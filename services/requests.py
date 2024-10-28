
import requests
from Logger import logger as log

def get_names(headers, path, queryparams):
    '''Get names'''
    endpoint = ""
    url = ''.join([path,endpoint])
    response = requests.request("GET", url, headers=headers, params = queryparams)
    return response


def get_public_profile_of_a_specific_user_without_auth(path, headers, username):
    '''Retrieve the public profile info'''
    endpoint = f"users/{username}"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - with username: %s and headers: %s"%(url, username, headers))
    response = requests.request("GET", url, headers=headers)
    return response

def get_profile_info_of_a_logged_in_user(path, headers):
    '''Retrieve the profile info of a logged-in info'''
    endpoint = "user"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - with a logged-in user and headers: %s"%(url, headers))
    response = requests.request("GET", url, headers=headers)
    return response

def get_public_repositories_for_a_user(path, headers, username):
    '''Retrieve the list of public repositories of an user'''
    endpoint = f"users/{username}/repos"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - with username: %s and headers: %s"%(url, username, headers))
    response = requests.request("GET", url, headers=headers)
    return response

def get_all_repos_for_a_logged_in_user(path, headers):
    '''Retrieve all repos (public and privates) for a logged-in info'''
    endpoint = "user/repos"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - with a logged-in user and headers: %s"%(url, headers))
    response = requests.request("GET", url, headers=headers)
    return response

def get_all_commits_for_a_public_repo(path, headers, owner, repo):
    '''Retrieve all commits (public and privates) for a logged-in info'''
    endpoint = f"repos/{owner}/{repo}/commits"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - with owner: %s and repo: %s and headers: %s"%(url, owner, repo, headers))
    response = requests.request("GET", url, headers=headers)
    return response

def patch_metadata_for_logged_user(path, headers, data):
    '''Update the metadata of logged user'''
    endpoint = "user"
    url = ''.join([path, endpoint])
    log.info("Testing endpoint: %s - for a logged-in user with: %s and headers: %s"%(url, data, headers))
    response = requests.request("PATCH", url, headers=headers, json = data)
    return response

def post_create_gist(path, headers, data):
    '''create a gist'''
    endpoint = 'gists'
    url = ''.join([path, endpoint])
    log.info("create a gist")
    response = requests.request("POST", url, headers = headers, json = data)
    return response


def get_gist_created(path, headers):
    '''get a gist'''
    endpoint = 'gists'
    url = ''.join([path, endpoint])
    log.info("create a gist")
    response = requests.request("POST", url, headers = headers, json = data)
    return response