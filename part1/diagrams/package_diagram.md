## High-Level Package Diagram

```mermaid
classDiagram
direction TB

package "Presentation Layer" {
    class API {
        +registerUser()
        +updateUser()
        +createPlace()
        +createReview()
        +listPlaces()
    }
}

package "Business Logic Layer" {
    class HBnBFacade {
        +createUser()
        +updateUser()
        +deleteUser()
        +createPlace()
        +updatePlace()
        +deletePlace()
        +createReview()
        +getPlaces()
    }

    class User
    class Place
    class Review
    class Amenity
}

package "Persistence Layer" {
    class Repository {
        +save()
        +update()
        +delete()
        +findById()
        +findAll()
    }
}

API --> HBnBFacade : Facade Pattern
HBnBFacade --> User
HBnBFacade --> Place
HBnBFacade --> Review
HBnBFacade --> Amenity
HBnBFacade --> Repository : CRUD Operations
