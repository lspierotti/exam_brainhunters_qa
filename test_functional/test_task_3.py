import pytest
from data import *
from services.requests import *
from Logger import logger as log

# ####################################################################################################
# Test the functionality of the endpoint "users/{username}/repos"
# ####################################################################################################


@pytest.fixture(scope='module')
def request_to_retrieve_the_public_repositories_of_an_user(generate_token):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    username = EXISTING_USERNAME
    response = get_public_repositories_for_a_user(path, headers, username)
    log.info("Response: %s"%response.json())  #A lot of content and -------
    return response

def test_http_status_code_when_retrive_a_public_repositorie(request_to_retrieve_the_public_repositories_of_an_user):
    assert request_to_retrieve_the_public_repositories_of_an_user.status_code == USERNAME_HTTP_STATUS_CODE_OK, \
    log.info("The http status code was not as expected: %s"%request_to_retrieve_the_public_repositories_of_an_user.text)
    
def test_list_of_repositories_should_not_be_zero(request_to_retrieve_the_public_repositories_of_an_user):
    response_json = request_to_retrieve_the_public_repositories_of_an_user.json()
    assert len(response_json) != 0, log.info("The quantity of repositories should not be zero")

def test_each_repositorie_has_a_different_name(request_to_retrieve_the_public_repositories_of_an_user):
    response_json = request_to_retrieve_the_public_repositories_of_an_user.json()
    list_names_repositories = [repository["name"] for repository in response_json]
    log.info("List of repositories: %s"%list_names_repositories)

    assert len(list_names_repositories) == len(set(list_names_repositories)), log.info("There are duplicated repositories")


@pytest.mark.parametrize("username, http_status_code", zip(LIST_INVALID_USERNAMES, LIST_USERNAMES_HTTP_STATUS_CODE_NOT_FOUND))
def test_to_retrieve_the_public_repositorie_of_an_invalid_user_without_auth(generate_token, username, http_status_code):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    username = username
    response = get_public_repositories_for_a_user(path, headers, username)
    log.info("Response: %s"%response.json())
    assert response.status_code == http_status_code, log.info("The http status code was not as expected: %s"%response.text)
    response_json = response.json()

    log.info("Verify the message: %s when the user does not exist"%USER_NOT_FOUND_MESSAGE)
    #verify the message when user does not exist
    assert response_json["message"] == USER_NOT_FOUND_MESSAGE
    