import uuid
from typing import TypedDict
import structlog
from email_service import send_confirmation_email

# 1. Instantiate the logger
logger = structlog.get_logger()

# 2. Strong typing for data model
class Order(TypedDict):
    order_id: str
    customer_email: str
    total: float

def process_orders(orders: list[Order]) -> None:
    # 3. Generate a unique run ID for this pipeline execution
    run_id = str(uuid.uuid4())

    # 4. Clean previous context and bind run_id globally for this batch
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(run_id=run_id)

    # 5. Log batch start
    logger.info("batch_started", order_count=len(orders))

    for order in orders:
        order_id = order["order_id"]
        logger.info("email_send_started", order_id=order_id)

        try:
            send_confirmation_email(order["order_id"], order["customer_email"], order["total"])
            logger.info("email_send_succeeded", order_id=order_id)
        except Exception as e:
            # 6. Structured error log with exact context and error message
            logger.error("email_send_failed", order_id=order_id, error=str(e))

    # 7. Log batch completion
    logger.info("batch_finished")