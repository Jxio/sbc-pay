"""This module provides Queue type services."""
import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import uuid
from concurrent.futures import CancelledError
from concurrent.futures import TimeoutError  # pylint: disable=W0622

from flask import current_app
from google.auth import jwt
from google.cloud import pubsub_v1
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from pay_api.services.gcp_queue.gcp_queue import GcpQueue

from .invoice import Invoice


@dataclass
class QueueMessage:
    """Queue message data class."""

    source: str
    message_type: str
    payload: dict
    topic: str


def publish_to_queue(queue_message: QueueMessage):
    """Publish to GCP PubSub Queue using queue."""
    if queue_message.topic is None:
        current_app.logger.info('Skipping queue message topic not set.')
        return

    # Create a SimpleCloudEvent from the QueueMessage
    cloud_event = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f'sbc-pay-{queue_message.source}',
        # Intentionally blank, this field has been moved to topic.
        subject=None,
        time=datetime.now(tz=timezone.utc).isoformat(),
        type=queue_message.message_type,
        data=queue_message.payload
    )

    # Initialize queue and publish
    gcp_queue = GcpQueue()
    gcp_queue.publish(queue_message.topic, gcp_queue.to_queue_message(cloud_event))
