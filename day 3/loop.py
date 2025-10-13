#Loops let you repeat code until a condition is met 
#great for automation or handling lists of data.


#for Loop
for i in range(1, 6):
    print("Number:", i)


# while Loop
count = 1
while count <= 5:
    print("Count:", count)
    count += 1

"""
Best Practice:

Use for when you know how many times you'll loop.
Use while when the loop depends on a condition that changes dynamically.
Be cautious with while loops to avoid infinite loops.
"""