# DevopsFullStackWebsite
![Auto Assign](https://github.com/african-devopsfullstack/demo-repository/actions/workflows/auto-assign.yml/badge.svg)

![Proof HTML](https://github.com/african-devopsfullstack/demo-repository/actions/workflows/proof-html.yml/badge.svg)

[![Quality Gate Status](http://216.80.104.71:9005/api/project_badges/measure?project=devopsfullstack-website&metric=alert_status&token=sqp_46199592cc52aeb6956da312ba5e9ee485975466)](http://216.80.104.71:9005/dashboard?id=devopsfullstack-website)
This guide will walk you through the process of setting up and running a Flask web application, including creating a .env file for configuring database connections.
Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system:

    Python 3.x
    pip (Python package manager)

Step 1: Clone the Repository

First, clone the Flask application repository to your local machine using the following command:

    git clone <repository-url>
    cd <repository-directory>

Step 2: Create a Virtual Environment (Optional but recommended)

It's a good practice to create a virtual environment for your Flask application to isolate its dependencies. To create a virtual environment, use the following commands:



    python -m venv venv

Activate the virtual environment:

On Windows:


    venv\Scripts\activate

On macOS and Linux:

    source venv/bin/activate

Step 3: Install Dependencies

Install the required Python packages using pip:


    pip install -r requirements.txt

Step 4: Create a .env File

To configure your Flask application's database connection, you'll need to create a .env file in the root directory of your project. This file should contain sensitive information like database credentials and should never be committed to version control. Below is an example .env file structure:

# .env
```
# Database configuration
DB_HOST=
DB_PORT=3306
DB_NAME=
DB_USER=
DB_PASSWORD=
```
Request the database connection details

Step 5: Run the Application
you can run the application using the following command:

    python app.py

or

    flask run

