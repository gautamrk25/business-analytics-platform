#!/usr/bin/env python3
"""
Repository Migration Prompt Generator for Claude Opus 4
This script generates prompts for Claude to execute the migration step by step
"""

import os
import sys
import time
import subprocess
from datetime import datetime

class MigrationPromptGenerator:
    def __init__(self):
        self.old_repo_url = "https://github.com/gautamrk25/2025.git"
        self.new_repo_url = "https://github.com/gautamrk25/business-analytics-platform.git"
        self.repo_name = "business-analytics-platform"
        self.current_dir = os.getcwd()
        self.prompts = []
        
    def generate_prompt_file(self, step_num: int, title: str, prompt: str):
        """Generate a prompt file for each step."""
        filename = f"migration_step_{step_num}_{title.lower().replace(' ', '_')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"STEP {step_num}: {title}\n")
            f.write("="*60 + "\n\n")
            f.write("Copy and paste this entire prompt into Claude Opus 4:\n")
            f.write("-"*60 + "\n\n")
            f.write(prompt)
            f.write("\n\n" + "-"*60 + "\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.prompts.append((step_num, title, filename))
        print(f"✓ Created: {filename}")
        
    def check_prerequisites(self):
        """Check if we're in the right directory and have git."""
        if not os.path.exists("README.md") or not os.path.exists("main.py"):
            print("Error: This script must be run from the project root directory")
            sys.exit(1)
            
        # Check git status
        result = subprocess.run("git status", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error: Not a git repository")
            sys.exit(1)
            
    def generate_all_prompts(self):
        """Generate all migration prompts."""
        
        # Prompt 0: Initial setup verification
        prompt0 = f"""I'm preparing to migrate my repository. Please help me verify my current setup.

Current directory: {self.current_dir}
Expected files: README.md, main.py, requirements.txt

Please:
1. Verify I'm in the correct directory by checking for key files
2. Check my current git remote with: git remote -v
3. Confirm the current remote is: {self.old_repo_url}
4. Check if there are any uncommitted changes with: git status

Let me know if everything looks ready for migration."""

        self.generate_prompt_file(0, "Verify Setup", prompt0)
        
        # Prompt 1: GitHub repository creation instructions
        prompt1 = f"""I need detailed instructions to create a new GitHub repository. I will create it manually through the GitHub web interface.

Please provide step-by-step instructions with exact settings:
- Repository name: {self.repo_name}
- Description: "AI-driven business intelligence platform with modular analysis capabilities"
- Visibility: Public
- Initialize: DO NOT add README, .gitignore, or license

After I create it, I'll have an empty repository at: {self.new_repo_url}

Please list the exact steps I should follow on github.com/new"""

        self.generate_prompt_file(1, "Create Repository", prompt1)
        
        # Prompt 2: Update remote and push
        prompt2 = f"""I have successfully created a new empty GitHub repository at {self.new_repo_url}

I need to migrate my existing code from {self.old_repo_url} to this new repository.

Current situation:
- Current directory: {self.current_dir}
- Old remote URL: {self.old_repo_url}
- New remote URL: {self.new_repo_url}
- All changes are committed and pushed to the old repository

Please execute these git commands for me:
1. First, show current remote: git remote -v
2. Remove the old remote: git remote remove origin
3. Add the new remote: git remote add origin {self.new_repo_url}
4. Verify the new remote: git remote -v
5. Push main branch: git push -u origin main
6. Push all tags: git push --tags

Show me the output of each command as you execute them."""

        self.generate_prompt_file(2, "Update Remote and Push", prompt2)
        
        # Prompt 3: Update documentation
        prompt3 = f"""The code has been successfully pushed to {self.new_repo_url}

Now I need to update all documentation files that reference the old repository URL.

Please:
1. Search for all markdown files in the current directory and subdirectories
2. In each markdown file, replace:
   - Old URL: {self.old_repo_url}
   - New URL: {self.new_repo_url}
3. Also update any path references:
   - Old: "cd 2025/Onix/Customers/Retail/2025/business-analysis-platform"
   - New: "cd business-analytics-platform"
4. Show me which files were updated and what changes were made
5. After updating all files, create a git commit with the message: "Update repository URLs after migration"
6. Push the commit to the new repository

Please show me each file that gets updated and confirm the changes."""

        self.generate_prompt_file(3, "Update Documentation", prompt3)
        
        # Prompt 4: Verify migration
        prompt4 = f"""The repository migration should now be complete. Please help me verify everything worked correctly.

Please perform these verification steps:

1. Check the current git remote configuration:
   - Run: git remote -v
   - Confirm it shows: {self.new_repo_url}

2. Test pushing to the new repository:
   - Run: git push origin main
   - Confirm it succeeds (or says "Everything up-to-date")

3. Verify the repository by cloning it to a temporary directory:
   - Create a temp directory
   - Clone: git clone {self.new_repo_url} temp_verify
   - List the files in temp_verify
   - Check for key files: README.md, main.py, requirements.txt, COLLABORATOR_GUIDE.md
   - Count total files
   - Remove the temp directory

4. Update PROJECT_STATUS.md with a migration note:
   - Add an entry under "Daily Progress Tracking" with today's date
   - Note: "Successfully migrated repository from {self.old_repo_url} to {self.new_repo_url}"
   - Commit with message: "Update PROJECT_STATUS.md with repository migration note"
   - Push to the new repository

5. Provide a final summary confirming:
   - All files are present in the new repository
   - Documentation has been updated
   - Git history is preserved
   - The new repository URL for sharing: {self.new_repo_url}"""

        self.generate_prompt_file(4, "Verify Migration", prompt4)
        
        # Create a master prompt file with instructions
        master_content = f"""Repository Migration Prompts for Claude Opus 4
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This directory now contains {len(self.prompts)} prompt files for migrating your repository.

INSTRUCTIONS:
=============
1. Open Claude Opus 4 (claude.ai)
2. Start a new conversation
3. Work through each prompt file in order:
"""
        
        for step_num, title, filename in self.prompts:
            master_content += f"\n   Step {step_num}: {title}\n"
            master_content += f"   File: {filename}\n"
            master_content += f"   Action: Copy the entire prompt from this file and paste into Claude\n"
            master_content += f"   Wait: Let Claude complete this step before moving to the next\n"
        
        master_content += f"""
IMPORTANT NOTES:
================
- Complete each step before moving to the next
- Step 1 requires manual action on GitHub.com
- All other steps will be executed by Claude
- Keep all prompt files until migration is complete
- After migration, share this URL with collaborators: {self.new_repo_url}

VERIFICATION:
=============
After completing all steps, you should:
- Have a new repository at {self.new_repo_url}
- All code and history migrated
- All documentation updated with new URLs
- Be able to clone with: git clone {self.new_repo_url}
"""
        
        with open("MIGRATION_INSTRUCTIONS.txt", 'w', encoding='utf-8') as f:
            f.write(master_content)
            
        print(f"\n✓ Created: MIGRATION_INSTRUCTIONS.txt (START HERE)")

def main():
    """Main execution function."""
    print("Repository Migration Prompt Generator for Claude Opus 4")
    print("="*60)
    
    generator = MigrationPromptGenerator()
    
    # Check prerequisites
    print("\nChecking prerequisites...")
    generator.check_prerequisites()
    print("✓ Prerequisites checked")
    
    # Generate all prompts
    print("\nGenerating migration prompts...")
    generator.generate_all_prompts()
    
    print("\n" + "="*60)
    print("SUCCESS! Migration prompts have been generated.")
    print("="*60)
    print("\nNEXT STEPS:")
    print("1. Open MIGRATION_INSTRUCTIONS.txt")
    print("2. Follow the instructions to use each prompt with Claude Opus 4")
    print("3. Complete each step in order")
    print("\nThe prompts will guide Claude to perform the exact same migration")
    print("that the automated script would have done.")
    
    # Create a .gitignore entry for the prompt files
    print("\nNote: You may want to add these prompt files to .gitignore:")
    print("migration_step_*.txt")
    print("MIGRATION_INSTRUCTIONS.txt")

if __name__ == "__main__":
    main()