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


