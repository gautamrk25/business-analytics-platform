import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import time
import hashlib

def get_safe_filename(url):
    # Create a filename from the URL path
    path = urlparse(url).path
    # Remove leading/trailing slashes and replace remaining slashes with underscores
    filename = path.strip('/').replace('/', '_')
    # Add .html extension if not present
    if not filename.endswith('.html'):
        filename += '.html'
    # If filename is empty, use the hash of the full URL
    if not filename:
        filename = hashlib.md5(url.encode()).hexdigest() + '.html'
    return filename

def download_page(url, output_dir):
    try:
        # Add delay to be respectful to the server
        time.sleep(1)
        
        response = requests.get(url)
        response.raise_for_status()
        
        # Create safe filename from URL
        filename = get_safe_filename(url)
        filepath = os.path.join(output_dir, filename)
        
        # Save the page content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Downloaded: {url} -> {filename}")
        return response.text
        
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return None

def extract_vertex_ai_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    
    # Find all links that contain 'vertex-ai/docs/experiments'
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if 'vertex-ai/docs/experiments' in full_url:
            links.add(full_url)
            
    return links

def main():
    # Create output directory
    output_dir = '/Users/gautamkotwal/Documents/Code/Onix/Customers/Retail/2025/mlops/workflow1/current/context/experiment-google-docs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Start with the main page
    base_url = 'https://cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments'
    visited_urls = set()
    urls_to_visit = {base_url}
    
    while urls_to_visit:
        current_url = urls_to_visit.pop()
        
        if current_url in visited_urls:
            continue
            
        print(f"\nProcessing: {current_url}")
        
        # Download the current page
        content = download_page(current_url, output_dir)
        if content:
            visited_urls.add(current_url)
            
            # Extract new links from the page
            new_links = extract_vertex_ai_links(content, base_url)
            urls_to_visit.update(new_links - visited_urls)
            
        print(f"Processed URLs: {len(visited_urls)}")
        print(f"URLs remaining: {len(urls_to_visit)}")

if __name__ == "__main__":
    main()
