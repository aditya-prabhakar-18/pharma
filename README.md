
# Pharmacy Management System 💊
A GUI based Python + MySQL desktop application for managing pharmacy stock, billing, and inventory.  
Originally developed as a Computer Science project to implement Python-MySQL Connectivity.


## 🧩 Features
- Add, update, and delete medicine records  
- Search and filter stock by expiry or availability  
- Generate and print bills  
- Simple login system  
- GUI built using Tkinter for an intuitive interface  


## 🛠️ Tech Stack
| Component | Technology |
|------------|-------------|
| Programming Language | Python 3.9 |
| Database | MySQL 8.0 |
| GUI | Tkinter |
| Libraries Used | `mysql-connector-python`, `Pillow`, `PrettyTable` |


## ⚙️ Installation & Setup
1. **Clone this repository**

    git clone https://github.com/adityaprabhakar/pharmacy-management-system.git
   cd pharmacy-management-system


2. **Install dependencies**


   pip install -r requirements.txt

3. **Configure the database**
-- Select Database
mysql> USE pharmacy;
Database changed;

-- Show Tables
mysql> SHOW TABLES;
+--------------------+
| Tables_in_pharmacy |
+--------------------+
| stocks             |
| users              |
+--------------------+
2 rows in set (0.00 sec);
mysql> DESC users;
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| userID  | int          | NO   | PRI | NULL    | auto_increment |
| name    | varchar(50)  | YES  |     | NULL    |                |
| username| varchar(20)  | YES  |     | NULL    |                |
| password| varchar(20)  | YES  |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+
4 rows in set (0.37 sec);
mysql> SELECT * FROM users;
+--------+------------------+----------+----------+
| userID | name             | username | password |
+--------+------------------+----------+----------+
| 1      | Admin            | root     | tiger    |
| 2      | Aditya Prabhakar | Adi      | tiger    |
+--------+------------------+----------+----------+
2 rows in set (0.10 sec);
mysql> DESC stocks;
+---------+--------------+------+-----+---------+-------+
| Field   | Type         | Null | Key | Default | Extra |
+---------+--------------+------+-----+---------+-------+
| med_id  | varchar(30)  | NO   | PRI | NULL    |       |
| med_name| varchar(200) | NO   |     | NULL    |       |
| amt     | int          | NO   |     | NULL    |       |
| expiry  | date         | NO   |     | NULL    |       |
| price   | float        | YES  |     | NULL    |       |
| lot_no  | int          | NO   |     | NULL    |       |
+---------+--------------+------+-----+---------+-------+


4. **Run the application**

   python ph.py

## 🧠 Learning Outcomes

* Integrated GUI and database using Python and MySQL
* Designed user authentication and CRUD operations
* Implemented stock and expiry management features
* Gained experience in data validation and event-driven programming


## 🧑‍💻 Author

**Aditya Prabhakar**


## 🙌 Acknowledgements

* Codemy.com Tkinter tutorials
* TutorialsPoint Python references
* StackOverflow community for debugging assistance

