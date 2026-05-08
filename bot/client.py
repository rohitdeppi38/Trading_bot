import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from .logging_config import setup_logger

logger = setup_logger(__name__)

def get_binance_client() -> Client:
    """
    Initializes and returns a Binance Client connected to the Futures Testnet.
    """
    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        error_msg = "BINANCE_API_KEY and BINANCE_API_SECRET must be set in environment variables or .env file."
        logger.error(error_msg)
        raise ValueError(error_msg)

    try:
        # Initialize the client. testnet=True configures it to use testnet endpoints.
        client = Client(api_key, api_secret, testnet=True)
        
        # We need to test the connection by getting account info or pinging.
        # Since this is a testnet, ping is a safe operation.
        client.futures_ping()
        logger.info("Successfully connected to Binance Futures Testnet.")
        
        return client
    except BinanceAPIException as e:
        logger.error(f"Binance API Error during initialization: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error initializing Binance client: {e}")
        raise
