# DeeZee-Freight
very simple html/css/javascript/python website for DeeZee Shipping Operations
## Notes
If you plan on running this locally for development or otherwise, contact one of the developers already in the project for the .env file

You will need to spin up a local mysql db to develop on. Ionos will not allow you to connect from your device.
```
Please always establish the connection to your database via your website/presence. For security reasons, it is not possible to access the database directly, for example via your local computer (external ODBC connection).

To protect your data, your database is located on a dedicated database server that is protected by a firewall.
```
virtual environment: `python -m venv venv` from above this root

`source venv/bin/activate` to turn on venv

just set up any docker and throw mysql in it. (schema.sql)[schema.sql] has the database schema, get a db dump of whatever's up currently and make that fit the schema.

`npm i` from in root

`pip install -r requirements.txt`

local running with debugger: `flask --app deeezeefreight run --debug` run from directory above this readme

## File explainations / directory map
- auth --> specifically for the login to access the tables
- db --> creates the database connections and initializes the cursor by selecting the table before any command is run
- functions --> has the big ol' functions that are either used more than once or messy and I didn't want to interrupt the logic of the routes file
- routes --> has all the routing for the application and handles all of the submissions
- static folder --> everything that doesnt change on the site. styling, dropdown object, assets folder
- assets folder --> all images used including the favicon
- countryDropdown --> js specifically for the form dropdown country selector because the code was long
- styles --> all the css
- templates folder --> templates for the site components
- dbTables --> page of tables of what's in the db. For employee use only. if not necessary for operations, will be removed.
- employeeRegistration --> employee registration form
- index --> landing page
- layout --> base layout for the site. contains header, error message section, body background, and footer
- login --> internal employee login to access db tables
- unauthorized --> tell the user they are not authorized to log in and route them back to landing page
- vendorRegistration --> page one of vendor registration form
- vendorRegistrationTwo --> page two of vendor registration. Contains the "ship to" locations. could hypothetically be merged into the first page but it risks very long and hard-to-read code. plus two pages follows the format of the previous site
- app.py --> runs the flask app
- _init_s --> tell python that the folder is a module. init in root is what scaffolds the site
- .env (not in repo) --> all environment variables required to run the site. can only get this from a fellow dev
- .gitignore --> tells git not to put auto-generated files in the repo