<h1 align="center">
    CareerConnect
</h1>

<h3 align=center style="font-weight: 1000;">
    Empowering seamless transition from school to work
</h3>


![Last Commit](https://img.shields.io/github/last-commit/KiseraTimon/ICS-Project-1)
![Jinja](https://img.shields.io/badge/jinja-Templates-yellowgreen)
![Languages](https://img.shields.io/github/languages/count/KiseraTimon/ICS-Project-1)

---

<h3 align=center style="font-weight: 1000">
🚀 Built with the tools and technologies
</h3>

<h1 align=center>

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python)
![Flask](https://img.shields.io/badge/-Flask-black?logo=flask)
![HTML](https://img.shields.io/badge/-HTML5-E34F26?logo=html5)
![CSS](https://img.shields.io/badge/-CSS3-1572B6?logo=css3)
![JavaScript](https://img.shields.io/badge/-JavaScript-yellow?logo=javascript)
![XML](https://img.shields.io/badge/-XML-0060aa?logo=xml)
![Jinja](https://img.shields.io/badge/-Jinja2-brown?logo=jinja)
![MySQL](https://img.shields.io/badge/-MySQL-grey?logo=mysql)
</h1>

---

## 📚 Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Future Possible Enhancements](#future-possible-enhancements)
- [Acknowledgements](#acknowledgements)
- [Assets](#assets)
- [License](#license)
- [Notes](#notes)

---

## Introduction

CareerConnect is a web-based, job market platform targeting students and businesses make the most of their knowledge and skills, and their hiring processes effectively.

This application features:

- A user-friendly interface for students and businesses to interact

- A robust backend powered by Flask

- A responsive design that works across various devices

- A secure authentication system for user accounts

- A job, internship, collab and short-contract listings service students and businesses

- Dashboards for all users to manage their profiles and actions through the application

- A search functionality for to quickly access job listings and profiles

- A messaging system for students and businesses to communicate

- A notification system for students and businesses to stay updated on job postings and applications

- A feedback system for students and businesses to rate and review each

---

## Prerequisites

- Python Version 3.13.2

- MySQL Packages

- Visual Studio Code (Or any IDE suitable for web application programming)

---

## Getting Started

1. Cloning Repository

    In a directory of your choice, clone this repository using the commands below

    ```bash
    git clone https://github.com/BritahKami/ICS-Project-1.git
    ```

2. Project setup:

    With the project cloned into your directory, the following steps will ensure you have a stable and running application

    - *Virtual Environment*

    First, create a virtual environment within the cloned project. If you are prompted to change the environment, click yes

    ```bash
    python -m venv .venv
    ```

    Next, activate the environment. You should see the name of your environment enclosed in parenthesis after this step

    ```bash
    .venv/scripts/activate
    ```

    - *Installing dependencies*

    With the virtual environment running, you can now install the dependencies used in this project

    ```bash
    pip install -r dependencies.txt
    ```

3. Configuring app files

    The application is still not ready to run, and a few changes MUST be made to the code. The following guidelines will conduct you through the necessary steps to both preview and run the app.

    - *Secret Key*

    By default, this particular app expects a `env.py` file.

    To setup your secret key manually, reference the [**assets**](#assets) section of this document, and locate the `env_example.py` file.

    Copy the contents of the file into a new `env.py` file within `website/config/env.py`

    - *Database Configuration*

    A MySQL database is used to store user data and newsletter information.

    This application expects a `connector.py` file that handles database connection.

    First, however, create a new MySQL database using the schema provided in the [**assets**](#assets) section.

    A MySQL database file `connector.py` is provided in the `website/database/` directory.
    It is dependent on the `env.py` file for configuration, so ensure you have created the `env.py` file as described above.
    You can then either populate the `env.py` file with your database credentials, or copy do that directly into the `connector.py` file as below.

    ```t
    host = ''           #Typically 'localhost'
    user = ''           # Typically 'root'
    password = ''       # Your MySQL password
    database = ''       # Your created database's name
    ```

4. Starting Server

    With the app configuration process complete, you can now run the develoment server using the commands below in your root app directory

    ```bash
    python main.py
    ```

---

## Project Structure

By the end of the setup, your project directories should look like this:

```t
├──.venv/
├──/logs/
├── website/                        # Flask Blueprint views & logic
│   ├── assets                      # Backend Logic & Page Routing
│   ├── config                      # Configuration & Constants File
│   │   ├── __init__.py
│   │   ├── env_example.py
│   │   └── env.py
│   ├── database                    # Database Setup Files
│   │   ├── __init__.py
│   │   ├── connector.py
│   │   └── icsdb.sql
│   ├── static                      # UI Assets
│   │   ├── css
│   │   ├── fonts
│   │   ├── images
│   │   └── js
│   ├── templates                   # UI Pages
│   │   ├── about
│   │   ├── auth
│   │   ├── contact
│   │   ├── dashboard
│   │   ├── other
│   │   ├── block.html
│   │   └── template.html
│   ├── __init__.py                 # App Initialization File
├── .gitignore                      # Git Commit Exclusions
├── dependencies.txt                # List of Dependencies
├── README.md                       # Documentation
└── utils.py                        # Custom Logging Helper
```

---

## Usage

1. User Accounts

    A user account is required to navigate access-controlled pages, like the dashboard.

    With the application running, use the sign up button to navigate to the registration page, where you can create a new account.

    The account will reflect on your MySQL Workbench. With the command below, you can access the list of all users in the system

    ```bash
    SELECT * FROM [dbname].users;   # Replace [dbname] with your database name
    ```

    Role access depends on the signup form you used to create an account

2. API Configuration

    Coming Soon

3. Dashboard

    Coming Soon

## Future Possible Enhancements

---

## Acknowledgements


## Assets

<details>
<summary><strong>env_example.py</strong></summary>

```bash
# Application Settings
FLASK_ENV=''
SECRET_KEY=''

# Database Settings
DB_HOST=''
DB_USER=''
DB_PASS=''
DB_NAME=''
```

</details>

<details>
<summary><strong>eenovators.sql</strong></summary>

```bash
# Coming Soon
```

</details>

---

## License

---

## Notes

School-to-work transition has been a very rough step for many students in Kenya, with even highly valued skill sets failing to attract quality work opportunities across all industries.
Businesses also struggle to make the most of their hiring windows, either due to poor communication about job vacancies, or due to inefficient talent pooling practices.

The research coming into this work highly acknowledges that something has been done to address this concerns. Today, there are several job markets accessible online that help to spread information about vacancies and ready talent, which assist in easing the school-to-work transition crisis to different degrees. But, it has also been observed that almost all fail to apply a student-focused approach. Instead, such spaces are oversaturated with cultured professionals, making recognition for students and graduates negligible

CareerConnect takes a student-first approach, aiming to provide a better pathway for every young individual to achieve a sense of tangible workforce experience through high quality jobs, internships and collaborations listings as well as a short-contract structure to self-market skills

The contents of this repository, with this guide provide deeper access to the design and logical patterns represented in code that bring CareerConnect to life
