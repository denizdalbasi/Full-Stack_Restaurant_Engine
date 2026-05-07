# Menemen Web Simulator

A professional ***Flask-based web application*** that simulates a full restaurant lifecycle—from interactive menemen cooking and customer feedback to financial management and inventory control.

---

## ***Objectives***

- **Simulate the business & cooking process**
  - Recreate real cooking steps while managing the financial side of a restaurant.
- **Manage live inventory**
  - Track stock levels in real-time and prevent ***negative*** cooking when ingredients run out.
- **Enforce business logic**
  - Block purchases (restocking) if the budget is insufficient and log every transaction.
- **Create an interactive web experience**
  - Use a Flask-driven UI to guide the user through preparation, cooking, and management.
- **Store and group data**
  - Use a database to archive logs and group customer feedback by user for a clean overview.

---

## ***Tech Stack***

- **Python (Flask)**
- **SQLite3**
- **HTML/CSS (Jinja2)**

---

## ***Database tables include:***

* ***`ingredient_list`***: Current stock levels and units.
* ***`recipe_amounts`***: Essential amounts needed for the recipe.
* ***`mutfak_araclari`***: Status of kitchen tools and extras.
* ***`finances`***: Total revenue, costs, and profit tracking.
* ***`activity_logs`***: Timestamped history of sales and expenses.
* ***`feedback`***: Customer reviews and user-based answers.

---

### **Live Site:** [Visit Menemen Simulator](http://admin684584165418645.pythonanywhere.com/)

> **Admin Access:**
> - **Username:** `admin`
> - **Password:** `admin123`

---

## ***Workflow***

To view the interactive logic and user flow, visit our Miro board:

[![Workflow Preview](https://img.shields.io/badge/Miro-View%20Workflow-blue?style=for-the-badge&logo=miro)](https://miro.com/app/board/uXjVHXw9tN8=/)
