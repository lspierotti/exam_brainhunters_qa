Feature: GitHub API User Profile and Repository Management Workflow
  As a user of the GitHub API
  I want to interact with various endpoints
  So that I can validate both successful and failed requests, and ensure correct API behavior

  Scenario: Complete workflow to validate user profile, repositories, and commits
    # Step 1: Unauthorized access
    Given the user tries to access their GitHub profile without a Bearer token
    Then the response status should be 401

    # Step 2: Authorized access
    When the user authenticates with a valid Bearer token
    Then the response status should be 200
    Then the user profile should be successfully retrieved

    # Step 3: Update profile field
    When the user updates their profile bio to "Software Engineer"
    Then the profile bio should be updated successfully

    # Step 4: Retrieve updated profile
    When the user retrieves their profile after the update
    Then the profile bio should be "Software Engineer"

    # Step 5: List repositories
    When the user fetches the list of repositories
    Then the response should include both public and private repositories

    # Step 6: Invalid repository
    When the user "lspierotti" attempts to list commits for a non-existent repository named "assembler"
    Then the response status should be 404

    # Step 7: List commits from first repository
    When the user "lspierotti" lists commits from the first repository
    Then the response should include commit details with sha, author, message, and date

    # Step 8: List commits from last repository
    When the user "lspierotti" lists commits from the last repository
    Then the response should include commit details with sha, author, message, and date
