TOKEN = ""
INVALID_TOKEN = "ghp_uEjHoVCpQ6uAsaLySYNusqOHDYA7fx156yk8"

EXISTING_USERNAME = "Raghav-Pal"
PUBLIC_REPO = "TerraformDemo1"
INVALID_PUBLIC_REPO = "Terraformula"

LIST_INVALID_USERNAMES =  ["non_existing_username_one", "", "user/name"]
USERNAME_HTTP_STATUS_CODE_OK = 200
LIST_USERNAMES_HTTP_STATUS_CODE_NOT_FOUND = [404] * len(LIST_INVALID_USERNAMES)
USER_NOT_FOUND_MESSAGE = "Not Found"

LIST_INVALID_REPO = ["Terraformula", "", "Repo/publico"]
LIST_REPOS_HTTP_STATUS_CODE_NOT_FOUND = [404] * len(LIST_INVALID_REPO)

EXPECTED_KEY_FIELDS_IN_PROFILE = ['login', 'id', 'node_id', 'url', 'public_repos', 'followers', 'following', 'created_at', 'updated_at']

LIST_KEYS_METADATA = ["blog", "bio", "name"]
LIST_ORIGIN_VALUES_METADATA = ['', None, None]
LIST_VALUES_METADATA = ["https://github.com/test_for_an_interview", "My name is Lucas Pierotti and I am Software Engineer", "Lucas"]

# "public_repos" : ["TerraformDemo1", "PythonAutomationFramework_1", "AppiumDemoProject"]

