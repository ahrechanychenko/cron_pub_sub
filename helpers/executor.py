import subprocess
import time
import yaml


# TODO - that is a basic func
def execute_job(cmd):
    outputs = {}
    start_time = time.time()
    try:
        cmd = cmd.split()
        print(cmd)
        output = subprocess.run(cmd, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.output)
    except OSError as e:
        print("command {} not found".format(cmd))
    finally:
        end_time = time.time()
        outputs["time"] = end_time - start_time
        if 'output' in locals():
            outputs["ret_code"] = output.returncode
            outputs["output"] = output
        else:
            outputs["ret_code"] = "1"
            outputs["output"] = "Command not found"
    return outputs


def get_jobs(jobs_yaml):
    with open(jobs_yaml, "r") as f:
        try:
            jobs = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    return jobs
