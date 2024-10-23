import pytest
from data import *
from services.requests import *
from Logger import logger as log

def assert_response_status(response, expected_status, message):
    assert response.status_code == expected_status, message

def assert_metadata_value(response_json, expected_value):
    log.info("Response before update metadata: %s"%response_json)
    assert response_json["bio"] == expected_value, log.info("The bio should be: %s but found %s"%(expected_value, response_json["bio"]))

def test_update_bio(generate_token):
    token, path = generate_token
    
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    # Step 1: Get user profile info and validate 
    response_get_user = get_profile_info_of_a_logged_in_user(path, headers)
    response_get_user_json = response_get_user.json()
    assert_response_status(response_get_user, 200, log.info("The bio is: %s"%(response_get_user_json["bio"])))
    assert_metadata_value(response_get_user_json, "Software Engineer")

    # Step 2: Update metadata
    body = {"bio": None}
    response_patch = patch_metadata_for_logged_user(path, headers, body)
    response_patch_json = response_patch.json()
    assert_response_status(response_patch, 200, log.info("We update the bio: %s"%body))
    assert_metadata_value(response_patch_json, None)

    # # Step 3: Update the metadata to reset the values to their original state"
    # body = {metadata_to_change: original_value}
    # response_patch = patch_metadata_for_logged_user(path, headers, body)
    # response_patch_json = response_patch.json()
    # assert_response_status(response_patch, 200, log.info("We update the %s: %s"%(metadata_to_change, body)))
    # assert_metadata_value(response_patch_json, metadata_to_change, original_value)
