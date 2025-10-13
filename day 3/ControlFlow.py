"""
Control Flow: if, elif, else
Control flow allows your program to make decisions and
run specific code based on certain conditions.


Example
If the student's score is above 50, they pass. Otherwise, they fail.
"""



score = 25

if score >= 70:
    print("Grade: A")
elif score >= 60:
    print("Grade: B")
elif score >= 50:
    print("Grade: C")
else:
    print("Grade: Fail")






"""
Takeaway:

if checks the first condition.
elif / else if checks the next ones.
else runs if none of the above are true.
"""