# Celery example

### Installation

```shell

apt install redis
service redis start

git clone <repo>
cd <repo>
git checkout celery

virtualenv celery
source celery/bin/activate
pip install 'celery[redis]'
```

### How to run 
```shell

celery -A pubsub worker -B -l INFO

```


