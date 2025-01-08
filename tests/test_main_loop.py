import pytest
from unittest.mock import MagicMock
from src.market import Market
from src.agent import Agent
from src.main_loop import MainLoop

def test_main_loop():
    """
    Test that the main_loop method executes and updates the market state.
    """
    mock_market = MagicMock(spec=Market)
    mock_agent = MagicMock(spec=Agent)
    agent_list = [mock_agent for _ in range(10)]

    MainLoop.main_loop(iterations=1000, market=mock_market, agent_list=agent_list)

    assert mock_market.new_iteration.call_count == 1000
    assert mock_agent.act.call_count == 1000 * len(agent_list)

def test_run_iteration():
    """
    Test that the _run_iteration method assigns positions and calls agent.act.
    """
    mock_market = MagicMock(spec=Market)
    mock_agents = [MagicMock(spec=Agent) for _ in range(5)]

    MainLoop._run_iteration(market=mock_market, agent_list=mock_agents)

    for i, agent in enumerate(mock_agents):
        assert agent.position is not None
        agent.act.assert_called_once_with(mock_market)
