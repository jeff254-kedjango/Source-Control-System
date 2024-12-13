'''
Test 1: Initialize the repository
This test case initializes the repository by calling the `initialize` method.
It should create the necessary directories, including the 'branches.json' file,
and prepare the repository structure for use.
'''
vcs = MyVCS()
vcs.initialize()  # Should create directories and 'branches.json' file

'''
Test 2: Create a new file
This test case simulates creating a new file in the repository. The user
will be prompted to create a file, and this test checks whether the file
appears in the staging directory.
'''
vcs.prepare_file()  # Allows the user to create a new file and enter content

# Check if the file exists in the staging directory
staged_files = os.listdir(vcs.staging_dir)
print(staged_files)  # Should show the newly created file

'''
Test 3: Commit the changes with a message
In this test, the user commits the staged file(s) with a message.
The test checks whether the commit appears in the commit history.
'''
vcs.commit("Initial commit")  # Commit staged files with a message

# View the commit history
vcs.view_history()  # Should display the commit history with the new commit

'''
Test 4: Create a new branch
This test case simulates the creation of a new branch. The user is expected
to create a new branch called 'feature_branch', and we check whether this
branch is properly recorded in the branches.json file.
'''
vcs.create_branch("feature_branch")

# Check the branches file
with open(vcs.branches_file, 'r') as f:
    branches = json.load(f)
    print(branches)  # Should include the new branch 'feature_branch'

'''
Test 5: Switch to the new branch
In this test, the user switches to the newly created branch. We then verify
that the current branch is correctly set to 'feature_branch'.
'''
vcs.checkout_branch("feature_branch")

# Check the current branch
print(vcs.current_branch)  # Should output 'feature_branch'

'''
Test 6: Create a new branch and make a commit on it
This test creates a new branch, checks out to it, and makes a commit on that branch.
It then merges the feature branch into the main branch and views the commit history.
'''
vcs.create_branch("feature_branch")
vcs.checkout_branch("feature_branch")
vcs.commit("Feature work done")

# Merge the feature branch into main
vcs.checkout_branch("main")
vcs.merge_branch("feature_branch")

# View history after merge
vcs.view_history()  # Should show commits from both branches

'''
Test 7: Simulate a conflict by creating different content in a file on both branches
In this test, the same file is modified in different ways on two branches to simulate a conflict.
We check if the conflict is detected and resolved properly.
'''
vcs.create_branch("feature_branch")
vcs.checkout_branch("feature_branch")
with open("conflict_file.txt", "w") as f:
    f.write("Feature branch version")

vcs.commit("Feature branch commit")

# Switch to main and modify the file
vcs.checkout_branch("main")
with open("conflict_file.txt", "w") as f:
    f.write("Main branch version")

vcs.commit("Main branch commit")

# Merge feature_branch into main, triggering a conflict
vcs.merge_branch("feature_branch")

# Detect and handle conflicts
conflicts = vcs.detect_file_conflicts("feature_branch")
print(conflicts)  # Should list 'conflict_file.txt'

# Handle the conflict
vcs.resolve_merge_conflicts(conflicts)  # User chooses a resolution

'''
Test 8: Handle conflict resolution
This test case is similar to Test 7, and it checks whether the conflict detection and resolution
mechanism is functioning properly. If a conflict occurs, it will be handled by the user.
'''
vcs.create_branch("feature_branch")
vcs.checkout_branch("feature_branch")
with open("conflict_file.txt", "w") as f:
    f.write("Feature branch version")

vcs.commit("Feature branch commit")

# Switch to main and modify the file
vcs.checkout_branch("main")
with open("conflict_file.txt", "w") as f:
    f.write("Main branch version")

vcs.commit("Main branch commit")

# Merge feature_branch into main, triggering a conflict
vcs.merge_branch("feature_branch")

# Detect and handle conflicts
conflicts = vcs.detect_file_conflicts("feature_branch")
print(conflicts)  # Should list 'conflict_file.txt'

# Handle the conflict
vcs.resolve_merge_conflicts(conflicts)  # User chooses a resolution

'''
Test 9: Commit changes
This test verifies that the commit functionality works after bug fixes have been made.
The test checks whether the commit history includes the new commit message.
'''
vcs.commit("Fix bug in feature")

# View commit history
vcs.view_history()  # Should display the commit history with "Fix bug in feature"

'''
Test 10: Add a file to staging
This test case ensures that the staging area can be reset after a file has been added.
We test the reset functionality by checking if the staging area is empty after reset.
'''
vcs.stage_file("test.txt")

# Reset the staging area
vcs.reset_staging()

# Check if the staging area is empty
staged_files = os.listdir(vcs.staging_dir)
print(staged_files)  # Should be empty

'''
Test 11: Simulate file conflict
This test case simulates a conflict in the `example.txt` file after it is modified
on two different branches. The test ensures that conflicts are detected and listed.
'''
vcs.create_branch("feature_branch")
vcs.checkout_branch("feature_branch")
with open("example.txt", "w") as f:
    f.write("Content from feature branch")
vcs.commit("Feature branch changes")

# Switch to main branch and modify the same file
vcs.checkout_branch("main")
with open("example.txt", "w") as f:
    f.write("Content from main branch")
vcs.commit("Main branch changes")

# Merge feature branch into main, expect conflict
vcs.merge_branch("feature_branch")

# Check for conflicts
conflicts = vcs.detect_file_conflicts("feature_branch")
print(conflicts)  # Should detect 'example.txt'

'''
Test 12: Initialize repository and check for required files
In this test, the repository is initialized, and the existence of required directories
and files such as `.myvcs`, `staging`, and `commits` is verified. Additionally,
the branches.json file is checked to ensure it contains the 'main' branch.
'''
import os
import json

# Initialize repository
vcs = MyVCS()
vcs.initialize()

# Check if .myvcs directory exists
print(os.path.exists(vcs.repo_dir))  # Should be True

# Check if staging and commits subdirectories exist
print(os.path.exists(vcs.staging_dir))  # Should be True
print(os.path.exists(vcs.commits_dir))  # Should be True

# Check if branches.json exists and contains the main branch
with open(vcs.branches_file, 'r') as f:
    branches = json.load(f)
    print('main' in branches)  # Should be True
