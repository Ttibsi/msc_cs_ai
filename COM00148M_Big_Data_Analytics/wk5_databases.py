# Week 5 - Datbases, Normalisation

* Explain the purpose and benefits of using a database management system (DBMS) over custom or file-based approaches to data storage.
* Describe the key features of the relational database model, including how data is structured into tables and how relationships are represented.
* Identify and define core relational concepts such as primary keys, foreign keys, and functional dependencies.>
* Apply the principles of normalisation to transform unnormalised schemas into First, Second, and Third Normal Form (1NF, 2NF, 3NF), and explain the rationale behind each step.
* Evaluate the advantages of normalised relational schemas in terms of data integrity, consistency, and reduction of redundancy.

### Lesson 1 - Why Databases
Database - A collection of related data items within a specific business process or
problem setting
DBMS - Database management system
Database model/schema - Description of the data at different levels of detail.

Conceptual data model - high level description of dta items and characteristics
    - represented with an Enhanced Entity Relationship model (EER)
Logical Data Model - translates the conceptual data model into a specific
    implementation.

Three layer architecture
- conceptual/logical layer
- external layer - any external data model, including UI views
- internal layer - specifies how data is stored or organised physically.

User types
- information architect
- business user
- database administrator
- application developer

Data definition language - used by a DBA to represent these models
Data manipulation language - used for CRUD operations

### Lesson 2 - Data modelling
ERD - Entity Relationship Diagram

Entities are represented as rectangles with a singular noun
    - ex `student`
Attributes are pieces of information to store on each entity
    - ex `id`, `name` etc
    - Drawn as an oval pointing to an entity
Composite attributes - attributes made of multiple others
Multivalue attributes - arrays
Derived values - that can be calculated based off other data
    - ex age can be calculated off of stored DOB
key attributes - unique identifiers, eg ID field

Relationships are shown as diamonds connecting two entities.
    - relationships can have their own attributes
Cardinality: 101, 1-many, many-many

Weak entity - cannot be uniquely identified by it's own attribute
    - ex `course material` cannot be uniquely identified without knowing what course
    they belong to
    - This uses a composite key, which is a unique identifier formed by combining
    multiple fields

Limitations
- temporal constraints cannot be represented in an ERD
- ERDs cannot represent complex business rules, eg prerequisite classes for a course
- ERDs don't include domain constraints
    - eg "course credits must be an integer between 10 and 20"
