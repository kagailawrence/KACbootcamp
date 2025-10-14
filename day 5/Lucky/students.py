import json

# Step 1: Load data from the "database"
with open('students_db.json', 'r') as file:
    students = json.load(file)

# Step 2: Add three new students
new_students = [
    {"name": "Alice", "score": 55},
    {"name": "Brian", "score": 78},
    {"name": "Cynthia", "score": 62}
]
students.extend(new_students)

# Step 3: Function to assign grade based on score
def get_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "Fail"

# Step 4: Update all students with their grades
for student in students:
    student["grade"] = get_grade(student["score"])

# Step 5: Define grade ranking for sorting (A highest, Fail lowest)
grade_order = {"A": 1, "B": 2, "C": 3, "Fail": 4}

# Step 6: Sort by grade ascending (A → Fail), then by score within grade
sorted_students = sorted(
    students, 
    key=lambda x: (grade_order[x["grade"]], x["score"])
)

# Step 7: Display results in a neat table
print("📘 Student Grades (Ascending by Grade)\n")
print(f"{'Name':<10} {'Score':<6} {'Grade'}")
print("-" * 25)
for s in sorted_students:
    print(f"{s['name']:<10} {s['score']:<6} {s['grade']}")

# Step 8: Save the updated list back to JSON file
with open('students_db.json', 'w') as file:
    json.dump(sorted_students, file, indent=4)

print("\n✅ Student data updated and saved to 'students_db.json'")
