#divid and conquer With comment
def binary_search(arr, target):     
    left, right = 0, len(arr) - 1  # Initialize the left and right pointers
    while left <= right:           # Continue until the pointers meet
        mid = (left + right) // 2  # Find the middle index
        if arr[mid] == target:     # Check if the middle element is the target
            return mid              # Target found, return the index
        elif arr[mid] < target:    # If target is greater, ignore left half
            left = mid + 1
        else:                      # If target is smaller, ignore right half
            right = mid - 1
    return -1                      # Target not found, return -1
# Example usage
arr = [1, 2, 3, 4, 5, 6]
target = 4      
result = binary_search(arr, target)
if result != -1:
    print(f"Element found at index {result}")
else:
    print("Element not found in the array")
    
