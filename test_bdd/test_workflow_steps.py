import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from services.requests import *

# Vincula el archivo .feature con el test
scenarios('/Users/lucaspierotti/Documents/main/propio/testing-personal/examen_pytest_brainhunters_lucas/features/test_workflow.feature')

# Step 1: Step definition for retrieving the profile without authentication (401 Unauthorized)
@given('the user tries to access their GitHub profile without a Bearer token')
def get_profile_without_token(generate_token):
    token, path = generate_token
    headers = {
        'Accept': 'application/vnd.github+json',
    }
    response = get_profile_info_of_a_logged_in_user(path, headers)
    pytest.response = response

@then('the response status should be 401')
def check_unauthorized_status():
    assert pytest.response.status_code == 401, f"Expected status code 401, but got {pytest.response.status_code}"


# Step 2: Autenticación con Bearer Token válido
@when('the user authenticates with a valid Bearer token')
def get_profile_with_valid_token(generate_token):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    response = get_profile_info_of_a_logged_in_user(path, headers)
    pytest.response = response

@then('the response status should be 200')
def check_ok_status():
    assert pytest.response.status_code == 200, f"Expected status code 200, but got {pytest.response.status_code}"

@then('the user profile should be successfully retrieved')
def validate_user_profile():
    json_response = pytest.response.json() #validar que el usuario sea el mio: lucas
    assert 'login' in json_response, "User profile data not found in the response"
    assert json_response["login"] == "lspierotti"

# Step 3: Actualización de un campo del perfil (bio)
@when(parsers.parse('the user updates their profile bio to "{new_bio}"'))
def update_user_profile(generate_token, new_bio):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    body = {"bio": new_bio}
    response = patch_metadata_for_logged_user(path, headers, body)
    pytest.response = response

@then('the profile bio should be updated successfully')
def validate_profile_update():
    json_response = pytest.response.json()
    assert pytest.response.status_code == 200, f"Expected status code 200, but got {pytest.response.status_code}"
    assert json_response["bio"] == "Software Engineer", "Bio was not updated successfully"

# Step 4: Validación de perfil actualizado
@when('the user retrieves their profile after the update')
def get_updated_profile(generate_token):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    response = get_profile_info_of_a_logged_in_user(path, headers)
    pytest.response = response

@then(parsers.parse('the profile bio should be "{expected_bio}"'))
def check_profile_bio(expected_bio):
    json_response = pytest.response.json()
    assert json_response.get("bio") == expected_bio, f"Expected bio to be '{expected_bio}', but got {json_response.get('bio')}"

# Step 5: Listar repositorios del usuario
@when('the user fetches the list of repositories')
def list_user_repositories(generate_token):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    response = get_all_repos_for_a_logged_in_user(path, headers)
    pytest.response = response

@then('the response should include both public and private repositories')
def validate_repositories_list():
    json_response = pytest.response.json()
    assert pytest.response.status_code == 200, f"Expected status code 200, but got {pytest.response.status_code}"
    assert isinstance(json_response, list), "Expected a list of repositories, but got something else"
    # Asegura que haya al menos un repositorio privado o público
    total_repos = len(json_response)
    count_private = sum(1 for repo in json_response if repo["private"] == True)
    count_public = sum(1 for repo in json_response if repo["private"] == False)

    assert total_repos == count_private + count_public, "the sum of public repos and private repos is not the same as the total repos"

# Step 6: Listar commits de repositorio inexistente
@when(parsers.parse('the user "{user}" attempts to list commits for a non-existent repository named "{repo_name}"'))
def list_commits_invalid_repo(generate_token, user, repo_name):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    response = get_all_commits_for_a_public_repo(path, headers, user, repo_name)
    pytest.response = response

@then('the response status should be 404')
def check_not_found_status():
    assert pytest.response.status_code == 404, f"Expected status code 404, but got {pytest.response.status_code}"

# Step 7: Listar commits de los repositorios del usuario
@when(parsers.parse('the user "{user}" lists commits from the first repository'))
def list_commits_first_repo(generate_token, user):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    response_repo = get_all_repos_for_a_logged_in_user(path, headers).json()
    first_repo = response_repo[0]
    response = get_all_commits_for_a_public_repo(path, headers, user, first_repo["name"])
    pytest.response = response

# Step 8: Listar commits de los repositorios del usuario
@when(parsers.parse('the user "{user}" lists commits from the last repository'))
def list_commits_last_repo(generate_token, user):
    token, path = generate_token
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
    }
    
    response_repo = get_all_repos_for_a_logged_in_user(path, headers).json()
    last_repo = response_repo[-1]
    response = get_all_commits_for_a_public_repo(path, headers, user, last_repo["name"])
    pytest.response = response

@then('the response should include commit details with sha, author, message, and date')
def validate_commit_details():
    json_response = pytest.response.json()
    assert pytest.response.status_code == 200, f"Expected status code 200, but got {pytest.response.status_code}"
    assert all(all(key in commit['commit'] for key in ['author', 'message']) for commit in json_response), "Commit details are incomplete"