# Problem 5

Students = [ {"student_id": 1, "name": "Bob", "email": "bob213@myu.edu", "year": 2},
{"student_id": 2, "name": "Alice", "email": "alice223129@myu.edu", "year": 5},
{"student_id": 2, "name": 17, "email": "charlie2@myu.edu", "year": 3} ]

# Problem 5.1
# Function Definition for primary key constraints
def check_primary_key_constraints(students):
    seen_ids = set()

    for student in students:
        student_id = student.get("student_id")

        if student_id in seen_ids:
            return "The data do not follows the primary key constraints"

        seen_ids.add(student_id)

    return "The data follows the primary key constraints"

#Problem 5.2
# Function Definition for domain constraints
def check_domain_constraints(students):
    for student in students:
        sid = student.get("student_id")
        violations = []

        # year check
        year = student.get("year")
        if year not in (1, 2, 3, 4):
            violations.append("incorrect year")

        # name check (type + length)
        name = student.get("name")
        if not isinstance(name, str):
            violations.append("name is not a string")
        else:
            if len(name) > 20:
                violations.append(f"name length is {len(name)}")

        # email check (username length only)
        email = student.get("email")
        if isinstance(email, str) and "@" in email:
            username = email.split("@")[0]
            if len(username) > 8:
                violations.append(f"email username length is {len(username)}")
        else:
            violations.append("invalid email format")

        # print results
        if violations:
            print(f"Student with ID {sid} violations: {', '.join(violations)}")
        else:
            print(f"Student with ID {sid} follows all domain constraints")

# Function Call for primary key constraints
result = check_primary_key_constraints(Students)
print(result)

# Function Call for domain constraints
check_domain_constraints(Students)

# Problem 6

Enrollments = [ (1, "DSC 450"), (1, "CSC 402"), (1, "IS 451"), (1, "DSC 578") , (1, "CSC 444"),
                (1, "DSC 501"), (3, "CSC 555")]

# Function Definition to check Enrollment Constraints
def check_enrollment_constraints(enrollments):
    course_count = {}

    for student_id, _ in enrollments:
        if student_id in course_count:
            course_count[student_id] += 1
        else:
            course_count[student_id] = 1

    violations = []
    for student_id, count in course_count.items():
        if count < 1 or count > 4:
            violations.append((student_id, count))

    return violations

# Function call for enrollment constraints check
enroll_violations = check_enrollment_constraints(Enrollments)
print(f"Student with ID: {enroll_violations[0][0]} has enrolled in: {enroll_violations[0][1]} courses")