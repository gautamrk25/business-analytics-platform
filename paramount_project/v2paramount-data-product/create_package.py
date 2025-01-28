import os
import subprocess

def create_tar_and_readme():
    # Define paths
    project_dir = "/Users/gautamkotwal/Documents/Code/Onix/Customers/Retail/2025/v2paramount-data-product"
    parent_dir = os.path.dirname(project_dir)
    
    # Create tar file command from parent directory
    tar_command = [
        "tar",
        "--exclude='node_modules'",
        "--exclude='.git'",
        "--exclude='.env'",
        "--exclude='build'",
        "--exclude='dist'",
        "-czf",
        os.path.join(parent_dir, "v2paramount-data-product.tar.gz"),
        "v2paramount-data-product/"
    ]
    
    # Execute tar command from parent directory
    try:
        os.chdir(parent_dir)  # Change to parent directory
        subprocess.run(tar_command, check=True)
        print("✅ Tar file created successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating tar file: {e}")
        return
    
    # Write README file in project directory
    try:
        readme_content = """# V2 Paramount Data Product

## Setup Instructions

1. Extract the tar file:
   ```bash
   tar -xzf v2paramount-data-product.tar.gz
   cd v2paramount-data-product
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy .env.example to .env and fill in required values:
   ```bash
   cp .env.example .env
   ```

4. Run development server:
   ```bash
   npm run dev
   ```

5. Build for production:
   ```bash
   npm run build
   ```
"""
        with open(os.path.join(project_dir, "README.md"), "w") as f:
            f.write(readme_content)
        print("✅ README.md created successfully")
    except Exception as e:
        print(f"❌ Error creating README file: {e}")

if __name__ == "__main__":
    create_tar_and_readme()
