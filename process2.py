"""process 2"""
import time
import sys

while True:
    sys.stdout.write("Message from process 2")
    sys.stdout.flush()
    time.sleep(3)
