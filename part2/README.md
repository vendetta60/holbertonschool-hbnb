# HBnB - Part 2: Implementing BL and API

▶  **Introduction**

This is the second part of the HBnB project, here we will tackle creating the functionality of the application. This structure is based on the Business Logic Layers. The focus on this part is to have RESTful APi and endpoints that ensure an effective web connection. It will also give a greater scope on how application look before having a front-end. 

▶  **Table of Contents**

- [Overview](#overview)
- [Concepts](#concepts)
- [Example](#example)
- [Installation](#Installation)
- [Author](#author)

▶  **Overview**

Throughout this project you'll see API and endppoint implementation using Flask documentation and Python that follow the Facade design pattern. A test layer was added to ensure function between Flask and the apps endpoints besides using curl.

▶  **Concepts**

- Setting up the structure with the directory and files following this:


		hbnb/
		├── app/
		│   ├── __init__.py
		│   ├── api/
		│   │   ├── __init__.py
		│   │   ├── v1/
		│   │       ├── __init__.py
		│   │       ├── users.py
		│   │       ├── places.py
		│   │       ├── reviews.py
		│   │       ├── amenities.py
		│   ├── models/
		│   │   ├── __init__.py
		│   │   ├── user.py
		│   │   ├── place.py
		│   │   ├── review.py
		│   │   ├── amenity.py
		│   ├── services/
		│   │   ├── __init__.py
		│   │   ├── facade.py
		│   ├── persistence/
		│       ├── __init__.py
		│       ├── repository.py
		├── run.py
		├── config.py
		├── requirements.txt
		├── README.md

- The function __init__ is added to initialize the functions within each directory.
- Flask was used as the framework that is flexible so is the application can be scaled.
- UUID's are added so data can be pulled and distributed.
- This was made by first adding the core business logic classes followed by the user, amenity, place and review endpoints to handle CRUD operations, create, read, update and delete. The delete operation will be added later in the project.
- Follows the facade structural design pattern that can be implemented using classes.


▶   **Example**

	class HBnBFacade:
	    def __init__(self):
	       self.user_repo = InMemoryRepository()

                     ...

	    def create_user(self, user_data)
		self.user_repo.add(user)
		return user


▶   **Installation**

Clone this in your terminal:

	git clone https://github.com/kamisos3/holbertonschool-hbnb/tree/main/part2

Then install from requirements.txt pytest, flask and flask-restx:

	pip install -r requirements.txt

Now you'll be able to run and test HBnB testpoints, you can use one of these commands:

	python run.py
	python3 run.py

▶   **Author**

Kami Sostre [https://github.com/kamisos3]
