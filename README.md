# DB_Design_Prj
## Run Frontend

In the frontend directory, you can run:

### npm install
Installs the node modules for the app

### npm start
Runs the app in the development mode.

Open http://localhost:3000 to view it in your browser.
The page will reload when you make changes.
You may also see any lint errors in the console.

## Run Backend 
In file server.py, in the following code snippet, add your workbench userid, password

`
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="",
  database = "HMS_prj",
  connection_timeout = 500
)
`

In the backend directory, you can run:

### FLASK_APP=server.py flask run -h localhost -p 3001 


## Database 

Create a database named HMS_prj.

Execute DDL.sql on MySQL Workbench to create the tables.

Execute InsertDML.sql on MySQL Workbench to insert dummy test data in the dates
