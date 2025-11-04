# 🏥 MediConnect – Medical Services Prototype

A full-stack **Flask web application** that connects patients with medical service providers.  
Users can **register, log in, book services, and track their request status**, while admins can **view, accept, and complete service requests,**  all through a clean, responsive interface.

---

## 🚀 Features

### 👤 User Panel
- **Register / Login** using email & password.
- **Book a medical service** (doctor visit, medical transport, check-up).
- **Track service request status** in real-time.
- **View all bookings** in a clean dashboard.

### 🩺 Admin Panel
- **Secure Admin Login** for service providers.
- **View all incoming service requests.**
- **Accept or mark a request as completed.**
- **Track user bookings and manage updates.**

### 🎨 UI / UX Highlights
- Clean, modern **responsive design**.
- **Background image overlay** with subtle blur for elegance.
- Dynamic navigation bar (changes based on user/admin role).
- Flash message system for actions (login success, request booked, etc.).
- Organized **templates** and **static assets**.

---

## 🧠 Tech Stack

| Category | Technologies Used |
|-----------|-------------------|
| **Frontend** | HTML5, CSS3, Jinja2 Templates |
| **Backend** | Python, Flask |
| **Database** | SQLite (SQLAlchemy) |
| **Styling** | Custom CSS |
| **Authentication** | Flask session management |
| **Tools** | Virtual Environment, Flask Shell for DB setup |

---

## 🧩 Folder Structure

```bash
mediconnect/

│
├── app.py (Main Flask app entry point)

├── database.py (Database models & init logic)

├── static/

│ ├── style.css (App styling)

│ └── backgroundg.jpg (Background image)

├── templates/

│ ├── base.html (Common layout for all pages)

│ ├── dashboard.html (User dashboard)

│ ├── book_service.html (Booking form page)

│ ├── track_status.html (Track service status)

│ ├── admin_login.html (Admin login page)

│ └── admin_dashboard.html (Admin control panel)

└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone this repository

```git clone https://github.com/AlenKJ01/Mediconnect.git`
cd mediconnect```

### 2️⃣ Create a virtual environment

```python -m venv venv```

### 3️⃣ Activate it

Windows:

```venv\Scripts\activate```

macOS/Linux:

```source venv/bin/activate```

### 4️⃣ Install dependencies

```pip install -r requirements.txt```

### 5️⃣ Initialize the database

Run the Flask shell:

```flask shell```

Then execute:

```from app import db, init_admin`
db.drop_all()
db.create_all()
init_admin()```

(This creates tables and a default admin account.)

Default admin credentials:

Email: alen@gmail.com

Password: alen001

### 6️⃣ Run the application
    
```flask run```

OR

```python app.py```


**Access at → http://127.0.0.1:5000**

🧱 Core Functionalities
| Function	       |         Description  |
|-----------|-------------------|
|Login / Register	       | Basic user authentication using Flask sessions.|
|Book Service	           | Stores service request data in the database.|
|Track Status	          |  Users can view live updates (Pending → Accepted → Completed).|
|Admin Control	           | Admin can view, accept, and complete user requests.|
|Dynamic Navigation	     |   Menu adapts based on user or admin role.|
|Background Styling	      |  Elegant full-page blurred background image.|
