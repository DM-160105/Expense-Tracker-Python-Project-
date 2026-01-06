# Expense Tracker

> A comprehensive, dual-interface (Web & CLI) application for tracking personal expenses, visualizing spending habits, and managing financial data efficiently.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![Flask](https://img.shields.io/badge/Flask-Web%20App-green.svg) ![MySQL](https://img.shields.io/badge/MySQL-Supported-orange.svg)

## 📖 Overview

**Expense Tracker** is a robust Python solution designed to help users track their daily spending effortlessly. Whether you are a fan of the command line's speed or prefer a visual web dashboard, this application serves both needs with a unified backend.

It is designed with flexibility in mind, allowing you to start immediately with **CSV storage** or scale up to a **MySQL database** for long-term usage.

## ✨ Features

- **Dual User Interfaces**:
  - **Web Dashboard (Flask)**: A modern, browser-based interface offering visual charts, easy forms, and summary views.
  - **CLI (Command Line Interface)**: A fast, menu-driven terminal interface for power users.
- **Flexible Data Storage**:
  - **CSV Mode**: The default "zero-config" mode. Data is stored in local CSV files.
  - **MySQL Mode**: Optional persistent storage using a relational database.
- **Insightful Analytics**:
  - **Visualizations**: Auto-generated bar and pie charts showing spending distribution.
  - **Summaries**: View total spending, average daily costs, and category breakdowns.
- **Advanced Filtering**: Filter your expense history by custom date ranges or categories.
- **CRUD Functionality**: Full support to Add, Read, Update, and Delete expenses.

## 🛠️ Technologies Used

| Category            | Technology     | Purpose                                    |
| :------------------ | :------------- | :----------------------------------------- |
| **Core Language**   | **Python 3**   | Application logic and backend processing   |
| **Web Framework**   | **Flask**      | Server-side web handling and routing       |
| **Template Engine** | **Jinja2**     | Rendering dynamic HTML pages               |
| **Database**        | **MySQL**      | (Optional) Relational data storage         |
| **File Storage**    | **CSV**        | (Default) Lightweight data persistence     |
| **Data Analysis**   | **Pandas**     | Data aggregation and statistical analysis  |
| **Visualization**   | **Matplotlib** | Generating trend lines and category charts |
| **CLI Formatting**  | **Tabulate**   | Displaying pretty tables in the terminal   |
| **Styling**         | **CSS3**       | Custom styling for the web interface       |

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher installed.
- (Optional) MySQL Server (if you plan to use database mode).

### Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/your-username/expense-tracker.git
    cd expense-tracker
    ```

2.  **Create a virtual environment** (Recommended)

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

The application is launched via the `main.py` entry point.

### Web Interface

To start the web server and view the dashboard in your browser:

```bash
python -m expense_tracker.main --mode web
```

> Open your browser and navigate to `http://127.0.0.1:5000`

### Command Line Interface

To use the terminal-based interactive menu:

```bash
python -m expense_tracker.main --mode cli
```

## ⚙️ Configuration

Configuration is managed via `config.py` and environment variables.

| Environment Variable      | Default           | Description                            |
| :------------------------ | :---------------- | :------------------------------------- |
| `EXPENSE_TRACKER_STORAGE` | `csv`             | Backend storage mode: `csv` or `mysql` |
| `FLASK_SECRET_KEY`        | `...`             | Secret key for Flask sessions          |
| `MYSQL_HOST`              | `localhost`       | Database host address                  |
| `MYSQL_USER`              | `root`            | Database username                      |
| `MYSQL_PASSWORD`          | [None]            | Database password                      |
| `MYSQL_DATABASE`          | `expense_tracker` | Database name                          |

To switch to MySQL, ensure you have created the database first:

```sql
CREATE DATABASE expense_tracker;
```

## 📂 Project Structure

```text
expense_tracker/
├── data/                # Local storage for CSV files
├── db/                  # Database logic (Storage adapters)
├── models/              # Data classes (Expense entity)
├── utils/               # Analytics and chart generation tools
├── web/                 # Flask web application
│   ├── static/          # CSS, JS, and generated Charts
│   └── templates/       # HTML Templates
├── config.py            # Global application settings
└── main.py              # Application entry point
```

## 📄 License

This project is open-source and available under the terms of the MIT License.
