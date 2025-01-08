import pytest
from unittest.mock import MagicMock
from src.utils import Action, operation_sign
from src.market import Market

@pytest.fixture
def mock_sessionmaker():
    """Provides a mock sessionmaker."""
    mock_session = MagicMock()
    mock_sessionmaker = MagicMock(return_value=mock_session)
    return mock_sessionmaker

@pytest.fixture
def market(mock_sessionmaker):
    """Creates a Market instance with mocked sessionmaker."""
    return Market(session_maker=mock_sessionmaker, 
                  initial_price=100.0, 
                  stock=50,
                  market_iteration_limit=1000)

def test_market_initialization(mock_sessionmaker):
    """Test the initialization of the Market class."""
    market = Market(session_maker=mock_sessionmaker, 
                    initial_price=100.0, 
                    stock=50,
                    market_iteration_limit=1000)

    assert market.price == 100.0
    assert market.last_iterarion_price == 100.0
    assert market.stock == 50
    assert market.iteration == 0
    mock_sessionmaker().add.assert_called_once()
    mock_sessionmaker().commit.assert_called_once()

def test_execute_action_buy_success(market):
    """Test executing a successful BUY action."""
    result = market.execute_action(action=Action.BUY, agent_name="Agent1")

    assert result is True
    assert market.stock == 49
    assert market.price > 100.0  # Price should increase
    assert len(market._transactions) == 1
    assert len(market._market_changes) == 1

def test_execute_action_sell_success(market):
    """Test executing a successful SELL action."""
    result = market.execute_action(action=Action.SELL, agent_name="Agent1")

    assert result is True
    assert market.stock == 51
    assert market.price < 100.0  # Price should decrease
    assert len(market._transactions) == 1
    assert len(market._market_changes) == 1

def test_execute_action_buy_failure(market):
    """Test executing a BUY action when stock is zero."""
    market.stock = 0
    result = market.execute_action(action=Action.BUY, agent_name="Agent1")

    assert result is False
    assert market.stock == 0
    assert len(market._transactions) == 0
    assert len(market._market_changes) == 0

def test_new_iteration(market):
    """Test advancing to a new iteration."""
    market.price = 120.0
    market.new_iteration()

    assert market.iteration == 1
    assert market.last_iterarion_price == 120.0
    market.session.bulk_save_objects.assert_called()
    market.session.commit.assert_called()

def test_adjust_price(market):
    """Test adjusting the market price."""
    market._adjust_price(change_percent=10.0)
    assert round(market.price, 2) == 110.00  # 10% increase

    market._adjust_price(change_percent=-10.0)
    assert round(market.price, 2) == 99.00  # 10% decrease

def test_log_transaction(market):
    """Test logging a transaction."""
    market._log_transaction(agent_name="Agent1", action=Action.BUY)

    assert len(market._transactions) == 1
    transaction = market._transactions[0]
    assert transaction.agent_name == "Agent1"
    assert transaction.action == Action.BUY.name

def test_log_market_change(market):
    """Test logging a market change."""
    market._log_market_change()

    assert len(market._market_changes) == 1
    market_change = market._market_changes[0]
    assert market_change.price == market.price
    assert market_change.stock == market.stock

def test_save_and_clear_logs(market):
    """Test saving logs to the database."""
    market._log_transaction(agent_name="Agent1", action=Action.BUY)
    market._log_market_change()

    market._save_and_clear_logs()

    market.session.bulk_save_objects.assert_called()
    market.session.commit.assert_called()
    assert len(market._transactions) == 0
    assert len(market._market_changes) == 0
