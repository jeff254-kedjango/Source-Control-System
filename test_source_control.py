import os
import json

# Test 1: Initialize the repository
vcs = MyVCS()
vcs.initialize()  # Should create directories and 'branches.json' file

# Test 2: Create a new file
vcs.prepare_file()  # Allows the user to create a new file and enter content

# Check if the file exists in the staging directory
staged_files = os.listdir(vcs.staging_dir)
print(staged_files)  # Should show the newly created file

# Test 3: Commit the changes with a message
vcs.commit("Initial commit")  # Commit staged files with a message

# View the commit history
vcs.view_history()  # Should display the commit history with the new commit

# Test 4: Create a new branch
vcs.create_branch("feature_branch")

# Check the branches file
with open(vcs.branches_file, 'r') as f:
    branches = json.load(f)
    print(branches)  # Should include the new branch 'feature_branch'

# Test 5: Switch to the new branch
vcs.checkout_branch("feature_branch")

# Check the current branch
print(vcs.current_branch)  # Should output 'feature_branch'

# Test 6: Create a new branch and make a commit on it
vcs.create_branch("feature_branch")
vcs.checkout_branch("feature_branch")
vcs.commit("Feature work done")

# Merge the feature branch into main
vcs.checkout_branch("main")
vcs.merge_branch("feature_branch")

# View history after merge
vcs.view_history()  # Should show commits from both branches

# Test 7: Simulate a conflict by creating different content in a file on both branches
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

# Test 8: Simulate a conflict again with different content in the file
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

# Test 9: Commit changes
vcs.commit("Fix bug in feature")

# View commit history
vcs.view_history()  # Should display the commit history with "Fix bug in feature"

# Test 10: Add a file to staging
vcs.stage_file("test.txt")

# Reset the staging area
vcs.reset_staging()

# Check if the staging area is empty
staged_files = os.listdir(vcs.staging_dir)
print(staged_files)  # Should be empty

# Test 11: Simulate file conflict
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

# Test 12: Check directory and file existence
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
