import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from app.config import settings
from app.database import SessionLocal
from app.services.scanner import Scanner

dramatiq.set_broker(RabbitmqBroker(url=settings.broker_uri))


@dramatiq.actor
def start_scan(_id: str):
    with SessionLocal() as session:
        scanner = Scanner(session, _id)
        scanner.start()
