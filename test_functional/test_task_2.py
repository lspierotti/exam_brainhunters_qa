import pytest
from data import *
from services.requests import *
from Logger import logger as log

# ####################################################################################################
# Test the functionality of the endpoint "/user" whe is logged-in
# ####################################################################################################


@pytest.fixture(scope='module')
def request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth(generate_token):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = get_profile_info_of_a_logged_in_user(path, headers)
    log.info("Response: %s"%response.json())
    return response

def test_http_status_code_when_retrive_an_existing_username_with_auth(request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth):
    assert request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth.status_code == USERNAME_HTTP_STATUS_CODE_OK, \
    log.info("The http status code was not as expected: %s"%request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth.text)

def test_logged_user_profile_fields(request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth):
    response_json = request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth.json()
    expected_fields = [
        'login', 'id', 'node_id', 'avatar_url', 'html_url', 
        'followers_url', 'following_url', 'gists_url', 
        'subscriptions_url', 'organizations_url', 'repos_url', 
        'events_url', 'received_events_url', 'type', 
        'user_view_type', 'site_admin', 'name', 
        'company', 'blog', 'location', 'email', 
        'hireable', 'bio', 'twitter_username', 
        'public_repos', 'public_gists', 'followers', 
        'following', 'created_at', 'updated_at', 
        'private_gists', 'total_private_repos', 
        'owned_private_repos', 'disk_usage', 
        'collaborators', 'two_factor_authentication', 
        'plan'
    ]

    # Verifica que todos los campos esperados estén presentes
    for field in expected_fields:
        assert field in response_json, log.info ("The field: %s is not present"%field)

def test_logged_user_profile_private_details(request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth):
    response_json = request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth.json()
    
    # Verifica campos adicionales específicos que pueden ser nulos o privados
    assert 'hireable' in response_json
    assert isinstance(response_json['hireable'], (bool, type(None)))

    assert 'bio' in response_json
    assert isinstance(response_json['bio'], (str, type(None)))

    assert 'twitter_username' in response_json
    assert isinstance(response_json['twitter_username'], (str, type(None)))

    # Verifica que el plan esté presente y tenga los campos correctos
    assert 'plan' in response_json
    assert isinstance(response_json['plan'], dict)

    assert 'name' in response_json['plan']
    assert isinstance(response_json['plan']['name'], str)

    assert 'space' in response_json['plan']
    assert isinstance(response_json['plan']['space'], int)

    assert 'collaborators' in response_json['plan']
    assert isinstance(response_json['plan']['collaborators'], int)

    assert 'private_repos' in response_json['plan']
    assert isinstance(response_json['plan']['private_repos'], int)

def test_logged_user_profile_boolean_fields(request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth):
    response_json = request_to_retrieve_the_profile_info_of_an_loggedin_usere_with_auth.json()

    # Verifica los campos booleanos
    assert 'site_admin' in response_json
    assert isinstance(response_json['site_admin'], bool)

    assert 'two_factor_authentication' in response_json
    assert isinstance(response_json['two_factor_authentication'], bool)

