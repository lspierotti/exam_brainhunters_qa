import pytest
from data import *
from services.requests import *
from Logger import logger as log

# ####################################################################################################
# Test the functionality of the endpoint "users/{username}"
# ####################################################################################################


@pytest.fixture(scope='module')
def request_to_retrieve_the_profile_info_of_an_existing_username_without_auth(generate_token):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    username = EXISTING_USERNAME
    response = get_public_profile_of_a_specific_user_without_auth(path, headers, username)
    log.info("Response: %s"%response.json())
    return response

def test_http_status_code_when_retrive_an_existing_username_without_auth(request_to_retrieve_the_profile_info_of_an_existing_username_without_auth):
    assert request_to_retrieve_the_profile_info_of_an_existing_username_without_auth.status_code == USERNAME_HTTP_STATUS_CODE_OK, \
    log.info("The http status code was not as expected: %s"%request_to_retrieve_the_profile_info_of_an_existing_username_without_auth.text)
    
def test_the_expected_key_fields(request_to_retrieve_the_profile_info_of_an_existing_username_without_auth):
    response_json = request_to_retrieve_the_profile_info_of_an_existing_username_without_auth.json()
    log.info("Verify these fields: %s should be at the response"%EXPECTED_KEY_FIELDS_IN_PROFILE)
    #verify the key values in the response
    for field in EXPECTED_KEY_FIELDS_IN_PROFILE:
        assert field in response_json, log.info("The user: %s is missing field: %s"%(EXISTING_USERNAME, field))

@pytest.mark.parametrize("username, http_status_code", zip(LIST_INVALID_USERNAMES, LIST_USERNAMES_HTTP_STATUS_CODE_NOT_FOUND))
def test_to_retrieve_the_profile_info_of_an_invalid_username_without_auth(generate_token, username, http_status_code):
    path = generate_token[1]
    headers = {
        'Accept': "application/json"
    }
    username = username
    response = get_public_profile_of_a_specific_user_without_auth(path, headers, username)
    log.info("Response: %s"%response.json())
    assert response.status_code == http_status_code, log.info("The http status code was not as expected: %s"%response.text)
    response_json = response.json()

    log.info("Verify the message: %s when the user does not exist"%USER_NOT_FOUND_MESSAGE)
    #verify the message when user does not exist
    assert response_json["message"] == USER_NOT_FOUND_MESSAGE
    