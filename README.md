
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

   * Ensure MySQL Server is running.
   * Create a database named `pharmacy`.
   * Update your MySQL credentials (username and password) inside `src/main.py` or `src/database_setup.py` if needed.

4. **Run the application**

   python src/main.py



## 🗂️ Project Structure


## 📸 Screenshots

|                  Login Page                 |                     Dashboard                     |               Billing Interface              |
| :-----------------------------------------: | :-----------------------------------------------: | :------------------------------------------: |
| ![Login](docs/screenshots/login_window.png) | ![Dashboard](docs/screenshots/main_interface.png) | ![Billing](docs/screenshots/bill_screen.png) |


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

