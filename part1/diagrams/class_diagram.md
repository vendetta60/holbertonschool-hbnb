
---

✅ **Task 1 – Business Logic Class Diagram**

```md
## Business Logic Layer – Class Diagram

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
    +updateProfile()
    +delete()
}

class Place {
    +title: string
    +description: string
    +price: float
    +latitude: float
    +longitude: float
    +update()
    +delete()
}

class Review {
    +rating: int
    +comment: string
    +update()
    +delete()
}

class Amenity {
    +name: string
    +description: string
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
