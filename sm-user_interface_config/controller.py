import threading
import subprocess

def run_script1():
    subprocess.call(["python", "app.py"])

def run_script2():
    subprocess.call(["python", "config_mqtt.py"])

# Create two threads, one for each script
t1 = threading.Thread(target=run_script1)
t2 = threading.Thread(target=run_script2)

# Start both threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()
