import multiprocessing as mp

def washer(dishes, output):
    for dish in dishes:
        print('Washing', dish, 'dish')
        output.put(dish)

def dryer(input):
    while True:
        dish = input.get()
        print('Drying', dish, 'dish')
        input.task_done()

dish_queue = mp.JoinableQueue()
dryer_proc = mp.Process(target=dryer, args=(dish_queue,))
dryer_proc.daemon = True
dryer_proc.start()

dishes = ['salad', 'bread', 'entree', 'dessert']
washer(dishes, dish_queue)
dish_queue.join()
"""
This code demonstrates a simple multiprocessing system where one process (`washer`) is responsible for putting items (dishes) into a queue, and another process (`dryer`) continuously processes items from that queue. Here’s a detailed breakdown of how the code works:

### Key Components:

1. **`multiprocessing` Module**: This module allows you to create processes, share data between them, and manage concurrent execution in Python.
   
2. **`JoinableQueue`**: A specialized queue that allows tasks to be marked as done, enabling the main process to wait until all tasks are completed before proceeding.

### Detailed Explanation:

#### Functions:

1. **`washer(dishes, output)`**:
   - Takes a list of `dishes` and an `output` queue as arguments.
   - Iterates over each dish in the list.
   - Prints a message indicating that a dish is being washed.
   - Puts the washed dish into the `output` queue.

2. **`dryer(input)`**:
   - Takes an `input` queue as an argument.
   - Runs an infinite loop, continuously pulling items from the queue.
   - For each dish, it prints a message indicating that the dish is being dried.
   - Calls `task_done()` on the queue to indicate that the task is completed for that dish.

#### Main Execution:

1. **Queue and Process Initialization**:
   - `dish_queue = mp.JoinableQueue()`: Creates a `JoinableQueue` to hold the dishes.
   - `dryer_proc = mp.Process(target=dryer, args=(dish_queue,))`: Creates a new process for the `dryer` function, passing the `dish_queue` as an argument.
   - `dryer_proc.daemon = True`: Sets the `dryer_proc` as a daemon process. This means it will terminate when the main process exits.
   - `dryer_proc.start()`: Starts the `dryer_proc` process, which begins running the `dryer` function in parallel.

2. **Washing Process**:
   - `dishes = ['salad', 'bread', 'entree', 'dessert']`: Defines a list of dishes to be washed.
   - `washer(dishes, dish_queue)`: Calls the `washer` function with the list of dishes and the `dish_queue`. Each dish is washed (printed) and then put into the queue.

3. **Waiting for Tasks to Complete**:
   - `dish_queue.join()`: This call blocks the main process until all items in the queue have been processed and `task_done()` has been called for each item. It ensures that the main process waits for all dishes to be dried before continuing or exiting.

### Summary:

- **`washer`** puts items into the queue, indicating they are ready to be dried.
- **`dryer`** runs in a separate process and keeps pulling items from the queue to process (dry them).
- The use of `JoinableQueue` and `task_done` ensures proper synchronization, so the main program knows when all dishes are processed (washed and dried).

This system demonstrates basic inter-process communication (IPC) using queues to pass data and ensure coordinated task completion between processes in Python's `multiprocessing` framework.
"""
