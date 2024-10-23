The objective of this project is to test GitHub API Endpoints

- There are two test folders: `test_functional` and `test_bdd`. In the first folder, all the tests for tasks 1 through 6 are located. The second folder, `test_bdd`, contains a test related to the workflow described in task 7. It could have also been developed as a series of functional tests in a cascade, but BDD was chosen because, given that it's a workflow, one can define the step definitions, making it clearer.

- The `data.py` file contains variables that will be used in the test files (many of them are used in the test parameterizations).
  
- - IMPORTANT: The token is provided through my personal GitHub account. It is stored in a variable called `TOKEN` in the data.py file. However, when committing the code, we will not include it. This means the tests will not run unless the corresponding key is provided.

- - IMPORTANT: In the `conftest.py` file, the logic for the project is defined. It was designed to be run either locally or from a Jenkins environment. However, what is commonly done is making a request with certain credentials to authenticate. Since we don't have access to that request, the tokens are hardcoded.
 
- The `Logger.py` file and log.log simply log the events occurring in the tests.

- The `pytest.ini` file sets the execution mode: either local or from jenkins.

- To run it in local way:

    - In the `pytest.ini` file, uncomment line 4 and edit the variable named:
        env_local
    - In the `pytest.ini` file, comment out line 3, as this is for executing via Jenkins. Note: remember to restore the file to its original state, meaning it should be ready for Jenkins execution.En el archivo pytest.ini, descomentar la linea 4 y editar la variable cuyo nombre es:



| Test | File | Objetive |
|----------|:-------------:|------:|
| 1 | test_task_1.py | It is understood that the request is made "without sending the token." Tests are also performed to access non-existent users or usernames that "break" the URL (e.g., "user/name"). |
| 2 | test_task_2.py | Tests are performed on a logged-in user (with token submission), and not only is the status code analyzed, but also the presence of specific fields.|
| 3 | test_task_3.py | Test 3 aims to list all public repositories of a user. Additionally, tests are conducted to access a repository of an invalid user. |
| 4 | test_task_4.py | Test 4 is designed to retrieve all repositories, both public and private, of an authenticated user. The response was analyzed, and it was observed that if the "private" attributes were set to False, the visibility was public. Tests are performed accordingly. |
| 5 | test_task_5.py | Test 5 checks the commits of a user's repository. Status code tests are performed, but it also verifies that the commit hashes are different (hence the set(list_sha)). Additionally, it checks what happens when attempting to access the commits of a valid user but from a non-existent repository. |
| 6 | test_task_6.py | Test 6 aims to test the editing of some user parameters. The bio, blog, and name are updated, and the test concludes by restoring the values to their original state.

In the flow of the `test_bdd`, there is a moment when it requests to edit a user attribute (the bio), but the flow never suggests reverting it to its original state. This means that if the `test_bdd` is executed and then `test_6` is run, conflicts will arise.

To prevent this issue, after executing the `test_bdd`, there is a `test_update_bio.py` that resets the values accordingly, ensuring that `test_6` can be executed without conflicts.|
