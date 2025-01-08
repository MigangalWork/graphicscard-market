import random

from src.market import Market
from src.agent import Agent


class MainLoop:

    @classmethod
    def main_loop(cls, market: Market, agent_list: list):
        for _ in range(1000):
            cls._run_iteration(market=market, agent_list=agent_list)
            market.new_iteration()

    @classmethod
    def _run_iteration(cls, market: Market, agent_list: list[Agent]):
        ordered_agents: list = random.sample(agent_list, len(agent_list))

        for pos, agent in enumerate(ordered_agents):
            agent.position = pos
            agent.act(market)
            