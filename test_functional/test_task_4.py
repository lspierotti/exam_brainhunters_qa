import pytest
from data import *
from services.requests import *
from Logger import logger as log

# ####################################################################################################
# Test the functionality of the endpoint "/user/repos" when is logged-in
# ####################################################################################################

@pytest.fixture(scope='module')
def request_to_retrieve_all_repos_for_an_loggedin_user_with_auth(generate_token):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = get_all_repos_for_a_logged_in_user(path, headers)
    # log.info("Response: %s"%response.json()) Too large
    return response

def test_http_status_code_when_retrive_all_repos(request_to_retrieve_all_repos_for_an_loggedin_user_with_auth):
    assert request_to_retrieve_all_repos_for_an_loggedin_user_with_auth.status_code == USERNAME_HTTP_STATUS_CODE_OK, \
    log.info("The http status code was not as expected: %s"%request_to_retrieve_all_repos_for_an_loggedin_user_with_auth.text)

def test_verify_the_field_private_and_visibility(request_to_retrieve_all_repos_for_an_loggedin_user_with_auth):
    response_json = request_to_retrieve_all_repos_for_an_loggedin_user_with_auth.json()
    touple_repository = [(repository["private"], repository["visibility"], repository["name"]) for repository in response_json]

    for private, visibility, name_repository in touple_repository:
        log.info("Private repository: %s - Visibility repository: %s, Name repository: %s"%(private, visibility, name_repository))
        if private == False:
            assert visibility == "public", log.info("Repo name: %s when private is False, expected 'public' visibility but got %s visibility"%(name_repository, visibility))
        else:
            assert visibility == "private", log.info("Repo name: %s when private is True, expected 'private' but got %s visibility"%(name_repository, visibility))

