import os

from celery import Celery
from celery.execute import send_task
from celery.utils.log import get_task_logger

from helpers.sub import receive_messages
from helpers.executor import execute_job

logger = get_task_logger(__name__)

app = Celery('pubsub',
             broker='redis://',
             backend='redis://')

app.conf.beat_schedule = {
    'fetch-tasks': {
        'task': 'pubsub.fetch_tasks',
        # Every 30 sec
        'schedule': 60.0,
    },
}


@app.task(ignore_result=True, name='pubsub.fetch_tasks')
def fetch_tasks():
    project_id = os.getenv("PROJECT")
    subscription_id = os.getenv("SUBSCRIPTION")
    print(project_id, subscription_id)
    tasks = receive_messages(project_id, subscription_id, timeout=10)
    print(tasks)
    if tasks:
        for task in tasks:
            print(task)
            send_task('pubsub.exec_command', (task,))

@app.task(name='pubsub.exec_command')
def exec_command(cmd):
    logger.info('Got task with data {cmd}'.format(cmd=cmd))
    print("Executing task")
    execute_job(cmd)

if __name__ == '__main__':
    app.start()


