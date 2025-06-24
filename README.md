# 🗓️ Automatic Timetable Generator

This project is a simple and functional **Timetable Generator** designed for a **single classroom** using **Graph Coloring Algorithm** and **Constraint Satisfaction** techniques.

It allows users to:
- Add faculties and subjects
- Select available faculties and their number of classes
- Define working days and slot timings
- Automatically generate a timetable avoiding conflicts

---

## 🚀 Tech Stack

### 🌐 Frontend
- **HTML & CSS** – Used for creating the user interface (add faculty, generate timetable, etc.)
- *(No JavaScript used)*

### 🐍 Backend
- **Python** (with **Flask** framework) – Handles routing, form submission, and algorithm logic

### 🧠 Algorithm
- **Graph Coloring Algorithm**
- **Constraint Satisfaction Problem (CSP)** rules to avoid clashes and maintain limits

### 🗃️ Database
- **SQLite** (`timetable.db`)
  - Stores subjects and assigned faculty
  - Can be extended to save generated timetables

### 📦 Python Libraries
- `sqlite3` – Database connection
- *(Optional)* `json` or `pandas` – For future exporting or formatting

---

## 🏗️ Features

- Add subject and faculty combinations
- Choose:
  - Faculty list and their class count
  - Working days (5-day or 6-day week)
  - Time slot range and number of slots per day
- Automatically generates a valid, clash-free timetable

---

## 📸 Sample Screenshots *(Optional)*

![image](https://github.com/user-attachments/assets/41e19fe2-a461-44e0-a978-9e48788c0d47)


## 🛠️ How to Run

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/timetable-generator.git
   cd timetable-generator
2. Install dependencies (Flask)
   pip install flask
3. Run the Flask app
   python app.py
4. Open your browser and go to http://localhost:5000   
   
   
