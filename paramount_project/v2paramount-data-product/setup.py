import os
import json

def create_directory_structure():
    # Base directory is current directory
    base_dir = os.getcwd()
    
    # Create directories
    directories = [
        'public',
        'src',
        'src/components'
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

def create_files():
    # Create index.html
    index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="Paramount Data Product" />
    <title>Paramount Data Product</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
    
    # Create index.js
    index_js = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''
    
    # Create index.css
    index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;'''
    
    # Create package.json
    package_json = {
        "name": "v2paramount-data-product",
        "version": "1.0.0",
        "private": True,
        "dependencies": {
            "@radix-ui/react-slot": "^1.1.0",
            "autoprefixer": "^10.4.20",
            "lucide-react": "^0.292.0",
            "postcss": "^8.4.49",
            "react": "^18.3.1",
            "react-dom": "^18.3.1",
            "react-scripts": "^5.0.1",
            "recharts": "^2.13.3",
            "tailwindcss": "^3.4.15"
        },
        "scripts": {
            "start": "PORT=5174 react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "eslintConfig": {
            "extends": ["react-app"]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        }
    }
    
    # Create tailwind.config.js
    tailwind_config = '''module.exports = {
  content: ['./src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}'''
    
    # Create postcss.config.js
    postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}'''

    # Write all files
    files_to_create = {
        'public/index.html': index_html,
        'src/index.js': index_js,
        'src/index.css': index_css,
        'package.json': json.dumps(package_json, indent=2),
        'tailwind.config.js': tailwind_config,
        'postcss.config.js': postcss_config
    }
    
    for file_path, content in files_to_create.items():
        full_path = os.path.join(os.getcwd(), file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)

def main():
    try:
        create_directory_structure()
        create_files()
        print("✅ Project structure and files created successfully!")
        print("\nNext steps:")
        print("1. Run: npm install")
        print("2. Run: npm start")
        print("3. Open: http://localhost:5174")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()