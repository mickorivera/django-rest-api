# ReST API for a User Account

FEATURES:
* User account registration
* User account activation
* User login
* User password reset


INSTALLATION
1. Setup python3 and pip
2. Create a virtual environment
    `python -m venv spectrumone_env`
3. Activate virtual environment
    `source spectrumone_env/bin/activate`
4. Install required python libraries
    `pip install -r requirements.txt`
5. Define environment variables for email sending
	`EMAIL_HOST - smtp server`
	`EMAIL_HOST_USER - smtp account username/email`
	`EMAIL_HOST_PASSWORD - smtp account password`
	`EMAIL_HOST_PORT - smtp server port`
6. Perform migration of schema
    `python manage.py migrate`
7. Run server locally
    `python manage.py runserver`