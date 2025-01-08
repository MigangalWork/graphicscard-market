import random

from src.market import Market
from src.agent import Agent


class MainLoop:
    """
    MainLoop coordinates the execution of iterations within a market, allowing agents to interact with it.
    """

    @classmethod
    def main_loop(cls, iterations: int, market: Market, agent_list: list):
        """
        Executes the main loop for a number of iterations,
        coordinating agent actions and updating the market state.

        Args:
            market (Market): The market object that tracks the state of the simulation.
            agent_list (list[Agent]): A list of agents participating in the market.
        """
        for _ in range(iterations):
            cls._run_iteration(market=market, agent_list=agent_list)
            market.new_iteration()

    @classmethod
    def _run_iteration(cls, market: Market, agent_list: list[Agent]):
        """
        Executes a single iteration where agents act in a randomized order.

        Args:
            market (Market): The market object.
            agent_list (list[Agent]): A list of agents participating in the market.
        """
        ordered_agents: list = random.sample(agent_list, len(agent_list))

        for pos, agent in enumerate(ordered_agents):
            agent.position = pos
            agent.act(market)
            