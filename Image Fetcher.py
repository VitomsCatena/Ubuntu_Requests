import os
import requests
import re
from urllib.parse import urlparse

def get_valid_filename(https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Felephant%2F&psig=AOvVaw1MDx63RF_QchFbdOulXGZK&ust=1757825967788000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCJiLz5X61I8DFQAAAAAdAAAAABAE):
    """
    Generates a valid filename from a URL.
    This function sanitizes the URL to remove invalid characters
    and extracts the original filename if available.
    """
    # Parse the URL to get the path
    parsed_url = urlparse(https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Felephant%2F&psig=AOvVaw1MDx63RF_QchFbdOulXGZK&ust=1757825967788000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCJiLz5X61I8DFQAAAAAdAAAAABAE)
    path = parsed_url.path

    # Extract the base filename from the URL path
    filename = os.path.basename(path)
    
    # If the filename is empty, create a generic one
    if not filename:
        filename = "downloaded_image"
        
    # Sanitize the filename to remove invalid characters
    # Only keep alphanumeric characters, underscores, hyphens, and dots
    sanitized_filename = re.sub(r'[^\w\.\-]', '_', filename)
    
    return sanitized_filename

def download_image():
    """
    Prompts the user for a URL, downloads the image, and saves it
    to the 'Fetched_Images' directory.
    """
    # Create the directory if it doesn't already exist
    # Using exist_ok=True prevents an error if the directory is already there
    try:
        os.makedirs("Fetched_Images", exist_ok=True)
        print("Directory 'Fetched_Images' is ready.")
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    # Prompt the user for the URL
    image_url = input("Please enter the URL of the image you want to download: ")

    try:
        # Use requests.get() to download the image in a stream
        # This is more memory-efficient for large files
        print(f"Connecting to the community to fetch {image_url}...")
        response = requests.get(image_url, stream=True, timeout=10)
        
        # Raise an exception for bad HTTP status codes (e.g., 404, 500)
        response.raise_for_status()

        # Get a sanitized filename from the URL
        filename = get_valid_filename(image_url)
        file_path = os.path.join("Fetched_Images", filename)

        # Check for duplicate filenames and append a number if necessary
        counter = 1
        original_file_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_file_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1

        # Open the file in binary write mode ('wb')
        with open(file_path, "wb") as f:
            # Write the content in chunks to the file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"\nSuccess! The image has been respectfully fetched and saved as:\n{file_path}")
        print("This resource is now organized for you and your community.")

    except requests.exceptions.HTTPError as err_http:
        print(f"\nRespectful Error: An HTTP error occurred. Status code: {err_http.response.status_code}")
        print("This can happen if the URL is invalid or the resource is no longer available.")
    except requests.exceptions.ConnectionError as err_conn:
        print(f"\nRespectful Error: A connection error occurred. Please check your internet connection.")
    except requests.exceptions.Timeout as err_timeout:
        print(f"\nRespectful Error: The request timed out. The server might be busy or unavailable.")
    except requests.exceptions.RequestException as err:
        print(f"\nRespectful Error: An unexpected error occurred: {err}")

# Run the download function when the script is executed
if __name__ == "__main__":
    download_image()
