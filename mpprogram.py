"""
Question1: How can we keep a process running and waiting, and push it job to process when needed?
Answer: To keep a process running and waiting and push it job to process we can use
Python Multiprocessing with Queue for inter-process communication.  

Question2: How to share data (large data) between two processes? How to avoid race conditions 
of writing / reading from same source.
Answer: To share large data between two processes and avoid race conditions of reading writing
from same resource we can use Python Multiprocessing and Queue as queues are process safe
and help avoid race conditions in inter-process communication.
"""

import multiprocessing
import os


def producer_function(queue, num_items):
    """Function that adds items to the queue."""
    for i in range(num_items):
        # Add item to queue
        queue.put(f"Item {i}")
        # print the item and process id
        print(f"Produced: Item {i} by process: {os.getpid()}")


def consumer_function(queue):
    """Function that print items from the queue"""
    while True:
        try:
            # Get an item from queue
            item = queue.get()
        except queue.Empty:
            # Handle the case when the queue is empty (no jobs)
            continue
        if item is None:
            # Break from loop when None is recieved
            break
        # print the item and process id
        print(f"Consumed: {item} by process: {os.getpid()}")


if __name__ == "__main__":
    # Create multiprocessing queue
    shared_queue = multiprocessing.Queue()

    # Number of items to produce large data
    NUM_ITEMS = 1000

    # Number of processes
    PROCESSES_COUNT = 4

    # Create producer process
    producer_process = multiprocessing.Process(
        target=producer_function, args=(shared_queue, NUM_ITEMS)
    )

    # Create consumer processes
    consumer_processes = []
    for _ in range(PROCESSES_COUNT):
        consumer_process = multiprocessing.Process(
            target=consumer_function, args=(shared_queue,)
        )
        consumer_processes.append(consumer_process)

    # Start producer process
    producer_process.start()

    # Start consumer processes
    for consumer_process in consumer_processes:
        consumer_process.start()

    # Wait for the producer process to finish
    producer_process.join()

    # Add None to queue for each process
    for _ in range(PROCESSES_COUNT):
        shared_queue.put(None)

    # Wait for consumer processes to finish
    for consumer_process in consumer_processes:
        consumer_process.join()
