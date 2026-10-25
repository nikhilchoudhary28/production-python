"""A simulated email delivery service. You don't need to edit this
file. One specific order is designed to fail, deterministically, so
you have something real to diagnose.
"""


def send_confirmation_email(order_id: str, customer_email: str, total: float) -> None:
    # ORD-1003 always fails, simulating a real delivery problem -
    # a bounced address, a full inbox, whatever the real cause might be.
    if order_id == "ORD-1003":
        raise RuntimeError("SMTP delivery failed: mailbox unavailable")
