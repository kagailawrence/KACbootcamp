

students = ["Kim", "Lawrence", "Joy", "Sam"]
scores = [82, 68, 47, 90]

for i in range(len(students)):
    name = students[i]
    score = scores[i]

    if score >= 70:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 50:
        grade = "C"
    else:
        grade = "Fail"

    print(f"{name}: Score = {score}, Grade = {grade}")



    """
    1.refactor the code,use both the [] && {} data structures
    2. add a new student "Alice" with score 55
    3.sort the output by score in descending order

    """

