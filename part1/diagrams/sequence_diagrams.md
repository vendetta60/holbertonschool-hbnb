
---

# 4️⃣ `part1/diagrams/sequence_diagrams.md`

```md
## Sequence Diagrams – API Calls

This document shows how the Presentation Layer, Business Logic Layer, and Persistence Layer interact for key API calls.

---

### 1. User Registration

```mermaid
sequenceDiagram
participant Client
participant API
participant Facade
participant User
participant Repository

Client ->> API: POST /users
API ->> Facade: createUser(userData)
Facade ->> User: create()
Facade ->> Repository: save(user)
Repository -->> Facade: success
Facade -->> API: user created
API -->> Client: 201 Created


2. Place Creation
sequenceDiagram
participant Client
participant API
participant Facade
participant Place
participant Repository

Client ->> API: POST /places
API ->> Facade: createPlace(placeData)
Facade ->> Place: create()
Facade ->> Repository: save(place)
Repository -->> Facade: success
Facade -->> API: place created
API -->> Client: 201 Created

3. Review Submission
sequenceDiagram
participant Client
participant API
participant Facade
participant Review
participant Repository

Client ->> API: POST /reviews
API ->> Facade: createReview(reviewData)
Facade ->> Review: create()
Facade ->> Repository: save(review)
Repository -->> Facade: success
Facade -->> API: review created
API -->> Client: 201 Created

4. Fetch List of Places
sequenceDiagram
participant Client
participant API
participant Facade
participant Repository

Client ->> API: GET /places
API ->> Facade: getPlaces()
Facade ->> Repository: findAll()
Repository -->> Facade: list of places
Facade -->> API: places list
API -->> Client: 200 OK

Explanatory Notes

Each diagram shows the flow of information from Client → API → Facade → Business Logic → Repository → Database.

The Facade pattern simplifies interactions between layers.

These diagrams cover the main use cases required by the project.
