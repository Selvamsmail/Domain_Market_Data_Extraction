import subprocess
import multiprocessing
import time

def run_script(script_name):
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    script_names = [
        "1_domain_click.py",
        "2_domain_click.py",
        "3_domain_click.py", 
    ]

    processes = []

    for script_name in script_names:
        process = multiprocessing.Process(target=run_script, args=(script_name,))
        processes.append(process)
        process.start()

    try:
        while True:
            running_processes = sum(1 for process in processes if process.is_alive())
            print(f"Number of scripts running: {running_processes}")
            time.sleep(30)

    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

    finally:
        for process in processes:
            process.join()