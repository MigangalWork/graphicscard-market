# Test cases
@pytest.fixture
def setup_market():
    market = Market(initial_price=200.00, stock=100)
    agent1 = RandomAgent("Agent1")
    agent2 = TrendFollowingAgent("Agent2")
    agent3 = CounterTrendAgent("Agent3")
    agent4 = CustomAgent("Agent4")

    market.add_agent(agent1)
    market.add_agent(agent2)
    market.add_agent(agent3)
    market.add_agent(agent4)

    return market

def test_initial_conditions(setup_market):
    market = setup_market
    assert market.price == 200.00
    assert market.stock == 100
    assert len(market.agents) == 4

def test_random_agent_buy(setup_market):
    market = setup_market
    agent = RandomAgent("TestAgent", balance=300)
    market.add_agent(agent)

    agent.act(market)
    assert (agent.graphics_cards > 0 and agent.balance < 300) or (agent.graphics_cards == 0)

def test_trend_following_agent_act(setup_market):
    market = setup_market
    agent = TrendFollowingAgent("TestTrend", balance=300)
    market.add_agent(agent)

    market.price = 202.00
    agent.last_price = 200.00
    agent.act(market)
    assert (agent.graphics_cards > 0 and agent.balance < 300) or (agent.graphics_cards == 0)

def test_counter_trend_agent_act(setup_market):
    market = setup_market
    agent = CounterTrendAgent("TestCounter", balance=300)
    market.add_agent(agent)

    market.price = 198.00
    agent.last_price = 200.00
    agent.act(market)
    assert (agent.graphics_cards > 0 and agent.balance < 300) or (agent.graphics_cards == 0)

def test_custom_agent_act(setup_market):
    market = setup_market
    agent = CustomAgent("TestCustom", balance=300)
    market.add_agent(agent)

    market.price = 210.00
    agent.act(market)
    assert (agent.graphics_cards > 0 and agent.balance < 300) or (agent.graphics_cards == 0)

def test_run_iteration(setup_market, monkeypatch):
    market = setup_market

    # Mock database session methods
    market.session.bulk_save_objects = MagicMock()
    market.session.commit = MagicMock()

    # Run one iteration
    market.run_iteration()

    # Verify database interactions
    market.session.bulk_save_objects.assert_called()
    market.session.commit.assert_called()

    # Verify changes in iteration count
    assert market.iteration == 1

    # Verify market changes and transactions are cleared
    assert len(market.market_changes) == 0
    assert len(market.transactions) == 0