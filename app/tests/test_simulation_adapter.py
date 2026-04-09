import pytest

from app.infrastructure.adapters import NormalizedOrderRequest, SimulationAdapter


@pytest.mark.asyncio
async def test_simulation_adapter_places_and_streams_fill() -> None:
    adapter = SimulationAdapter()
    response = await adapter.place_order(
        NormalizedOrderRequest(
            account_id="acct-1",
            symbol="BTC-USD",
            side="buy",
            quantity=1.0,
            price=100.0,
        )
    )
    assert response.status == "filled"

    updates = await adapter.stream_order_updates()
    assert any(update.order_id == response.order_id for update in updates)
