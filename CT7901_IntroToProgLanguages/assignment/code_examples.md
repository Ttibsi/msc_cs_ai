# geltmsoftlang code examples

### Associative array
```
var studentAge: map[str, int] = {
    "Jason": 17,
    "Zack": 17,
    "Billy": 16,
    "Trini": 16,
    "Kimberly": 17,
    "Tommy": 16
};
```

* As a list
```
// Implicit indexing
var students: map[int, str] = {"Jason", "Zack", "Billy", "Trini", "Kimberly", "Tommy"};
print(studentx[0]); // Jason

// Explicit indexing
var students: map[int, str] = {
    0: "Jason",
    1: "Zack",
    2: "Billy",
    3: "Trini",
    4: "Kimberly",
    5: "Tommy"
};
```

* structs
```
var tommyOliver: map[str: str] = {
    "FirstName": "Tommy",
    "LastName": "Oliver",
    "FavouriteColour": "Green",
};
```

* classes
```
// also spot functions with annotated return types and functions as a valid 
// type in our type system
var tommyOliver: map[str: (str)func() ] = {
    "getSurname": function() str {
        return self.LastName; // Implicit self passed to method
    };
};

print(tommyOliver.getSurname());
```

* Nested tables
```
var tommyOliver: map[str: map[str: str] ] = {
    "friendsWithFavouriteColours": {
        "Jason": "Red",
        "Zack": "Black",
        "Billy": "Blue",
        "Trini": "Yellow",
        "Kimberly": "Pink",
    }
};
```

* student data
```
var students: map[str: map[str, int]] = {
    "Tommy": {
        "Attendance": 74,
        "TotalGrades": 44
    },
    "Jason": {
        "Attendance": 98,
        "TotalGrades": 80
    },
}
```

* test results
```

var mathTests: map[str: map[str, int]] = {
    "Arithmetic 1": {
        "Total marks": 10,
        "Jason": 9,
        "Tommy": 4
    },
    "Shapes and Angles": {
        "Total marks": 40,
        "Jason": 29,
        "Tommy": 36 
    },
}
```

### Union

* Union example
```
// If a student's name isn't known internally, call a function to 
// query the database
var studentAge: union[int, (int)func(str)] = function(name: str) int {
    return query_db(name, "StudentAge");
}
```

* Optional
```
var litExamResult: union[float, Null] = Null
if (name != Null) { print(litExamResult); } 
```

* Attendance
```
var JasonAttendance: map[str, union[bool, Null]] = {
    "Mon": true,
    "Tue": False,
    "Wed": Null,
    "Thurs": Null, 
    "Fri": Null
}
```

* Quizzes
```
var quizQuestionL str = "When was the Battle of Hastings?";
var quizAnswers: map[int, union[int, str]] = {
    1066,
    "13th century",
    "10th century",
    1940
};

```

* Bigger class
```
var tommyOliver: map[str, union[str, map[int, int], ()func()] = {
    "faveColour": "green",
    "grades": {19, 32, 64, 68},
    "gradeAverage": function() {
        return sum(grades) / len(grades)
    }
};
```
