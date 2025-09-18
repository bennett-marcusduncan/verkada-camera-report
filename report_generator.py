import requests
import os
import csv
from io import StringIO
from dotenv import load_dotenv

def get_api_token(api_key):
    """
    Exchanges a top-level Verkada API key for a short-lived API token.
    Returns the token string if successful, otherwise returns None.
    """
    token_url = 'https://api.verkada.com/token'
    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }
    try:
        response = requests.post(token_url, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        return token_data.get('token')
    except requests.exceptions.RequestException as e:
        print(f"Failed to get API token: {e}")
        return None

def generate_verkada_report(api_token):
    """
    Retrieves a list of all Verkada devices using an API token,
    and returns the data as a CSV string.
    """
    headers = {
        'Accept': 'application/json',
        'x-verkada-auth': api_token
    }

    # The Verkada API endpoint to get camera data.
    api_url = 'https://api.verkada.com/cameras/v1/devices'

    all_cameras = []
    page_token = None
    
    # Handle pagination to retrieve all devices
    while True:
        try:
            params = {'page_size': 100} # Max page size is 100
            if page_token:
                params['page_token'] = page_token

            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'cameras' in data:
                all_cameras.extend(data['cameras'])

            page_token = data.get('next_page_token')
            if not page_token:
                break
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    # Define the fields for the CSV report
    fieldnames = [
        'name',
        'serial',
        'mac_address',
        'model',
        'site',
        'local_ip',
        'status',
        'last_online'
    ]

    # Use StringIO to create a CSV in memory
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()

    for camera in all_cameras:
        writer.writerow({
            'name': camera.get('name', 'N/A'),
            'serial': camera.get('serial', 'N/A'),
            'mac_address': camera.get('mac_address', 'N/A'),
            'model': camera.get('model', 'N/A'),
            'site': camera.get('site', 'N/A'),
            'local_ip': camera.get('local_ip', 'N/A'),
            'status': camera.get('firmware', 'N/A'),
            'last_online': camera.get('last_online', 'N/A')
        })
    
    return csv_buffer.getvalue()

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()
    
    api_key = os.getenv('VERKADA_API_KEY')
    if not api_key:
        print("Error: VERKADA_API_KEY not found in .env file or environment.")
    else:
        print("Attempting to retrieve API token...")
        api_token = get_api_token(api_key)
        
        if api_token:
            print("Successfully retrieved API token. Generating report...")
            report_csv = generate_verkada_report(api_token)
            
            if report_csv:
                # Create the 'reports' directory if it doesn't exist
                reports_dir = 'reports'
                if not os.path.exists(reports_dir):
                    os.makedirs(reports_dir)
                
                # Save the file inside the new 'reports' directory
                file_path = os.path.join(reports_dir, 'verkada_report.csv')
                with open(file_path, 'w', newline='') as file:
                    file.write(report_csv)
                print(f"Report successfully generated and saved to {file_path}")
            else:
                print("Failed to generate report.")
        else:
            print("Process aborted. Please check your API key and network connection.")
