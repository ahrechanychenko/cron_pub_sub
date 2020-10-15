# import multiprocessing
from time import sleep
import threading
# import sys
import os

# from helpers.executor import execute_job
from helpers.executor import get_jobs
from helpers.sub import receive_messages


if __name__ == '__main__':
    try:
        project_id = "pub-sub-demo-292308"
        subscription_id = "sub_one"
        id_to_cmd = get_jobs(os.environ.get("CMD_YAML", "cmds.yaml"))

        print("\nChecking for a new jobs: \n ...")
        jobs_to_execute = []
        sleep(30)

        try:
            download_thread = threading.Thread(target=receive_messages,
                                               name="Downloader",
                                               args=(project_id, subscription_id, jobs_to_execute))
            download_thread.daemon = True
            download_thread.start()
        except KeyboardInterrupt:
            print("exiting")
        while True:
            if jobs_to_execute:
                print("list of remaining:\n {}".format(jobs_to_execute))
                for job in jobs_to_execute:
                    print("job id is: {}".format(job))
                    #TODO - add multiproccessor async execution
                    print("finished, removing job from queue")
                    jobs_to_execute.remove(job)
                    if jobs_to_execute:
                        print("list of remaining:\n {}".format(jobs_to_execute))

            else:
                print("There are no waiting jobs to execute. "
                      "sleeping for a 30 sec")
                sleep(30)
                continue
    except KeyboardInterrupt:
        exit(1)
