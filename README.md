# AetherChain: AI-Powered Supply Chain Intelligence Platform 🔗

A full-stack data application designed to provide intelligent insights into a global supply chain. This project integrates a robust backend API, multiple databases, and an interactive analytics dashboard to solve common logistical challenges.

![Streamlit Dashboard Screenshot](https://raw.githubusercontent.com/your-username/your-repo/main/path/to/screenshot.png) ## 🎯 Problem Solved

Traditional supply chain management often suffers from a lack of real-time visibility and siloed data. This leads to:
* **Reactive Inventory Management:** Ordering new stock only after a shortage occurs, leading to delays.
* **Poor Visibility:** Difficulty understanding complex supplier-product relationships across a global network.
* **Inefficient Operations:** Inability to quickly identify operational bottlenecks, like which warehouses are nearing capacity.

AetherChain addresses these problems by providing a centralized, data-driven platform for monitoring, analysis, and proactive decision-making.

## ✨ Key Features

This project is a complete ecosystem, demonstrating skills across the entire data lifecycle.

#### 🐍 Backend (FastAPI)
* **RESTful API:** A robust API built with FastAPI to manage suppliers, products, warehouses, and inventory.
* **Multi-Database Architecture:**
    * **PostgreSQL:** Used for structured, transactional data (products, inventory, etc.).
    * **Neo4j Graph Database:** Models the complex relationships between suppliers and products, allowing for powerful path-finding queries.
* **Intelligent Endpoints:**
    * **Low Stock Alert System:** An endpoint that performs a complex SQL query to identify all products whose total stock is below their pre-defined reorder level.
    * **Graph-Powered Queries:** An endpoint that queries the Neo4j database to trace a product's supply path back to its supplier and country of origin.

#### 📊 Frontend (Streamlit)
* **Multi-Page Interactive Dashboard:** A clean, professional user interface with separate pages for different analyses.
* **Real-time Alerts:** The homepage prominently displays a "Low Stock Alerts" table, providing immediate, actionable insights.
* **Advanced Visualizations:** Utilizes Plotly to create animated, interactive charts:
    * Warehouse utilization (capacity vs. stock).
    * Top N most stocked products.
    * Inventory value distribution treemap.
* **Supply Chain Graph Explorer:** An interactive tool to select any product and visually trace its supply path using the Neo4j backend.

#### 🐳 Data & Architecture
* **Fully Containerized:** The entire application stack (PostgreSQL, Neo4j, Backend API, Dashboard) is managed by Docker and Docker Compose for easy setup and deployment.
* **Data Generation Script:** Includes a powerful Python script using `Faker` to populate the databases with thousands of realistic data points, enabling meaningful analysis from the start.

## 🛠️ Technology Stack

* **Backend:** Python, FastAPI, SQLAlchemy, Neo4j Driver
* **Frontend:** Streamlit, Pandas, Plotly Express
* **Databases:** PostgreSQL (Relational), Neo4j (Graph)
* **DevOps:** Docker, Docker Compose

## 🏗️ System Architecture



The system is composed of four main containerized services that communicate internally. The user interacts only with the Streamlit dashboard, which in turn gets all its data from the FastAPI backend.

1.  **FastAPI Backend (`backend_api`):** The central "brain" of the application.
2.  **Streamlit Frontend (`dashboard_app`):** The user interface and visualization layer.
3.  **PostgreSQL Database (`postgres_db`):** The primary data store.
4.  **Neo4j Database (`neo4j_db`):** The graph data store for relationship analysis.

## 🚀 How to Run

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* [Python 3.9+](https://www.python.org/downloads/) installed.

### Step 1: Clone the Repository
Clone this project to your local machine.
```bash
git clone [https://github.com/your-username/AetherChain_V2.git](https://github.com/your-username/AetherChain_V2.git)
cd AetherChain_V2
```

### Step 2: Start the Application (Terminal 1)
In your first terminal, from the project's root directory, run the following command. This will build the Docker images and start all four services.
```bash
docker-compose up --build
```
Leave this terminal open. It will stream the logs from all the running services.

### Step 3: Generate the Data (Terminal 2)
The application starts with an empty database. You need to run the data generation script to populate it.

1.  Open a **second, new terminal**.
2.  Navigate to the `backend` directory:
    ```bash
    cd path/to/your/project/backend
    ```
3.  Create and activate a Python virtual environment:
    ```bash
    # Create venv
    python -m venv venv
    # Activate venv (Windows)
    .\venv\Scripts\activate
    # Activate venv (macOS/Linux)
    # source venv/bin/activate
    ```
4.  Install the required packages for the script:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the generation script:
    ```bash
    python ../scripts/generate_data.py
    ```
    This will take a few minutes to create all the suppliers, products, and inventory.

### Step 4: Explore the Application
Once the script is finished, you can access the running application:

* **View the Dashboard:** ➡️ **[http://localhost:8501](http://localhost:8501)**
* **Explore the API Docs:** ➡️ **[http://localhost:8000/docs](http://localhost:8000/docs)**
* **Query the Graph DB:** ➡️ **[http://localhost:7474](http://localhost:7474)** (Login: `neo4j` / `aetherpass`)
