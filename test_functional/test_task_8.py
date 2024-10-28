import pytest
from data import *
from services.requests import *
from Logger import logger as log

def test_create_a_gist(generate_token):  
    token, path = generate_token 
    headers = {
        'Authorization': token[0],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    body ={"description":"ejemplo gist lucas", "public":False, "files":{"LeerFichero5.md":{"content":"Prueba 1"}}} 
    response_json_post = post_create_gist(path, headers, body)
    assert response_json_post.status_code == 201

    response_json = response_json_post.json()
    url_gist = response_json['url']
    assert url_gist != '', log.info("la url esta vacía")
    assert response_json["public"] == False

    response_get = requests.get(url_gist, headers)
    response_get_json = response_get.json()
    log.info(response_get_json)

    assert response_get.status_code == 200
    assert "LeerFichero5.md" in response_get_json["files"]["LeerFichero5.md"]["raw_url"]

    # Probar que otra persona no puede acceder a mi gist privado
    raw_url = response_get_json["files"]["LeerFichero5.md"]["raw_url"]

    response_get_raw = requests.get(raw_url)
    response_get_raw_json = response_get_raw.json()
    # response_get_raw.status_code == 