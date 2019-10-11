# MySQL permissions management system

### KPI laboratory work

#### Setup
Activate your virtualenv and install dependencies:
```bash
pip install -r requirements.txt
```

#### Login
Login with already create user in MySQL:
```bash
python cli.py login username password
```
You can relogin with another use anytime.

#### Give required privileges to administrative user
This user need's to have all required grants, 
other ways you will have Permission Denied responses.
Commands to give all required privileges for user:
```mysql
CREATE USER 'username'@'localhost' IDENTIFIED BY 'username';
GRANT ALL PRIVILEGES on *.* to 'username'@'localhost';
GRANT GRANT OPTION on *.* to 'username'@'localhost';
```

#### Management commands
Now you can manage permission
```bash
python cli.py grant grant_action username target_type
python cli.py revoke grant_action username target_type
```
Where `grant_action` is any Static Privileges for GRANT and REVOKE
from MySQL documentation
(https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html)
 written using SnakeCase.

Use show-grants command to see changes:
```bash
(venv) sergiy@pc:~/KPI/lab2$ python cli.py show-grants test_user;
Show Grants for user: test_user
("GRANT ALL PRIVILEGES ON *.* TO 'test_user'@'localhost'",)
("GRANT INSERT (User) ON `mysql`.`user` TO 'test_user'@'localhost'",)
("GRANT ALL PRIVILEGES ON `db`.`test` TO 'test_user'@'localhost'",)
```

##### Four types of target_type
1) global - applied for all db tables and columns
1) db - applied for specific db
1) table - applied for specific db and table
1) cols - applied for specific db, table and columns

Examples:
```bash
python cli.py grant create test_user global # run's immediately
python cli.py grant alter test_user db # run's immediately
python cli.py grant drop test_user table # ask's you to provide target db and table
```
```bash
(venv) sergiy@pc:~/KPI/lab2$ python cli.py grant insert test_user cols
Input database name or '*': test_db
Input table name or '*': test_table
Input columns names with '|' delimiter: field_1|field_2|field_3 
Executing request grant INSERT to test_user
SQL query: GRANT INSERT (field_1,field_2,field_3) ON test_db.test_table TO 'test_user'@'localhost'
```
Executed the next SQL query:
```mysql
GRANT INSERT (field_1,field_2,field_3) ON test_db.test_table TO 'test_user'@'localhost'
```
