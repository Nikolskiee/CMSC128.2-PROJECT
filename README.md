# CMSC128.2-PROJECT

# Setting Up Virtual Environment
## On Windows Powershell
Turn off Execution Policy Temporarily  
`Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process`

Create a Virtual Environment  
`py -m venv env`

Activate the Virtual Environment  
`env\Scripts\Activate.ps1`

Deactivate the Virtual Envirtonment  
`deactivate`

# Install Django
`pip install django`

# Go inside the PROJECT
`cd seirvice`

# Dependencies
Dependencies are installed using `pip`  
## To add dependencies on **requirements.txt**  
`pip freeze > requirements.txt`  
## To install dependencies using **requirements.txt**
`pip install -r requirements.txt`  

# Database
The database will be on Postgresql  
## To install Postgresql On Windows Subsystems for Linux 
`sudo apt install postgresql`  
## To start postgresql 
`sudo service postgresql start`    
`sudo -i -u postgres`  
## To create a Database
`psql`  

CREATE DATABASE seirvice_db;  
CREATE ROLE seirvice_user WITH LOGIN PASSWORD 'password';  
GRANT ALL PRIVILEGES ON DATABASE seirvice_db TO seirvice_user;  

\c seirvice_db  
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  
quit  
\q  

## To deploy database to localhost
psql -h localhost -p 5432 -U seirvice_user -W -d seirvice_db  

## Making Migrations
`py manage.py makemigrations`  
`py manage.py migrate`  

# To deploy the PROJECT locally
`py manage.py runserver`  


