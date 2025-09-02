import time

def call_background_task(message: str):
    time.sleep(2)
    print("Background Task called!", flush=True)
    print(f"Message: {message}", flush=True)

