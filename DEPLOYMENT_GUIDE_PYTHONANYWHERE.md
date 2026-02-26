# Deploying to PythonAnywhere (Free Tier + MySQL)

[Content verified and identical to the artifact version. This copy is placed in the project root for user convenience.]

## Prerequisites
- A GitHub account (recommended for easy code transfer)
- Your project code ready to go (which we have prepared)

## Step 1: Sign Up for PythonAnywhere
1.  Go to [www.pythonanywhere.com](https://www.pythonanywhere.com/).
2.  Click **Sign up** and create a **Beginner (Free)** account.
    *   *Note: The username you choose will be part of your website URL (e.g., `yourusername.pythonanywhere.com`).*

## Step 2: Upload Your Code
The easiest way is to use GitHub.

1.  **On GitHub**: Create a new repository and push your code to it.
2.  **On PythonAnywhere**:
    *   Go to the **Consoles** tab.
    *   Click **Bash** to open a terminal.
    *   Clone your repository:
        ```bash
        git clone https://github.com/yourusername/your-repo-name.git
        ```
    *   *Note: If you don't use GitHub, you can upload files manually zip them and upload via the **Files** tab.*

## Step 3: Set Up the Database (MySQL)

1.  Go to the **Databases** tab on PythonAnywhere.
2.  Under **Create a database**, set a password for your database (remember this!) and click **Initialize MySQL**.
3.  Once created, you will see your **Database host**, **Username**, and **Database name** (e.g., `yourusername$default`).

### Import the Schema
1.  Go back to the **Consoles** tab and open **Bash**.
2.  Navigate to your project folder:
    ```bash
    cd your-repo-name
    ```
3.  Import the schema file we evaluated (`full_schema.sql`) into your new database:
    ```bash
    mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com -p 'yourusername$default' < full_schema.sql
    ```
    *   *Replace `yourusername` and `yourusername.mysql.pythonanywhere-services.com` with the details from your Databases tab.*
    *   *Enter your database password when prompted.*

## Step 4: Configure the Web App

1.  Go to the **Web** tab.
2.  Click **Add a new web app**.
3.  Click **Next**, then select **Flask**, then select **Python 3.10** (or the version matching your local env).
4.  **Path**: It will ask for the path to your flask app. You can leave the default for now, we will change it.

### Configure Environment Variables (via WSGI file)
In the **Web** tab, scroll down to the **Code** section and find the **WSGI configuration file** link.

1.  Click the link to edit the WSGI file.
2.  Delete the default content and paste this (adjusting the path to your project):

    ```python
    import sys
    import os

    # Add your project directory to the sys.path
    project_home = '/home/yourusername/your-repo-name'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    # Set Environment Variables
    os.environ['SECRET_KEY'] = 'your-secret-key-here'
    os.environ['DB_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
    os.environ['DB_USER'] = 'yourusername'
    os.environ['DB_PASSWORD'] = 'your-database-password'
    os.environ['DB_NAME'] = 'yourusername$default'
    os.environ['FLASK_ENV'] = 'production'

    # Import flask app but need to call it "application" for WSGI to work
    from app import app as application
    ```
    *   *Make sure to replace the placeholder values with your actual database details and paths!*
    
### Alternative: Using .env on Server
If you uploaded your `.env` file (be careful not to commit secrets to public GitHub), you can load it in the WSGI file:

```python
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/your-repo-name')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
```

## Step 5: Install Dependencies (Virtual Environment)
1.  Go to the **Consoles** tab -> **Bash**.
2.  Create a virtual environment:
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 my-virtualenv
    ```
3.  Install your dependencies:
    ```bash
    workon my-virtualenv
    cd your-repo-name
    pip install -r requirements.txt
    pip install python-dotenv mysql-connector-python bcrypt
    ```

## Step 6: Finalize Web App Config
1.  Go back to the **Web** tab.
2.  Under **Virtualenv**, enter the path to your virtual environment: `/home/yourusername/.virtualenvs/my-virtualenv` (it might auto-complete).
3.  Scroll to the top and click the green **Reload** button.

## Step 7: Verify
Visit your website URL (`https://yourusername.pythonanywhere.com`). It should be live!

### Troubleshooting
- If you see "Something went wrong", check the **Error log** link in the **Web** tab.
- Common issues:
    - Wrong database password in WSGI file.
    - Missing `pip install` packages.
    - Incorrect path in WSGI file.
