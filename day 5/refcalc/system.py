import json


with open('students_db.json', 'r') as file:
    students = json.load(file)

# Step 2: Add a new student (Alice)
students.append({"name": "Alice", "score": 55})

# Step 3: Define a function to determine grades
def get_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "Fail"

# Step 4: Assign grades to each student
for student in students:
    student["grade"] = get_grade(student["score"])

# Step 5: Sort students by score (descending order)
sorted_students = sorted(students, key=lambda x: x["score"], reverse=True)

# Step 6: Display results
print("Student Grades (Sorted by Score)\n")
for s in sorted_students:
    print(f"{s['name']}: Score = {s['score']}, Grade = {s['grade']}")

# Step 7: Save updated data back to JSON file (our 'database')
with open('students_db.json', 'w') as file:
    json.dump(sorted_students, file, indent=4)

print("\nStudent data updated and saved to 'students_db.json'")
