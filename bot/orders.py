from typing import Optional, Dict, Any
# pyrefly: ignore [missing-import]
from binance.client import Client
# pyrefly: ignore [missing-import]
from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logging_config import setup_logger

logger = setup_logger(__name__)

def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Core function to place an order on Binance Futures Testnet.
    Returns the order response dictionary.
    """
    logger.info(f"Requesting to place {order_type} order for {quantity} {symbol} ({side})")
    
    # Common parameters for all orders
    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
    }

    if order_type == 'LIMIT':
        if not price:
            raise ValueError("Price is required for LIMIT orders.")
        params['price'] = price
        params['timeInForce'] = 'GTC' # Good Till Cancelled is required for LIMIT orders
        
    elif order_type == 'STOP_MARKET':
        if not stop_price:
            raise ValueError("Stop price is required for STOP_MARKET orders.")
        params['stopPrice'] = stop_price

    try:
        # We must use futures_create_order for Futures Testnet
        response = client.futures_create_order(**params)
        logger.info(f"Successfully placed {order_type} order. OrderID: {response.get('orderId')}")
        logger.debug(f"Full Order Response: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception while placing order: {e.status_code} - {e.message}")
        raise
    except BinanceOrderException as e:
        logger.error(f"Binance Order Exception while placing order: {e.status_code} - {e.message}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while placing order: {e}")
        raise
