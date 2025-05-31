import os
import tarfile

def create_tar():
    # Name of the output tar file
    tar_name = "omniagent_demo.tar"
    
    # Create tar file
    with tarfile.open(tar_name, "w") as tar:
        # Add index.html
        if os.path.exists("index.html"):
            tar.add("index.html")
        else:
            print("Warning: index.html not found")
            
        # Add images directory
        if os.path.exists("images"):
            tar.add("images")
        else:
            print("Warning: images directory not found")
    
    print(f"Created {tar_name} successfully!")

if __name__ == "__main__":
    create_tar()
