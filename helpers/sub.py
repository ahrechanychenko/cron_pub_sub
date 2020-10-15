from google.cloud import pubsub_v1
import sys


def receive_messages(project_id, subscription_id, jobs, timeout=None):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]
    from concurrent.futures import TimeoutError
    from google.cloud import pubsub_v1

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_id}`
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print("Received message: {}".format(message))
        message.ack()
        jobs.append(message.data)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on {}..\n".format(subscription_path))

    # Wrap subscriber in a 'with' block to automatica   lly call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()