import subprocess
import time
import yaml


# TODO - that is a basic func
def execute_job(cmd):
    outputs = {}
    start_time = time.time()
    try:
        output = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.output)
    except FileNotFoundError as e:
        print("command {} not found".format(cmd))
    finally:
        end_time = time.time()
        outputs["time"] = end_time - start_time
        if output:
            outputs["ret_code"] = output.returncode
        else:
            outputs["ret_code"] = "1"
    return outputs


def get_jobs(jobs_yaml):
    with open(jobs_yaml, "r") as f:
        try:
            jobs = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    return jobs
