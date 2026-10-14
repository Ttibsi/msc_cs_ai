# Week 6 - SQL, Distributed Data, Hadoop

* Explain the models of databases for BIg Data. [MLO4]
* Explain how Big Data causes problems for analytics. [MLO4]
* Explain how SQL databases can help represent a wide variety of data. [MLO4]
* Explain how distributed computation approaches such as Hadoop  can allow computation on huge volumes of data. [MLO4]

### Lesson 1 - Constructing and Querying a Database
Structured Query Language (SQL) is both a Data Definition and Data Manipulation Language.
```sql
CREATE table `STUDENT` VALUES (
    `studentID` INT NOT NULL,
    `firstName` VARCHAR(45) NULL,
    PRIMARY KEY(`studentID`)
);
```

The exact syntax will depend on the exact database product being used. Above is a mix of the
example in the learning material and sqlite. This probably doesn't execute anywhere.

We can then insert data using the `INSERT INTO` statement.
Querying is done using a `SELECT` statement:
```sql
SELECT firstName FROM STUDENT;
```

however, this is much more powerful. You can use a `WHERE` clause to apply a condition:
```sql
SELECT studentID FROM STUDENT WHERE firstName == "Bill";
```

`GROUP BY` clause - added to a SELECT statement for grouping results
`HAVING` - filters the groups created by GROUP BY based on conditions involving aggregates
`ORDER BY` - sort the results by a given column in ascending or descending order

Joining tables together changes in complexity depending on which syntax you use.
```sql
SELECT * FROM STUDENT,COURSE;
```

This is where the `WHERE` clause comes in useful. (note this example doesn't make too much sense)
```sql
SELECT * FROM STUDENT,COURSE WHERE STUDENT.studentID = COURSE.studentID;
```

Finding students with the same last name is more complex than first appears:
```sql
SELECT s1.studentID, s1.firstName, s1.lastName, s2.studentID, s2.firstName, s2.lastName
FROM STUDENT s1, STUDENT s2
WHERE s1.lastName = s2.lastName AND s1.studentID <> s2.studentID;
```

note `<>` is the "not equal" symbol in SQL. This last AND statement prevents matching the same
student against themselves.

Aggregate functions allow us to do more with the data we can see:
```sql
SELECT lastName, count(*) AS nameCount
FROM STUDENT
GROUP BY lastName
HAVING nameCount > 1;
```
This will give us two rows, every lastName in the database and the count of the number of
times that lastName appears. The `HAVING` clause means that we only see non-unique lastNames.

### Task 1 - Writing SQL statements
These tasks use a mySQL server provided by the uni

1. Write a query to get all student details from the STUDENT table, ordered by auth.
```sql
select * from `STUDENT` ORDER BY `auth`
```

2. Now write a query to get all student details from the STUDENT table, but use ‘group by auth’
instead. What does it show? You should see only one record for each authority.
Amend the select query to count the number in each group, and output the count with the name of the authority.
```sql
select auth, count(*) as authCount from `STUDENT` GROUP BY `auth`
```

3. Write a query to count the enrolments on each subject. To do this, start by selecting data
from SUBJECT and ENROLL where the subjectId matches. Next add a clause to group the output
by the subjectName. Finally, modify the select clause to count the records in each group.
```sql
select subjectName, count(*) as enrollments
from ENROLL, SUBJECT
where ENROLL.subjectId = SUBJECT.subjectID
group by SUBJECT.subjectName;
```

4. Write a query to display the names and student ID of all students taking subjects History.
This is a more complex query – you need to match the STUDENT table to the ENROLL table,
and the ENROLL table to the SUBJECT table, and add a condition to restrict results to only those where the subject is History.
```sql
SELECT DISTINCT s.studentID, s.firstName, s.lastName FROM STUDENT s
JOIN ENROLL e on s.studentID = e.studentID
JOIN SUBJECT on e.subjectId = SUBJECT.subjectId
WHERE SUBJECT.subjectName = "History"
```

5. Write a query to get the names of the student taking Maths who have a ‘U’ grade.
This is an extension of the previous form of query, adding another condition to the where clause.
```sql
SELECT DISTINCT s.studentID, s.firstName, s.lastName, e.grade FROM STUDENT s
JOIN ENROLL e on s.studentID = e.studentID
JOIN SUBJECT on e.subjectId = SUBJECT.subjectId
WHERE SUBJECT.subjectName = "Maths"
AND e.grade = "U"
```

### Lesson 2 - Next Generation of databases
These are databases that don't use the realtional model, such as nosql databases.
They rely on graphs and other database architectures

nosql = "not only sql".

ACID consistency model
    - Atomic - all operations in a database transaction should be atomic
    - Consistent - All users see the same updated data
    - Isolated - transactions do not contend with each other to modify data.
        - Trying to modify the same data at the same time is moderated by the database,
        queuing the transactions to prevent issues
    - Durable - The results of a transaction are permanent, even with failures

BASE consistency model
    - Basic availability
    - Soft state - when the database is updated, it may be inconsistent for some time
    - Eventual consistency - when the database is in a known, consistent state

BASE is primarily used by key-value and document stores
(Redis, maybe?)

Key-Value stores - a type of database, everything is treated as a blob of data associated with a key.
Document database - document stores, Similar to KV stores, they instead store all data inside
    large JSON or XML documents in their memory
Graph databases - ex graphQL, Modelled on a graph, nodes are data values and edges are relationships.

XQuery - a language designed to query XML documents, often used in XML-based databases
eXist - XML database open source example

xml-based databases are often used in content management systems.
json-based databases are often used in web-based workloads.
