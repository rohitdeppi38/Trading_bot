def validate_symbol(symbol: str) -> str:
    """Validate the trading symbol."""
    symbol = symbol.upper()
    if not symbol.isalnum():
        raise ValueError(f"Invalid symbol format: {symbol}. Must be alphanumeric.")
    if not symbol.endswith("USDT"):
        raise ValueError(f"Invalid symbol format: {symbol}. This bot requires USDT-M futures pairs (e.g., BTCUSDT).")
    return symbol

def validate_side(side: str) -> str:
    """Validate the order side."""
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Validate the order type."""
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET"]:
        raise ValueError(f"Invalid order type: {order_type}. Supported types: MARKET, LIMIT, STOP_MARKET.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Validate the order quantity."""
    if quantity <= 0:
        raise ValueError(f"Invalid quantity: {quantity}. Must be greater than 0.")
    return quantity

def validate_price(price: float, order_type: str) -> float:
    """Validate the order price."""
    if order_type.upper() == "LIMIT" and price <= 0:
        raise ValueError(f"Invalid price: {price}. Price must be greater than 0 for LIMIT orders.")
    return price

def validate_stop_price(stop_price: float, order_type: str) -> float:
    """Validate the stop price for STOP_MARKET orders."""
    if order_type.upper() == "STOP_MARKET" and stop_price <= 0:
        raise ValueError(f"Invalid stop price: {stop_price}. Stop price must be greater than 0 for STOP_MARKET orders.")
    return stop_price
