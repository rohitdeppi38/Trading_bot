# pyrefly: ignore [missing-import]
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from bot.client import get_binance_client
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_stop_price,
)
from bot.orders import place_order
from bot.logging_config import setup_logger

app = typer.Typer(help="Simplified Binance Futures Testnet Trading Bot")
console = Console()
logger = setup_logger(__name__)

@app.command()
def place(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET, LIMIT, or STOP_MARKET"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT orders)"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop Price (Required for STOP_MARKET orders)")
):
    """
    Place an order on the Binance Futures Testnet.
    """
    try:
        # Validate inputs
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        
        if order_type == "LIMIT":
            price = validate_price(price, order_type)
        elif order_type == "STOP_MARKET":
            stop_price = validate_stop_price(stop_price, order_type)

    except ValueError as e:
        logger.error(f"Input validation error: {e}")
        console.print(Panel(f"[bold red]Validation Error:[/bold red] {e}", title="Error"))
        raise typer.Exit(code=1)

    # Show Order Request Summary
    req_table = Table(title="Order Request Summary", show_header=False)
    req_table.add_row("Symbol", symbol)
    req_table.add_row("Side", f"[bold {'green' if side == 'BUY' else 'red'}]{side}[/]")
    req_table.add_row("Type", order_type)
    req_table.add_row("Quantity", str(quantity))
    if price:
        req_table.add_row("Price", str(price))
    if stop_price:
        req_table.add_row("Stop Price", str(stop_price))
    
    console.print(req_table)
    console.print("\n[yellow]Connecting to Binance Testnet...[/yellow]")

    try:
        client = get_binance_client()
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        # Show Success Details
        console.print(Panel("[bold green]Order Placed Successfully![/bold green]", border_style="green"))
        
        resp_table = Table(title="Order Response Details")
        resp_table.add_column("Field", style="cyan")
        resp_table.add_column("Value", style="magenta")
        
        resp_table.add_row("Order ID", str(response.get('orderId')))
        resp_table.add_row("Status", str(response.get('status')))
        resp_table.add_row("Executed Qty", str(response.get('executedQty', 0)))
        
        # In futures API, avgPrice is returned.
        avg_price = response.get('avgPrice', 0)
        resp_table.add_row("Avg Price", str(avg_price))
        
        console.print(resp_table)

    except Exception as e:
        # Errors are already logged in the respective modules
        console.print(Panel(f"[bold red]Failed to place order:[/bold red]\n{e}", title="API Error", border_style="red"))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
