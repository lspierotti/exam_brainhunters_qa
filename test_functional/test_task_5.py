import pytest
from data import *
from services.requests import *
from Logger import logger as log

# ####################################################################################################
# Test the functionality of the endpoint "repos/{owner}/{repos}/commits"
# ####################################################################################################

#happy path
@pytest.fixture(scope='module')
def request_to_get_the_list_of_commits_of_public_repo(generate_token):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    owner = EXISTING_USERNAME
    public_repo = PUBLIC_REPO

    response = get_all_commits_for_a_public_repo(path, headers, owner, public_repo)
    # log.info("Response: %s"%response.json())  #A lot of content and -------
    return response

def test_http_status_code_when_retrive_commits_for_a_repo(request_to_get_the_list_of_commits_of_public_repo):
    assert request_to_get_the_list_of_commits_of_public_repo.status_code == USERNAME_HTTP_STATUS_CODE_OK, \
    log.info("The http status code was not as expected: %s"%request_to_get_the_list_of_commits_of_public_repo.text)

def test_each_commit_has_a_different_hash(request_to_get_the_list_of_commits_of_public_repo):
    commits_json = request_to_get_the_list_of_commits_of_public_repo.json()
    list_sha = [commit["sha"] for commit in commits_json]
    assert len(list_sha) == len(set(list_sha)), log.info("There are commits with the same sha")

def test_commit_fields(request_to_get_the_list_of_commits_of_public_repo):
    commits_json = request_to_get_the_list_of_commits_of_public_repo.json()
    for commit in commits_json:
        # Cada commit debe tener su 'sha', 'author', 'message' y 'date'
        assert 'sha' in commit, log.info("Missing 'sha' field")
        assert 'commit' in commit, log.info("Missing 'commit' object")
        assert 'author' in commit['commit'], log.info("Missing 'author' field")
        assert 'message' in commit['commit'], log.info("Missing 'message' field")
        assert 'date' in commit['commit']['author'], log.info("Missing 'date' field")

        # Valido que cada campo tenga el tipo esperado
        assert isinstance(commit['sha'], str), log.info("'sha' should be a string")
        assert isinstance(commit['commit']['author']['name'], str), log.info("'author' name should be a string")
        assert isinstance(commit['commit']['message'], str), log.info("'message' should be a string")
        assert isinstance(commit['commit']['author']['date'], str), log.info("'date' should be a string")

#repos inexitentes para un usuario valido
@pytest.mark.parametrize("repo, http_status_code", zip(LIST_INVALID_REPO, LIST_REPOS_HTTP_STATUS_CODE_NOT_FOUND))
def test_http_status_code_when_retrieve_commits_for_an_inexistent_repo(generate_token, repo, http_status_code):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    owner = EXISTING_USERNAME
    public_repo = repo

    response = get_all_commits_for_a_public_repo(path, headers, owner, public_repo)
    # log.info("Response: %s"%response.json())  #A lot of content and -------
    
    assert response.status_code == http_status_code, log.info("The http status code was not as expected: %s"%response.text)
    response_json = response.json()

    log.info("Verify the message: %s when the repo does not exist"%USER_NOT_FOUND_MESSAGE)
    #verify the message when user does not exist
    assert response_json["message"] == USER_NOT_FOUND_MESSAGE
       