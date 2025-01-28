import os
import shutil
import datetime
import json
import argparse
from pathlib import Path

class ProjectBackupManager:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.backup_dir = self.project_dir / 'backups'
        self.backup_manifest = self.backup_dir / 'manifest.json'
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize or load manifest
        self.manifest = self._load_manifest()
        
        # Files/directories to exclude from backup
        self.exclude_patterns = [
            'node_modules',
            'backups',
            '.git',
            '__pycache__',
            '*.pyc',
            '.DS_Store',
            'venv',
            'build',
            'dist',
            '.env'
        ]

    def _load_manifest(self):
        if self.backup_manifest.exists():
            with open(self.backup_manifest, 'r') as f:
                return json.load(f)
        return {'backups': []}

    def _save_manifest(self):
        with open(self.backup_manifest, 'w') as f:
            json.dump(self.manifest, f, indent=2)

    def _should_exclude(self, path):
        path_str = str(path)
        return any(pattern in path_str for pattern in self.exclude_patterns)

    def create_backup(self, description=None):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = self.backup_dir / backup_name

        try:
            # Create backup directory
            backup_path.mkdir(exist_ok=True)

            # Copy project files
            for item in self.project_dir.iterdir():
                if not self._should_exclude(item):
                    if item.is_file():
                        shutil.copy2(item, backup_path)
                    elif item.is_dir():
                        shutil.copytree(item, backup_path / item.name, 
                                      ignore=shutil.ignore_patterns(*self.exclude_patterns))

            # Update manifest
            backup_info = {
                'name': backup_name,
                'timestamp': timestamp,
                'description': description or 'No description provided',
                'path': str(backup_path)
            }
            self.manifest['backups'].append(backup_info)
            self._save_manifest()

            print(f"Backup created successfully: {backup_name}")
            return True

        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False

    def list_backups(self):
        if not self.manifest['backups']:
            print("No backups found.")
            return

        print("\nAvailable backups:")
        print("-" * 80)
        for backup in self.manifest['backups']:
            print(f"Name: {backup['name']}")
            print(f"Timestamp: {backup['timestamp']}")
            print(f"Description: {backup['description']}")
            print(f"Path: {backup['path']}")
            print("-" * 80)

    def restore_backup(self, backup_name):
        # Find backup in manifest
        backup = next((b for b in self.manifest['backups'] if b['name'] == backup_name), None)
        if not backup:
            print(f"Backup '{backup_name}' not found.")
            return False

        try:
            backup_path = Path(backup['path'])
            if not backup_path.exists():
                print(f"Backup directory not found: {backup_path}")
                return False

            # Create a safety backup before restore
            safety_backup_name = f"pre_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.create_backup(description="Safety backup before restore")

            # Remove existing project files (except excluded ones)
            for item in self.project_dir.iterdir():
                if not self._should_exclude(item):
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)

            # Restore from backup
            for item in backup_path.iterdir():
                if item.is_file():
                    shutil.copy2(item, self.project_dir)
                elif item.is_dir():
                    shutil.copytree(item, self.project_dir / item.name, 
                                  dirs_exist_ok=True)

            print(f"Successfully restored from backup: {backup_name}")
            return True

        except Exception as e:
            print(f"Error restoring backup: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='React Project Backup Manager')
    parser.add_argument('--project-dir', type=str, default=os.getcwd(),
                       help='Project directory path (default: current directory)')
    parser.add_argument('action', choices=['backup', 'restore', 'list'],
                       help='Action to perform')
    parser.add_argument('--description', type=str, help='Backup description')
    parser.add_argument('--backup-name', type=str, help='Backup name for restore')

    args = parser.parse_args()
    
    manager = ProjectBackupManager(args.project_dir)
    
    if args.action == 'backup':
        manager.create_backup(args.description)
    elif args.action == 'restore':
        if not args.backup_name:
            print("Please provide a backup name to restore")
            manager.list_backups()
        else:
            manager.restore_backup(args.backup_name)
    elif args.action == 'list':
        manager.list_backups()

if __name__ == '__main__':
    main()
    