import pytest
from unittest.mock import MagicMock
from src.market import Market
from src.agent import RandomAgent, TrendAgent, CustomAgent

@pytest.fixture
def mock_market():
    """Provides a mock Market instance."""
    market = MagicMock(spec=Market)
    market.price = 100.0
    market.last_iterarion_price = 95.0
    market.stock = 50
    market.iteration = 0
    market.market_iteration_limit = 1000
    market.execute_action.return_value = True
    
    return market

@pytest.fixture
def random_agent():
    """Provides a RandomAgent instance."""
    return RandomAgent(name="RandomAgent", balance=1000.0)

@pytest.fixture
def trend_agent():
    """Provides a TrendAgent instance."""
    return TrendAgent(name="TrendAgent", balance=1000.0, trend_direction=1)

@pytest.fixture
def custom_agent():
    """Provides a CustomAgent instance."""
    agent = CustomAgent(name="CustomAgent", balance=1000.0)
    agent.position = 50
    return agent

def test_random_agent_act(mock_market, random_agent):
    """Test the RandomAgent act method performs an action without error."""
    random_agent.act(mock_market)
    assert random_agent.balance <= 1000.0 


def test_trend_agent_buy(mock_market, trend_agent):
    """Test TrendAgent when market price is trending upwards."""
    mock_market.last_iterarion_price = 90.0
    trend_agent.act(mock_market)
    assert trend_agent.balance <= 1000.0 


def test_trend_agent_sell(mock_market, trend_agent):
    """Test TrendAgent when market price is trending downwards."""
    mock_market.last_iterarion_price = 110.0
    trend_agent.act(mock_market)
    assert trend_agent.balance <= 1000.0 

# Custom Agent tests

def test_custom_agent_sell_due_to_iteration(mock_market, custom_agent):
    """Test CustomAgent SELL action when iteration matches graphics cards."""
    custom_agent.graphics_cards = 1
    mock_market.iteration = 999

    custom_agent.act(mock_market)
    assert custom_agent.graphics_cards == 0

def test_custom_agent_hold_due_to_iteration(mock_market, custom_agent):
    """Test CustomAgent HOLD action when iteration is graphics_cards + 1."""
    custom_agent.graphics_cards = 1
    mock_market.iteration = 998

    custom_agent.act(mock_market)
    assert custom_agent.graphics_cards == 1

def test_custom_agent_buy_due_to_price_trend(mock_market, custom_agent):
    """Test CustomAgent BUY action when price trends favor buying."""
    custom_agent.position = 100
    custom_agent.balance = 1000.0
    mock_market.price = 120.0
    mock_market.last_iterarion_price = 100.0
    mock_market.iteration = 50

    custom_agent.act(mock_market)
    assert custom_agent.graphics_cards == 1
    assert custom_agent.balance < 1000.0 

def test_custom_agent_sell_due_to_price_trend(mock_market, custom_agent):
    """Test CustomAgent SELL action when price trends favor selling."""
    custom_agent.position = 99
    custom_agent.graphics_cards = 1
    mock_market.price = 90.0
    mock_market.last_iterarion_price = 100.0

    custom_agent.act(mock_market)
    assert custom_agent.graphics_cards == 0
    assert custom_agent.balance >= 90 

def test_custom_agent_buy_in_early_iteration(mock_market, custom_agent):
    """Test CustomAgent BUY action in early iterations."""
    mock_market.price = 100.0
    mock_market.last_iterarion_price = 100.0
    custom_agent.position = 100
    mock_market.iteration = 2
    custom_agent.graphics_cards = 0
    custom_agent.balance = 1000

    custom_agent.act(mock_market)
    assert custom_agent.graphics_cards == 1
    assert custom_agent.balance < 1000.0 
