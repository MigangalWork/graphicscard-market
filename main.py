import configparser

from src.agent import Agent, CustomAgent, RandomAgent, TrendAgent
from src.main_loop import MainLoop
from src.market import Market
from src.db import session_maker


def create_agents(config) -> list[Agent]:

    agent_list: list = list()
    for i in range(int(config['agents']['random_agents'])):
        agent_list.append(RandomAgent(name=f"Random_{i+1}", balance=int(config['agents']['balance'])))

    for i in range(int(config['agents']['follow_trend_agents'])):
        agent_list.append(TrendAgent(name=f"Trend_{i+1}", trend_direction=1, balance=int(config['agents']['balance'])))

    for i in range(int(config['agents']['counter_trend_agents'])):
        agent_list.append(TrendAgent(name=f"Counter_{i+1}", trend_direction=-1, balance=int(config['agents']['balance'])))

    agent_list.append(CustomAgent(name="CustomAgent", balance=int(config['agents']['balance'])))

    return agent_list


if __name__ == "__main__":
    print(' ---- Program started ---- ')
    config = configparser.ConfigParser()
    config.read("config.conf")
    market: Market = Market(session_maker=session_maker, 
                    initial_price=float(config['market']['initial_price']),
                    stock=int(config["market"]['initial_stock']),
                    market_iteration_limit=int(config['market']['iterations']))
    
    agent_list: list = create_agents(config=config)
    MainLoop.main_loop(iterations=int(config['market']['iterations']), market=market, agent_list=agent_list)

    for agent in agent_list:
        print(f"{agent.name}: Balance = ${agent.balance:.2f}, Cards = {agent.graphics_cards}")
