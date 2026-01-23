
---

# 3️⃣ `part1/diagrams/class_diagram.md`

```md
## Detailed Class Diagram – Business Logic Layer

This document provides a class diagram of the Business Logic layer for HBnB Evolution, showing entities, attributes, methods, and relationships.

```mermaid
classDiagram

class BaseModel {
    +id: UUID
    +created_at: datetime
    +updated_at: datetime
}

class User {
    +first_name: string
    +last_name: string
    +email: string
    +password: string
    +is_admin: boolean
    +register()
    +updateProfile()
    +delete()
}

class Place {
    +title: string
    +description: string
    +price: float
    +latitude: float
    +longitude: float
    +create()
    +update()
    +delete()
}

class Review {
    +rating: int
    +comment: string
    +create()
    +update()
    +delete()
}

class Amenity {
    +name: string
    +description: string
    +create()
    +update()
    +delete()
}

BaseModel <|-- User
BaseModel <|-- Place
BaseModel <|-- Review
BaseModel <|-- Amenity

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "*" --> "*" Amenity : includes

Entity Descriptions

User: Represents a system user (regular or admin). Can own multiple places and write reviews.
Attributes: first_name, last_name, email, password, is_admin
Methods: register(), updateProfile(), delete()

Place: Represents a property listed by a user. Can have multiple amenities and reviews.
Attributes: title, description, price, latitude, longitude
Methods: create(), update(), delete()

Review: Represents feedback by a user for a place.
Attributes: rating, comment
Methods: create(), update(), delete()

Amenity: Represents features/services that can be associated with places.
Attributes: name, description
Methods: create(), update(), delete()

Relationships

Inheritance: All entities inherit from BaseModel.

User – Place: One user can own multiple places.

User – Review: One user can write multiple reviews.

Place – Review: One place can have multiple reviews.

Place – Amenity: Many-to-many relationship.
