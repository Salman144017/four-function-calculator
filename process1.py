"""process 1"""
import time
import sys

while True:
    sys.stdout.write("Message from process 1")
    sys.stdout.flush()
    time.sleep(2)
