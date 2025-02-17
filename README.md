RoadWatch Project Setup Guide
This guide provides step-by-step instructions to set up the RoadWatch project on your local machine. The project uses Django and MySQL to manage the data and serve the web application.

Prerequisites
Before starting the setup, ensure you have the following tools installed:

Python Install Python 3.8 or above from Python.org. Ensure pip is included during installation for package management.
MySQL Install MySQL Community Server from MySQL Downloads. Install MySQL Workbench (optional, but helpful for managing databases via a GUI).
Visual Studio Code (VSCode) Install Visual Studio Code from VSCode Downloads (optional, but useful for development).
Virtualenv (Optional, but recommended) Install the virtual environment tool:

pip install virtualenv
Steps to Set Up the Project
1. Download the Project
Download the project as a ZIP file from your source and extract it to a folder of your choice on your local machine.

2. Set Up a Virtual Environment
Navigate to the project directory where the project files were extracted and open new terminal:


cd myproject
Create a virtual environment in the root project folder:

=
python -m venv .venv
Activate the virtual environment:

On Windows :

.venv\Scripts\activate
On macOS/Linux :
bash
Copy code
source .venv/bin/activate
3. Install Required Dependencies
With the virtual environment activated, install the project dependencies from requirements.txt:

bash
Copy code
pip install -r requirements.txt
This will install all the necessary packages, including Django and other Python libraries used in the project.

4. Set Up the MySQL Database
Step 1: Ensure MySQL is Installed and Accessible
If you get the error 'mysql' is not recognized as an internal or external command , follow these steps:

Windows : You need to add MySQL to your environment variables so that the mysql command can be recognized globally.
Open Control Panel > System > Advanced system settings .
Click on Environment Variables .
Under System Variables , find the Path variable and click Edit .
Add the path to your MySQL bin directory (usually something like C:\Program Files\MySQL\MySQL Server 8.0\bin).
Click OK to save the changes, then restart your terminal (Command Prompt or PowerShell).
Step 2: Create the Database
Navigate to the folder containing the roadwatch_database.sql file. You can use File Explorer to go to the folder, and then in the address bar, type cmd and press Enter to open a Command Prompt window at that location.

In the Command Prompt (ensure MySQL is installed and accessible), log in to MySQL:

mysql -u root -p
Enter your MySQL root password when prompted.

Create a new database named roadwatch:

sql
Copy code
CREATE DATABASE roadwatch;
Exit MySQL:


exit;
Step 3: Import the Database
Now, you need to import the provided SQL file (roadwatch_database.sql) into the roadwatch database.

On Windows :
Open Command Prompt in the folder where the .sql file is located.
Run the following command:

mysql -u root -p roadwatch < roadwatch_database.sql
If you haven't added MySQL to your environment variables, navigate to the folder where MySQL is installed (e.g., C:\Program Files\MySQL\MySQL Server 8.0\bin), then run the above command with the full path to the mysql executable.

Using MySQL Workbench (optional):
Open MySQL Workbench.
Connect to your MySQL server and select the roadwatch database.
Use File > Run SQL Script to select and run the roadwatch_database.sql file.
5. Configure Django Settings
Open the project in your text editor (e.g., VSCode).
Navigate to the myproject/settings.py file.
In the DATABASES section, configure the MySQL database details:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roadwatch',  # Name of the database
        'USER': '',  # MySQL username ex. 'root'
        'PASSWORD': '',  # MySQL password ex. 'root'
        'HOST': 'localhost',  # Database host (localhost if running on the same machine)
        'PORT': '3306',  # Default MySQL port
    }
}
Save the changes to settings.py.
6. Run Database Migrations
Run the following Django commands to apply migrations and set up the database schema:

python manage.py makemigrations
python manage.py migrate
7. Create a Superuser
To access the Django admin panel, create a superuser:


python manage.py createsuperuser
Follow the prompts to set a username, email, and password.

8. Start the Development Server
Run the Django development server:


python manage.py runserver
The application will be available at http://127.0.0.1:8000.

9. Access the Admin Panel
To access the Django Admin Panel, go to http://127.0.0.1:8000/admin and log in using the superuser credentials created earlier.

Project Structure
The project has the following directory structure:

myproject/ ├── .venv/ # Virtual environment folder │ ├── Include/ │ ├── Lib/ │ └── Scripts/ ├── .vscode/ # VSCode settings ├── myapp/ # Django app containing core functionality │ ├── media/ # Media folder for uploaded files │ ├── migrations/ # Database migrations │ ├── static/ # Static files (CSS, JS, Images, etc.) │ ├── templates/ # HTML templates │ └── src/ # Source code ├── myproject/ # Main project configuration files ├── manage.py # Django project manager file ├── requirements.txt # List of Python dependencies └── roadwatch_database.sql # SQL file for importing the database
