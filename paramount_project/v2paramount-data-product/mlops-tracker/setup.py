import os
import json

def create_directory_structure():
    # Use current directory as base
    base_dir = os.getcwd()
    
    # Define the directory structure
    directories = [
        "src/components/Header",
        "src/components/ChecklistPanel",
        "src/components/ProgressPanel",
        "src/components/ImplementationView",
        "src/components/CodeEditor",
        "src/components/ResourceDetails",
        "src/components/Notifications",
        "src/hooks",
        "src/interfaces",
        "src/services",
        "src/store",
        "src/styles",
        "src/utils",
        "public/assets"
    ]
    
    # Create directories only if they don't exist
    for dir_path in directories:
        full_path = os.path.join(base_dir, dir_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")
    
    # Create necessary files with basic content
    files = {
        "src/interfaces/types.ts": """
export enum PracticeCategory {
    INITIAL_SETUP = 'Initial Setup',
    DATA_PREPARATION = 'Data Preparation',
    PIPELINE_SETUP = 'Pipeline Setup',
    MODEL_DEVELOPMENT = 'Model Development'
}

export interface Practice {
    id: string;
    category: PracticeCategory;
    title: string;
    description: string;
}
""",
        "src/interfaces/api.ts": """
import { Practice } from './types';

export interface MLOpsTrackerAPI {
    getPractices(): Promise<Practice[]>;
    updatePractice(id: string, updates: Partial<Practice>): Promise<Practice>;
}
""",
        "src/services/mockData.ts": """
import { Practice, PracticeCategory } from '../interfaces/types';

export const mockPractices: Practice[] = [
    {
        id: '1',
        category: PracticeCategory.INITIAL_SETUP,
        title: 'Configure Compute Resources',
        description: 'Set up and configure compute resources for ML workloads'
    }
];
""",
        "src/services/apiClient.ts": """
import { MLOpsTrackerAPI } from '../interfaces/api';
import { mockPractices } from './mockData';

export class ApiClient implements MLOpsTrackerAPI {
    async getPractices() {
        return mockPractices;
    }
    
    async updatePractice(id: string, updates: any) {
        // Mock implementation
        return { ...mockPractices[0], ...updates };
    }
}
""",
        "src/store/index.ts": """
import { createContext } from 'react';
import { Practice } from '../interfaces/types';

export interface AppState {
    practices: Practice[];
}

export const AppContext = createContext<AppState>({ practices: [] });
""",
        "src/styles/globals.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
    --primary-color: #0070f3;
    --background-color: #ffffff;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
        Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
""",
        "src/utils/helpers.ts": """
export function calculateProgress(completed: number, total: number): number {
    return Math.round((completed / total) * 100);
}

export function formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US').format(date);
}
""",
        "package.json": json.dumps({
            "name": "mlops-tracker",
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "@types/node": "^18.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "typescript": "^4.9.0",
                "tailwindcss": "^3.3.0",
                "@headlessui/react": "^1.7.0",
                "@heroicons/react": "^2.0.0"
            },
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            }
        }, indent=2),
        "tsconfig.json": json.dumps({
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "baseUrl": ".",
                "paths": {
                    "@/*": ["./src/*"]
                }
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
            "exclude": ["node_modules"]
        }, indent=2),
        "src/hooks/useClickOutside.ts": """
import { useEffect, RefObject } from 'react';

type Handler = (event: MouseEvent | TouchEvent) => void;

export function useClickOutside<T extends HTMLElement = HTMLElement>(
  ref: RefObject<T>,
  handler: Handler
): void {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      const el = ref?.current;
      if (!el || el.contains((event?.target as Node) || null)) {
        return;
      }

      handler(event);
    };

    document.addEventListener('mousedown', listener);
    document.addEventListener('touchstart', listener);

    return () => {
      document.removeEventListener('mousedown', listener);
      document.removeEventListener('touchstart', listener);
    };
  }, [ref, handler]);
}
""",
        "src/components/Header/UserDropdown.tsx": """
import { useState, useRef } from "react";
import { UserIcon, LogOut, Settings, User } from "lucide-react";
import { useClickOutside } from "../../hooks/useClickOutside";

export const UserDropdown = ({
  userName,
  onLogout,
}: {
  userName: string;
  onLogout: () => void;
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useClickOutside(dropdownRef, () => setIsOpen(false));

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100"
      >
        <UserIcon className="w-5 h-5" />
        <span>{userName}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-1">
          <button className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center space-x-2">
            <User className="w-4 h-4" />
            <span>Profile</span>
          </button>
          <button className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center space-x-2">
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </button>
          <button
            onClick={onLogout}
            className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center space-x-2 text-red-600"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserDropdown;
""",
        "src/components/Header/Header.tsx": """
import React from 'react';
import UserDropdown from './UserDropdown';

export const Header = () => {
    const handleLogout = () => {
        // Implement logout logic
        console.log('Logging out...');
    };

    return (
        <header className="bg-white shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center">
                        <h1 className="text-xl font-bold text-gray-900">MLOps Tracker</h1>
                    </div>
                    <div className="flex items-center">
                        <UserDropdown 
                            userName="John Doe"
                            onLogout={handleLogout}
                        />
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
""",
    }
    
    # Create files only if they don't exist
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content.strip())
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")
            
    # Create empty component index files
    component_dirs = [d for d in directories if d.startswith('src/components/')]
    for comp_dir in component_dirs:
        index_path = os.path.join(base_dir, comp_dir, 'index.tsx')
        component_name = os.path.basename(comp_dir)
        with open(index_path, 'w') as f:
            f.write(f"""
import React from 'react';

export const {component_name} = () => {{
    return (
        <div>
            <h2>{component_name}</h2>
        </div>
    );
}};

export default {component_name};
""".strip())
        print(f"Created component: {comp_dir}/index.tsx")

if __name__ == "__main__":
    current_dir = os.path.basename(os.getcwd())
    if current_dir != "mlops-tracker":
        print("Error: Please run this script from within the mlops-tracker directory")
        exit(1)
        
    create_directory_structure()
    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Run: npm install")
    print("2. Run: npm run dev")