#TODO - timeout and retry for pub/sub to avoid forever loop
#TODO - execution

import multiprocessing
from time import sleep
import threading
import os
import argparse

from helpers.executor import execute_job
from helpers.executor import get_jobs
from helpers.sub import receive_messages


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='#TODO')
    parser.add_argument('--project-id')
    parser.add_argument('--subscription-id')
    args = parser.parse_args()
    project_id = args.project_id
    subscription_id = args.subscription_id
    id_to_cmd = get_jobs(os.environ.get("CMD_YAML", "cmds.yaml"))

    print("\nChecking for a new jobs: \n ...")
    jobs_to_execute = multiprocessing.Manager().Queue()
    sleep(5)

    try:
        download_thread = threading.Thread(target=receive_messages,
                                           daemon=True,
                                           name="Downloader",
                                           args=(project_id, subscription_id, jobs_to_execute))
        download_thread.start()
        while True:
            if jobs_to_execute.qsize() > 0:
                count = multiprocessing.cpu_count()
                pool = multiprocessing.Pool(processes=count*3)
                res = pool.apply_async(execute_job, (jobs_to_execute,)).get()
                print(res)
                pool.terminate()
                pool.join()

            else:
                sleep(10)
                print("no jobs to execute")
                continue

    except KeyboardInterrupt:
        print("exiting")
        exit(1)