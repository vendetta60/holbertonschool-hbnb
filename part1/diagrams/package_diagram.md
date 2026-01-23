## High-Level Package Diagram

This diagram illustrates the three-layer architecture of the HBnB Evolution application and shows the communication between layers using the **Facade Pattern**.

```mermaid
classDiagram
class PresentationLayer {
    +ServiceAPI
}
class BusinessLogicLayer {
    +ModelClasses (User, Place, Review, Amenity)
}
class PersistenceLayer {
    +DatabaseAccess
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations


Layer Descriptions

Presentation Layer: Handles all user-facing services and APIs.

Business Logic Layer: Implements core entities and business rules.

Persistence Layer: Responsible for storing and retrieving data from the database.

Facade Pattern: Provides a single interface for the Presentation Layer to communicate with the Business Logic Layer.
