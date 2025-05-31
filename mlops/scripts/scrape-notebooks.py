import requests
import os
from urllib.parse import urljoin

def download_notebook(base_url, notebook_name, save_dir):
    """
    Download a single notebook from GitHub.
    
    Args:
        base_url (str): Base GitHub URL
        notebook_name (str): Name of the notebook file
        save_dir (str): Directory to save the notebook
    """
    # Convert the GitHub tree URL to raw content URL
    raw_url = base_url.replace('tree/main', 'raw/main')
    file_url = urljoin(raw_url + '/', notebook_name)
    
    # Replace URL-encoded characters
    file_url = file_url.replace('%5F', '_')
    
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create save path
        save_path = os.path.join(save_dir, notebook_name)
        
        # Save the notebook
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {notebook_name}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {notebook_name}: {e}")

def main():
    # Base URL
    base_url = "https://github.com/GoogleCloudPlatform/vertex-ai-samples/tree/main/notebooks/official/model_monitoring_v2"
    
    # Save directory
    save_dir = "/Users/gautamkotwal/Documents/Code/Onix/Customers/Retail/2025/mlops/workflow1/current/phoenix-mlops/notebooks/google-examples"
    
    # Create save directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    # List of notebooks to download
    notebooks = [
        # Old experimentation notebooks
        # "build_model_experimentation_lineage_with_prebuild_code.ipynb",
        # "comparing_local_trained_models.ipynb",
        # "comparing_pipeline_runs.ipynb",
        # "delete_outdated_tensorboard_experiments.ipynb",
        # "get_started_with_custom_training_autologging_local_script.ipynb",
        # "get_started_with_vertex_experiments.ipynb",
        # "get_started_with_vertex_experiments_autologging.ipynb",
        "model_monitoring_for_custom_model_batch_prediction_job.ipynb",
        "model_monitoring_for_custom_model_online_prediction.ipynb",
        "model_monitoring_for_model_outside_vertex.ipynb"
    ]
    
    # Download each notebook
    for notebook in notebooks:
        download_notebook(base_url, notebook, save_dir)

if __name__ == "__main__":
    main()
