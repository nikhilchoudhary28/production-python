import structlog
from notifier import Order, process_orders

# Configure structlog processors before pipeline execution
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,          # Merges run_id into every log line
        structlog.processors.TimeStamper(fmt="iso"),       # Adds UTC ISO-8601 timestamp
        structlog.processors.JSONRenderer(),               # Outputs logs as JSON lines
    ]
)

ORDERS: list[Order] = [
    {"order_id": "ORD-1001", "customer_email": "asha@example.com", "total": 42.50},
    {"order_id": "ORD-1002", "customer_email": "wei@example.com", "total": 18.00},
    {"order_id": "ORD-1003", "customer_email": "farid@example.com", "total": 91.20},
    {"order_id": "ORD-1004", "customer_email": "priya@example.com", "total": 12.75},
    {"order_id": "ORD-1005", "customer_email": "diego@example.com", "total": 63.40},
]

if __name__ == "__main__":
    process_orders(ORDERS)