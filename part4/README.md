# HBnB - Part 4

▶ **Introduction**  

This project is a web-based clone of the AirBnB platform, built as part of the Holberton School curriculum. It uses HTML, CSS, and vanilla JavaScript for the frontend, and a Flask backend with a SQLite database for data persistence. The project demonstrates full-stack web development, including user authentication, dynamic content rendering, and RESTful API integration. You can also see that Python fundamentals to create functions have been applied throught the whole project.

▶ **Table of Contents**

- [Overview](#overview)
- [Concepts](#concepts)
- [Example](#example)
- [Installation](#installation)
- [Author](#author)



▶ **Overview**  

HBnB is a web application that allows users to browser, search, and review places to stay. The frontend is built with HTML, CSS, and JavaScript, providing a responsive and interactive user experience. The backend is powered by Flask and SQLAlchemy, exposing RESTful APIs for user authentication, place management, and reviews. The project is designed for educational purposes, focusing on the integration of frontend and backend technologies.



▶ **Concepts**

- Full-stack web development
- RESTful API design and consumption
- User authentication with JWT
- Dynamic DOM manipulation with JavaScript
- Responsive design with CSS
- Database management with SQLite and SQLAlchemy


▶ **Example**

1. **Login:**  
   Users can log in with their credentials. The frontend sends a POST request to the backend API, which returns a JWT token for authenticated sessions.

2. **Browse Places:**  
   The homepage displays a list of available places, dynamically fetched from the backend API and rendered using JavaScript.

3. **Add Review:**  
   Logged-in users can add reviews to places. Reviews are sent to the backend and displayed in real time.



▶ **Installation**

Clone this repository in your terminal:

```bash
git clone https://github.com/kamisos3/holbertonschool-hbnb/tree/main
cd holbertonschool-hbnb/part4
```

Set up the Python virtual environment and install dependencies:

```bash
cd front-end
pip install -r requirements.txt
```

Start the frontend server:

```bash
python3 -m http.server 5000
```


▶ **Author**

Kami Sostre [https://github.com/kamisos3]


