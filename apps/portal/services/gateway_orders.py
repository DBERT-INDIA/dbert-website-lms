"""Track the purchase agreed before checkout and bind it to one capture."""


class GatewayOrderError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def create_gateway_order_schema(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS gateway_payment_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL UNIQUE,
            intern_id INTEGER NOT NULL,
            product_type TEXT NOT NULL,
            product_id INTEGER,
            post_id INTEGER,
            course_title TEXT,
            amount_paise INTEGER NOT NULL CHECK (amount_paise > 0),
            currency TEXT NOT NULL,
            domain TEXT,
            joining_date TEXT,
            created_at TEXT NOT NULL,
            payment_id TEXT UNIQUE,
            settled_at TEXT
        )
    """)


def remember_gateway_order(conn, order_id, intern_id, purchase, now):
    conn.execute("""
        INSERT INTO gateway_payment_orders
        (order_id, intern_id, product_type, product_id, post_id, course_title, amount_paise,
         currency, domain, joining_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_id, intern_id, purchase["product_type"], purchase.get("product_id"),
        purchase.get("post_id"), purchase.get("course_title"), purchase["amount_paise"],
        purchase["currency"], purchase.get("domain"), purchase.get("joining_date"), now,
    ))


def get_gateway_order(conn, order_id, intern_id=None):
    query = "SELECT * FROM gateway_payment_orders WHERE order_id=?"
    params = (order_id,)
    if intern_id is not None:
        query += " AND intern_id=?"
        params = (order_id, intern_id)
    row = conn.execute(query, params).fetchone()
    if not row:
        raise GatewayOrderError("The payment order could not be matched to this purchase.", 404)
    return row


def validate_gateway_capture(order, capture, payment_id):
    if not isinstance(capture, dict) or (
        capture.get("id") != payment_id
        or capture.get("order_id") != order["order_id"]
        or type(capture.get("amount")) is not int
        or capture["amount"] != order["amount_paise"]
        or capture.get("currency") != order["currency"]
    ):
        raise GatewayOrderError("The captured payment does not match the expected order.", 409)
    if capture.get("status") != "captured":
        raise GatewayOrderError("The payment is awaiting capture. Check the payment status shortly.", 409)


def claim_gateway_capture(conn, order, capture, payment_id, now):
    """Lock the order and prevent two transactions from applying one capture."""
    validate_gateway_capture(order, capture, payment_id)
    claimed = conn.execute("""
        UPDATE gateway_payment_orders SET payment_id=?, settled_at=?
        WHERE id=? AND payment_id IS NULL
    """, (payment_id, now, order["id"]))
    if claimed.rowcount == 1:
        return True
    settled = get_gateway_order(conn, order["order_id"])
    if settled["payment_id"] == payment_id:
        return False
    raise GatewayOrderError("A different payment has already been settled for this order.", 409)
