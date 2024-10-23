

import pytest
import os
import data
import Configfile
import configparser
from Logger import logger as log

def pytest_addoption(parser):
    parser.addoption("--env_local", action="store", default="pr")
    parser.addoption("--trunner", action="store", default="local") 
    # ----toma el valor por defecto a menos que se lo indique por consola

def pytest_configure(config):
    os.environ["env_aux"] = config.getoption("env_local")
    os.environ["trunner"] = config.getoption("trunner")

def load_config(f):
    config = configparser.ConfigParser()
    config.read(f)
    return config

def env_session():
    trunner = os.environ["trunner"]
    if trunner == 'jenkins':
        environment = os.environ["env"]
        print("**** ENVIRONMENT: " + environment + " ****") 
        print ("***** Ejecucion desde JENKINS *****")
        config = load_config(Configfile.CONFIGFILE_JENKINS)
        
    else:
        environment = os.environ["env_aux"]
        print("**** ENVIRONMENT: " + environment + " ****") 
        print ("***** Ejecucion desde LOCAL *****")
        config = load_config(Configfile.CONFIGFILE_LOCAL)
        
    path = config.get(environment, "path")    
    # path_token = config.get(environment, "path_token")
    print ("URL: ", path)
    # print ("URL: ", path_token)
    # return path, path_token
    return path


@pytest.fixture(scope="session")
def generate_token():
    # url, url_token = env_session()
    url = env_session()
    # Aquí lo ideal sería realizar una request a algún endpoint que nos provea auth
    # Enviando un Header y un body
    # headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    # }
        
    # body = {
    #     'username': data.MAIL,
    #     'password' : data.PASSWORD,
    #     'grant_type' : 'password'
    # }
    # response = requests.request("POST", url_token, headers = headers, data = body).json()
    # token = "Bearer " + response['access_token']
    # A fines prácticos enviamos un token valido (obtenido desde github y otro incorrecto)
    token = ["Bearer " + data.TOKEN, "Bearer " + data.INVALID_TOKEN]
    return token, url 




    
    