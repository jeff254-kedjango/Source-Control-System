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
            filename = input("Enter the name of the file you want to upload: ")
            if os.path.exists(filename):
                self.stage_file(filename)
                print(f"File '{filename}' uploaded and staged successfully!")
            else:
                print("File not found. Please try again.")

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
        if not os.listdir(self.staging_dir):
            print("No files to commit. Stage files first.")
            return

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
        self.reset_staging()

    def reset_staging(self):
        """
        Clears the staging area to reflect the current branch's state.
        """
        if os.path.exists(self.staging_dir):
            shutil.rmtree(self.staging_dir)
        os.makedirs(self.staging_dir)
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
                shutil.copy(source_file, target_file)
                print(f"File {file_name} merged from branch {source_branch}.")

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
        try:
            # Fetch the latest changes from both branches
            self.repo.git.fetch('origin', self.target_branch)
            self.repo.git.fetch('origin', source_branch)

            # Check out to the target branch and attempt a dry-run merge
            self.repo.git.checkout(self.target_branch)
            self.repo.git.merge('--no-commit', '--no-ff', source_branch)
        except GitCommandError as e:
            if 'CONFLICT' in str(e):
                # Extract conflicting files from the error message
                conflict_files = self._parse_conflict_files(str(e))
                return conflict_files
            else:
                raise
        finally:
            # Abort the merge to maintain a clean state
            self.repo.git.merge('--abort')

        return []  # No conflicts detected

    def _parse_conflict_files(self, error_message):
        """
        Helper method to parse conflict files from a Git error message.
        Args:
            error_message (str): The Git error message.
        Returns:
            List of conflicting file paths.
        """
        conflict_files = []
        for line in error_message.splitlines():
            if line.startswith('CONFLICT (content): Merge conflict in'):
                conflict_files.append(line.split()[-1])
        return conflict_files

    def auto_resolve_conflicts(self, resolution_strategy='ours'):
        """
        Automatically resolves conflicts using a specified strategy.
        Args:
            resolution_strategy (str): Conflict resolution strategy ('ours' or 'theirs').
        """
        valid_strategies = {'ours', 'theirs'}
        if resolution_strategy not in valid_strategies:
            raise ValueError(f"Invalid resolution strategy. Choose from {valid_strategies}.")

        try:
            self.repo.git.checkout('--ours' if resolution_strategy == 'ours' else '--theirs', '.')
            self.repo.git.add('.')
            self.repo.git.commit('-m', f'Auto-resolved conflicts using {resolution_strategy} strategy.')
        except GitCommandError as e:
            raise RuntimeError(f"Failed to auto-resolve conflicts: {str(e)}")

    def merge_and_push(self, source_branch):
        """
        Merges the source branch into the target branch and pushes the changes.
        Args:
            source_branch (str): The name of the branch to merge.
        Returns:
            str: Merge status message.
        """
        conflicts = self.detect_file_conflicts(source_branch)
        if conflicts:
            return f"Merge aborted due to conflicts in files: {', '.join(conflicts)}"

        try:
            self.repo.git.checkout(self.target_branch)
            self.repo.git.merge(source_branch)
            self.repo.git.push('origin', self.target_branch)
            return f"Successfully merged {source_branch} into {self.target_branch} and pushed changes."
        except GitCommandError as e:
            raise RuntimeError(f"Merge and push failed: {str(e)}")

    def create_pr_comment(self, message):
        """
        Creates a comment on the pull request (stubbed for integration with an external PR system).
        Args:
            message (str): The comment message.
        """
        # This is a stub for actual integration with a PR system
        print(f"PR Comment: {message}")

    def execute_merge_workflow(self, source_branch, auto_resolve=False, resolution_strategy='ours'):
        """
        Executes the complete merge workflow with optional auto-resolution of conflicts.
        Args:
            source_branch (str): The name of the branch to merge.
            auto_resolve (bool): Whether to automatically resolve conflicts.
            resolution_strategy (str): Conflict resolution strategy if auto_resolve is True.
        Returns:
            str: Workflow execution status.
        """
        conflicts = self.detect_file_conflicts(source_branch)
        if conflicts:
            if auto_resolve:
                self.auto_resolve_conflicts(resolution_strategy)
                self.repo.git.push('origin', self.target_branch)
                return f"Conflicts auto-resolved using {resolution_strategy} strategy and changes pushed."
            else:
                return f"Merge aborted due to conflicts in files: {', '.join(conflicts)}"

        return self.merge_and_push(source_branch)

