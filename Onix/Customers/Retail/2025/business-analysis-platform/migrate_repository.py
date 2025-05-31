#!/usr/bin/env python3
"""
Repository Migration Script
Migrates the Business Analysis Platform to a new GitHub repository
"""

import os
import subprocess
import sys
import time
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple

class RepositoryMigrator:
    def __init__(self):
        self.old_repo_url = "https://github.com/gautamrk25/2025.git"
        self.new_repo_url = "https://github.com/gautamrk25/business-analytics-platform.git"
        self.repo_name = "business-analytics-platform"
        self.description = "AI-driven business intelligence platform with modular analysis capabilities"
        
    def run_command(self, command: str, check: bool = True) -> Tuple[int, str, str]:
        """Execute a shell command and return the result."""
        print(f"Executing: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if check and result.returncode != 0:
            print(f"Error executing command: {command}")
            print(f"Error output: {result.stderr}")
            sys.exit(1)
            
        return result.returncode, result.stdout, result.stderr
    
    def step1_create_repository_instructions(self):
        """Print instructions for creating the GitHub repository."""
        print("\n" + "="*60)
        print("STEP 1: Create GitHub Repository")
        print("="*60)
        print("\nPlease create a new repository on GitHub with these settings:")
        print(f"1. Go to: https://github.com/new")
        print(f"2. Repository name: {self.repo_name}")
        print(f"3. Description: {self.description}")
        print(f"4. Set to: Public")
        print(f"5. DO NOT initialize with README, .gitignore, or license")
        print(f"6. Click 'Create repository'")
        print("\nPress Enter when you've created the repository...")
        input()
        
    def step2_update_remote_and_push(self):
        """Update git remote and push to new repository."""
        print("\n" + "="*60)
        print("STEP 2: Update Remote and Push Code")
        print("="*60)
        
        # Check current remote
        print("\nCurrent git remote configuration:")
        self.run_command("git remote -v")
        
        # Remove old remote and add new one
        print("\nUpdating remote URL...")
        self.run_command("git remote remove origin", check=False)
        self.run_command(f"git remote add origin {self.new_repo_url}")
        
        # Verify new remote
        print("\nNew remote configuration:")
        self.run_command("git remote -v")
        
        # Push all branches and tags
        print("\nPushing to new repository...")
        self.run_command("git push -u origin main")
        self.run_command("git push --tags", check=False)
        
        print("\n✓ Code successfully pushed to new repository!")
        
    def step3_update_documentation(self):
        """Update all documentation with new repository URL."""
        print("\n" + "="*60)
        print("STEP 3: Update Documentation")
        print("="*60)
        
        # Find all markdown files
        markdown_files = []
        for root, dirs, files in os.walk("."):
            # Skip hidden directories and virtual environments
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        
        print(f"\nFound {len(markdown_files)} markdown files to check")
        
        # Update URLs in each file
        updated_files = []
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if file contains old URL
                if self.old_repo_url in content:
                    # Replace old URL with new URL
                    new_content = content.replace(self.old_repo_url, self.new_repo_url)
                    # Also update the path-specific clone instructions
                    new_content = new_content.replace(
                        "cd 2025/Onix/Customers/Retail/2025/business-analysis-platform",
                        "cd business-analytics-platform"
                    )
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    updated_files.append(file_path)
                    print(f"Updated: {file_path}")
                    
            except Exception as e:
                print(f"Error updating {file_path}: {e}")
        
        if updated_files:
            print(f"\n✓ Updated {len(updated_files)} files")
            
            # Commit the changes
            print("\nCommitting documentation updates...")
            self.run_command("git add -A")
            self.run_command('git commit -m "Update repository URLs after migration"')
            self.run_command("git push origin main")
        else:
            print("\n✓ No files needed updating")
    
    def step4_verify_migration(self):
        """Verify the migration was successful."""
        print("\n" + "="*60)
        print("STEP 4: Verify Migration")
        print("="*60)
        
        # Check remote configuration
        print("\nCurrent remote configuration:")
        self.run_command("git remote -v")
        
        # Test push
        print("\nTesting push to new repository...")
        returncode, stdout, stderr = self.run_command("git push origin main", check=False)
        if returncode == 0:
            print("✓ Push test successful")
        else:
            print("✗ Push test failed - may already be up to date")
        
        # Clone to temporary directory to verify
        print("\nCloning repository to verify all files are present...")
        with tempfile.TemporaryDirectory() as tmpdir:
            clone_path = os.path.join(tmpdir, self.repo_name)
            returncode, stdout, stderr = self.run_command(
                f"git clone {self.new_repo_url} {clone_path}", 
                check=False
            )
            
            if returncode == 0:
                # Count files in cloned repo
                file_count = sum(1 for _ in Path(clone_path).rglob('*') if _.is_file())
                print(f"✓ Successfully cloned repository")
                print(f"✓ Found {file_count} files in cloned repository")
                
                # Check for key files
                key_files = ['README.md', 'requirements.txt', 'main.py', 'COLLABORATOR_GUIDE.md']
                for key_file in key_files:
                    if os.path.exists(os.path.join(clone_path, key_file)):
                        print(f"✓ Key file present: {key_file}")
                    else:
                        print(f"✗ Key file missing: {key_file}")
            else:
                print("✗ Failed to clone repository")
                print(f"Error: {stderr}")
        
        # Update PROJECT_STATUS.md with migration note
        print("\nUpdating PROJECT_STATUS.md with migration note...")
        status_file = "PROJECT_STATUS.md"
        if os.path.exists(status_file):
            with open(status_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add migration note at the top of daily progress
            migration_note = f"""
### {time.strftime('%Y-%m-%d')}
- Successfully migrated repository from {self.old_repo_url} to {self.new_repo_url}
- Updated all documentation to reflect new repository URL
- All git history preserved
- Repository now has a dedicated, professional URL

"""
            
            # Find the daily progress section and insert the note
            if "## Daily Progress Tracking" in content:
                content = content.replace(
                    "## Daily Progress Tracking",
                    f"## Daily Progress Tracking\n{migration_note}"
                )
            else:
                # If section doesn't exist, append to end
                content += f"\n{migration_note}"
            
            with open(status_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Commit the update
            self.run_command(f"git add {status_file}")
            self.run_command('git commit -m "Update PROJECT_STATUS.md with repository migration note"')
            self.run_command("git push origin main")
            
            print("✓ PROJECT_STATUS.md updated with migration note")
        
        print("\n" + "="*60)
        print("MIGRATION COMPLETE!")
        print("="*60)
        print(f"\n✓ Repository successfully migrated to: {self.new_repo_url}")
        print(f"\nNext steps for collaborators:")
        print(f"1. Clone from new URL: git clone {self.new_repo_url}")
        print(f"2. The project is now at the root level (no nested paths)")
        print(f"3. All documentation has been updated with the new URL")

def main():
    """Main execution function."""
    print("Business Analysis Platform - Repository Migration Script")
    print("This script will help you migrate to a new GitHub repository")
    
    # Confirm we're in the right directory
    if not os.path.exists("README.md") or not os.path.exists("main.py"):
        print("\nError: This script must be run from the project root directory")
        print("Please navigate to the business-analysis-platform directory and try again")
        sys.exit(1)
    
    # Create and run migrator
    migrator = RepositoryMigrator()
    
    try:
        # Step 1: Instructions for creating repository
        migrator.step1_create_repository_instructions()
        
        # Step 2: Update remote and push
        migrator.step2_update_remote_and_push()
        
        # Step 3: Update documentation
        migrator.step3_update_documentation()
        
        # Step 4: Verify migration
        migrator.step4_verify_migration()
        
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()