### **Running the Verkada Report Generator Locally**

This guide provides step-by-step instructions to set up and run the Python script on your MacBook Pro, which now uses Verkada's new two-step authentication process.

#### **Step 1: Set up Your Python Environment**

It's a best practice to use a virtual environment to manage dependencies for each project.

Open your Mac's Terminal application and follow these commands:

1. **Create a Project Folder**:  
   mkdir verkada-report-app  
   cd verkada-report-app

2. **Create a Virtual Environment**:  
   python3 \-m venv venv

3. **Activate the Virtual Environment**:  
   source venv/bin/activate

   Your terminal prompt will now show (venv) to indicate the virtual environment is active.

#### **Step 2: Set up Your Files**

Save the updated Python script as report\_generator.py and create two new files in your project folder: a requirements.txt file for dependencies and a .env file for your API key.

1. **report\_generator.py**: (The updated code from the previous block)  
2. **requirements.txt**:  
   requests  
   python-dotenv

3. **Create a .env file**: This is where you'll securely store your permanent Verkada API Key.  
   * Create a new file named .env in the verkada-report-app folder.  
   * Add the following line to the file, replacing YOUR\_VERKADA\_API\_KEY\_HERE with your actual key.

VERKADA\_API\_KEY=YOUR\_VERKADA\_API\_KEY\_HERE  
**Note**: The .env file should be kept private and never committed to a public repository like Git.

#### **Step 3: Install Dependencies**

With your virtual environment active, use pip to install the required libraries.

pip install \-r requirements.txt

#### **Step 4: Run the Script**

You are now ready to generate the report. Run the script directly from your terminal.

python3 report\_generator.py

The script will first attempt to get a short-lived API token and then use that token to retrieve your device data. After it runs, you will find a new file named verkada\_report.csv in your verkada-report-app directory containing the information about all your devices.
