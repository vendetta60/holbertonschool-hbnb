# HBnB - Part 3: Authentication and Database

▶  **Introduction**

In this part of the HBnB project it's to add protection to our app. Using JSON Web Token authentication and hashing passwords that are created. Also implement memory using MySQL engine that handles SQL to create the database and the tables to store data. This is key to have a protected application that can store and retrieve requests.

▶  **Table of Contents**

- [Overview](#overview)
- [Concepts](#concepts)
- [Example](#example)
- [Installation](#Installation)
- [Author](#author)

▶  **Overview**

In this project we added Bcrypt, to hash passwords, Flask-JWT-Extended for authentication, SQLAlchemy/MySQL to create the databases and SQLite for development.

▶  **Concepts**

- There was files added to the structure to prevent circulation, make the user repository and add a database, like this:


		hbnb/
		├── app/
		│   ├── __init__.py
		|	├── extensions.py
		├── database/
		|   ├── setup_database.sql
		|   ├── table_relation.sql
		|   ├── db_diagram.mmd
		|   ├── db_diagram.png
		│   ├── api/
		│   │   ├── __init__.py
		│   │   ├── v1/
		│   │       ├── __init__.py
		│   │       ├── users.py
		│   │       ├── places.py
		│   │       ├── reviews.py
		│   │       ├── amenities.py
		|	|		├── auth.py
		│   ├── models/
		│   │   ├── __init__.py
		│   │   ├── user.py
		│   │   ├── place.py
		│   │   ├── review.py
		│   │   ├── amenity.py
		|	|	├── baseclass.py
		│   ├── services/
		│   │   ├── __init__.py
		│   │   ├── facade.py
		│   ├── persistence/
		│       ├── __init__.py
		│       ├── repository.py
		|		├── user_repository.py
		├── run.py
		├── config.py
		├── requirements.txt
		├── README.md

- Adding JWT authentication to secure the API and manage user sessions.
- Implement adiministrator login and credential verification.
- Make the CRUD methods interact with the database and are validated.
- SQLAlchemy was used as the Object Relational Mapper to prepare for MySQL queries.
- Maped relationships between User, Place, Amenity and Review in a Mermaid diagram in /database/db_diagram.mmd


▶   **Example**

	class HBnBFacade:
	    def __init__(self):
	       self.user_repo = SQLAlchemyRepository(User)
		   self.place_repo = SQLAlchemyRepository(Place)

                     ...

	    def create_user(self, user_data)
		user = User(**user_data)
		self.user_repo.add(user)
		return user

- To create the databases type in your terminal:

		$ flask shell

		 >> from app import db

		 >> db.create_all()


▶   **Installation**

Clone this in your terminal:

	git clone https://github.com/kamisos3/holbertonschool-hbnb/tree/main/part3

Then install from requirements.txt pytest, flask and flask-restx:

	pip install -r requirements.txt

Now you'll be able to run and test HBnB testpoints, you can use one of these commands:

	python run.py
	python3 run.py

▶   **Author**

Kami Sostre [https://github.com/kamisos3]
