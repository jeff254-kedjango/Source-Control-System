import os
import shutil
import json
import time

class MyVCS:
    def __init__(self):
        """
        Initialize the MyVCS class with necessary directory and file paths.
        Ensures the repository, staging, and commits structure is clearly defined.
        """
        self.repo_dir = ".myvcs"
        self.staging_dir = os.path.join(self.repo_dir, "staging")
        self.commits_dir = os.path.join(self.repo_dir, "commits")
        self.branches_file = os.path.join(self.repo_dir, "branches.json")
        self.current_branch = "main"

    def initialize(self):
        """
        Initializes the version control repository if it does not already exist.
        Creates necessary directories and files and prompts user to prepare files.
        """
        if not os.path.exists(self.repo_dir):
            os.makedirs(self.staging_dir)
            os.makedirs(self.commits_dir)
            with open(self.branches_file, 'w') as f:
                json.dump({"main": []}, f)
            print("Repository initialized.")

            # Guide the user to create or upload a file after initialization
            self.prepare_file()
        else:
            print("Repository already exists.")

    def prepare_file(self):
        """
        Guides the user to create or upload a file for version control.
        Offers options for creating a new file, uploading, or skipping this step.
        """
        print("\nWelcome! Let's get started.")
        choice = input("Do you want to: \n(1) Create a new file \n(2) Upload an existing file \n(3) Skip this step (initialize repo) \nEnter 1, 2, or 3: ")

        if choice == '1':
            filename = input("Enter the name of the new file (e.g., 'example.txt'): ")
            content = input("Enter the content for the file: ")
            with open(filename, 'w') as f:
                f.write(content)
            print(f"File '{filename}' created successfully!")
            self.stage_file(filename)

        elif choice == '2':
            try:
                # Attempting to use Google Colab file upload feature
                from google.colab import files
                print("Please select the file to upload:")
                uploaded = files.upload()
                if uploaded:
                    file_name = list(uploaded.keys())[0]
                    print(f"File '{file_name}' uploaded successfully!")
                    self.stage_file(file_name)
                else:
                    print("No file uploaded.")
            except ImportError:
                # Handle non-Colab environments, and prompt user to manually upload a file
                print("Google Colab's file upload is not available in this environment. Please manually upload a file to continue.")
                filename = input("Enter the name of the file you want to upload: ")
                self.stage_file(filename)

        elif choice == '3':
            print("Skipping file creation/upload. Repository initialized.")

        else:
            print("Invalid choice. Please try again.")
            self.prepare_file()

    def stage_file(self, file_path):
        """
        Adds a file to the staging area, ensuring no duplicate staging.
        Args:
            file_path (str): Path of the file to stage.
        """
        if not os.path.exists(self.staging_dir):
            os.makedirs(self.staging_dir)

        staged_files = os.listdir(self.staging_dir)
        if file_path in staged_files:
            print(f"File {file_path} is already staged.")
            return

        shutil.copy(file_path, self.staging_dir)
        print(f"{file_path} added to staging area.")

    def commit(self, message):
        """
        Creates a commit by saving staged files and recording metadata.
        Args:
            message (str): Commit message describing the changes.
        """
        if not os.path.exists(self.staging_dir):
            os.makedirs(self.staging_dir)

        commit_id = len(os.listdir(self.commits_dir)) + 1
        commit_path = os.path.join(self.commits_dir, f"commit_{commit_id}")
        shutil.copytree(self.staging_dir, commit_path)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        with open(self.branches_file, 'r+') as f:
            branches = json.load(f)
            branches[self.current_branch].append({
                "id": commit_id,
                "message": message,
                "timestamp": timestamp
            })
            f.seek(0)
            json.dump(branches, f, indent=4)

        shutil.rmtree(self.staging_dir)
        print(f"Commit {commit_id} created: {message}")

    def view_history(self):
        """
        Displays the commit history of the current branch.
        """
        with open(self.branches_file, 'r') as f:
            branches = json.load(f)

        print(f"History for branch {self.current_branch}:")
        for commit in branches[self.current_branch]:
            print(f"Commit {commit['id']} | {commit['message']}")
            print(f"Timestamp: {commit.get('timestamp', 'N/A')}")

    def create_branch(self, branch_name):
        """
        Creates a new branch by copying the commit history of the current branch.
        Args:
            branch_name (str): Name of the new branch.
        """
        with open(self.branches_file, 'r+') as f:
            branches = json.load(f)
            if branch_name in branches:
                print("Branch already exists.")
                return
            branches[branch_name] = branches[self.current_branch].copy()
            f.seek(0)
            json.dump(branches, f, indent=4)
        print(f"Branch {branch_name} created.")

    def checkout_branch(self, branch_name):
            """
            Switches to a different branch and resets the staging area.
            Args:
                branch_name (str): Name of the branch to switch to.
            """
            with open(self.branches_file, 'r') as f:
                branches = json.load(f)
            if branch_name not in branches:
                print("Branch does not exist.")
                return
            self.current_branch = branch_name
            print(f"Switched to -> {branch_name}.")
            # Ensure staging directory exists before resetting it
            if not os.path.exists(self.staging_dir):  
                os.makedirs(self.staging_dir)
            self.reset_staging()

    def reset_staging(self):
        """
        Clears the staging area to reflect the current branch's state.
        """
        staged_files = os.listdir(self.staging_dir)
        for file in staged_files:
            os.remove(os.path.join(self.staging_dir, file))
        print(f"Staging area reset for -> {self.current_branch}.")

    def merge_branch(self, source_branch):
        """
        Merges the commit history and file content from another branch.
        Args:
            source_branch (str): Name of the branch to merge into the current branch.
        """
        with open(self.branches_file, 'r+') as f:
            branches = json.load(f)
            if source_branch not in branches:
                print("Source branch does not exist.")
                return

            branches[self.current_branch].extend(branches[source_branch])
            f.seek(0)
            json.dump(branches, f, indent=4)

        print(f"Branch {source_branch} merged into {self.current_branch}.")
        self.apply_merge_changes(source_branch)

    def apply_merge_changes(self, source_branch):
            """
            Applies file changes from a merged branch into the staging area.
            Args:
                source_branch (str): Name of the branch being merged.
            """
            source_commits = self.get_commits_for_branch(source_branch)
            for commit in source_commits:
                commit_path = os.path.join(self.commits_dir, f"commit_{commit['id']}")
                for file_name in os.listdir(commit_path):
                    source_file = os.path.join(commit_path, file_name)
                    target_file = os.path.join(self.staging_dir, file_name)
                    # Check if the staging directory exists and create if needed
                    if not os.path.exists(self.staging_dir):
                        os.makedirs(self.staging_dir)  # Create the staging directory 
                    # Check if the source file exists before copying 
                    if os.path.exists(source_file):  
                        if not os.path.exists(target_file):
                            shutil.copy(source_file, target_file)
                        print(f"File {file_name} merged from branch {source_branch}.")
                    else:
                        print(f"Warning: Source file '{source_file}' not found. Skipping.")

    def get_commits_for_branch(self, branch_name):
        """
        Retrieves the commit history for a specified branch.
        Args:
            branch_name (str): Name of the branch to retrieve commits for.
        Returns:
            List of commits for the branch.
        """
        with open(self.branches_file, 'r') as f:
            branches = json.load(f)
        return branches.get(branch_name, [])

    def detect_file_conflicts(self, source_branch):
        """
        Detects file conflicts during branch merging.
        Args:
            source_branch (str): The name of the branch being merged.
        Returns:
            List of conflicting files, if any.
        """
        conflicts = []
        source_commits = self.get_commits_for_branch(source_branch)
        target_commits = self.get_commits_for_branch(self.current_branch)

        # Check for files present in both branches with differing content
        for commit in source_commits:
            source_commit_path = os.path.join(self.commits_dir, f"commit_{commit['id']}")
            for file_name in os.listdir(source_commit_path):
                source_file = os.path.join(source_commit_path, file_name)
                target_commit_path = os.path.join(self.commits_dir, f"commit_{target_commits[-1]['id']}")
                target_file = os.path.join(target_commit_path, file_name)

                if os.path.exists(target_file) and not self.files_are_identical(source_file, target_file):
                    conflicts.append(file_name)

        return conflicts

    def files_are_identical(self, file1, file2):
        """
        Compares two files to see if they are identical.
        Args:
            file1 (str): Path of the first file.
            file2 (str): Path of the second file.
        Returns:
            bool: True if files are identical, otherwise False.
        """
        return open(file1, 'rb').read() == open(file2, 'rb').read()

    def resolve_merge_conflicts(self, conflicting_files):
        """
        Resolves conflicts by providing the user with options to choose a resolution strategy.
        Args:
            conflicting_files (list): List of conflicting files to resolve.
        """
        print("Merge conflicts detected!")
        print("Conflicting files:")
        for idx, file in enumerate(conflicting_files, 1):
            print(f"{idx}. {file}")

        choice = input("Choose how to resolve conflicts:\n1. Keep current branch's version\n2. Use the version from the merged branch\n3. Manually resolve\nEnter 1, 2, or 3: ")

        if choice == '1':
            print("Keeping current branch's version.")
        elif choice == '2':
            print("Using the version from the merged branch.")
        elif choice == '3':
            print("Please manually resolve the conflicts in the conflicting files.")
            # You may add functionality here to open the files in a text editor for manual resolution.
        else:
            print("Invalid choice, no conflicts resolved.")
