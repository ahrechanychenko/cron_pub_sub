import uuid

from celery import Celery
from celery.execute import send_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('pubsub',
             broker='redis://',
             backend='redis://')

app.conf.beat_schedule = {
    'fetch-tasks': {
        'task': 'pubsub.fetch_tasks',
        # Every 30 sec
        'schedule': 30.0,
    },
}

def fetch_data():
    return (uuid.uuid4() for _ in range(10))

@app.task(ignore_result=True, name='pubsub.fetch_tasks')
def fetch_tasks():
    for task in fetch_data():
        send_task('pubsub.exec_command', (task,))

@app.task(name='pubsub.exec_command')
def exec_command(cmd):
    logger.info(f'Got task with data {cmd}')
    return cmd

if __name__ == '__main__':
    app.start()


