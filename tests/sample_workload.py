import time


print("MemLens: Starting sample memory workload...")

# Create a large list to consume memory
data = []

for i in range(5):
    data.append([0] * 500000)

    print(f"Step {i + 1}: Memory allocated")

    time.sleep(1)

print("\nMemory workload completed!")

# Keep memory allocated for 10 seconds
time.sleep(10)

del data

print("Memory released!")
