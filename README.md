# notification_center
 notification center with the aim of conveying crucial information to users through system-generated messages. These messages could include updates on the delivery of purchased items, notifications about payment failures, and alerts about new followers, among others.

 
## Features:

### User Management:
User registration and login.
Secure authentication with JWT tokens.
Get Other user details to publish message to them

### Message Management:
Publish new message entries to one or more users.
Mark existing message entries as seen, deleted and archived.
Query message entries based on various criteria (e.g., limit, offset, keyword search on message_content) for the current user.

### Technology Stack:
FastAPI (backend framework)
Python (programming language)
PostgreSQL (database)
sqlalchemy (ORM)

### Installation and Usage
Create venv and install requrements.txt using below command:
```bash
python -m venv venv
pip install -r requirements
```
Once done create .env file with all the required environment variables based on config.py file.
After that create 2 database in postgres, I used following names notificaion_center (for main application) and notificaion_center_test (for test cases)

To run the Project use below command from the root dir:
```bash
uvicorn app.main:app --reload
```

To run test cases set PYTHONPATH env variable till root folder based on your project location, below is the example for windows OS.

```bash
set PYTHONPATH=set PYTHONPATH=C:\Users\kunal.behra\Documents\Projects\notification_center
````






