import pytest
from data import *
from services.requests import *
from Logger import logger as log

def assert_response_status(response, expected_status, message):
    assert response.status_code == expected_status, message

def assert_metadata_value(response_json, metadata_to_change, expected_value):
    log.info("Response before update metadata: %s"%response_json)
    assert response_json[metadata_to_change] == expected_value, log.info("The %s should be: %s but found %s"%(metadata_to_change, expected_value, response_json[metadata_to_change]))


@pytest.mark.parametrize("metadata_to_change, original_value, value_to_change", zip(LIST_KEYS_METADATA, LIST_ORIGIN_VALUES_METADATA, LIST_VALUES_METADATA))
def test_update_metadata_of_user_auth_ok(generate_token, metadata_to_change, original_value, value_to_change):
    token, path = generate_token
    
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    # Step 1: Get user profile info and validate 
    response_get_user = get_profile_info_of_a_logged_in_user(path, headers)
    response_get_user_json = response_get_user.json()
    assert_response_status(response_get_user, 200, log.info("The %s is: %s"%(metadata_to_change, response_get_user_json[metadata_to_change])))
    assert_metadata_value(response_get_user_json, metadata_to_change, original_value)

    # Step 2: Update metadata
    body = {metadata_to_change: value_to_change}
    response_patch = patch_metadata_for_logged_user(path, headers, body)
    response_patch_json = response_patch.json()
    assert_response_status(response_patch, 200, log.info("We update the %s: %s"%(metadata_to_change, body)))
    assert_metadata_value(response_patch_json, metadata_to_change, value_to_change)

    # Step 3: Update the metadata to reset the values to their original state"
    body = {metadata_to_change: original_value}
    response_patch = patch_metadata_for_logged_user(path, headers, body)
    response_patch_json = response_patch.json()
    assert_response_status(response_patch, 200, log.info("We update the %s: %s"%(metadata_to_change, body)))
    assert_metadata_value(response_patch_json, metadata_to_change, original_value)

@pytest.mark.parametrize("metadata_to_change, original_value, value_to_change", zip(LIST_KEYS_METADATA, LIST_ORIGIN_VALUES_METADATA, LIST_VALUES_METADATA))
def test_update_metadata_of_user_auth_not_ok(generate_token, metadata_to_change, original_value, value_to_change):
    token, path = generate_token
    
    headers = {
        'Authorization': "Bearer " + INVALID_TOKEN,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    #Obtengo la información del perfil del usuario (debe fallar)
    response_get_user = get_profile_info_of_a_logged_in_user(path, headers)
    assert response_get_user.status_code == 401, log.info("The user authentication failed with invalid credentials")
    
    # No debería intentar hacer más si no se puede autenticar
    if response_get_user.status_code == 401:
        log.info("User is not authenticated. Skipping metadata update steps due to failed authentication.")
        return

    # Si por alguna razón el test continúa (lo cual no debería con un token inválido), validamos igual
    log.info("Unexpectedly authenticated. Continuing with metadata update...")

    # Step 2: Intentar actualizar la metadata (esto tampoco debería funcionar)
    body = {metadata_to_change: value_to_change}
    response_patch = patch_metadata_for_logged_user(path, headers, body)
    assert response_patch.status_code == 401, log.info("The patch request should fail with invalid credentials")
