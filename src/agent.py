import random
from typing import Literal, Optional
from src.market import Market
from src.utils import Action, operation_sign

class Agent:
    def __init__(self, name: str, balance: float):
        self.name: str = name
        self.balance: float = balance
        self.graphics_cards: int = 0
        self.position: Optional[int] = None
    
    def _base_act(self, action: Action, market: Market):
        if action == Action.HOLD:
            return
        elif action == Action.BUY and self.balance < market.price:
            return
        elif action == Action.SELL and self.graphics_cards < 1:
            return
        
        execution_ok: bool = market.execute_action(action=action, agent_name=self.name)

        if not execution_ok:
            return

        self.balance = self.balance + (market.price * operation_sign[action])
        self.graphics_cards = self.graphics_cards - operation_sign[action]

    def act(self, market: Market):
        raise NotImplementedError
    

class RandomAgent(Agent):
    def act(self, market: Market):
        action: Action = random.choice([Action.BUY, Action.SELL, Action.HOLD])
        self._base_act(action=action, market=market)

class TrendAgent(Agent):
    def __init__(self, name: str, balance: float, trend_direction: Literal[1, -1]):
        super().__init__(name, balance)
        if trend_direction not in [1, -1]:
            raise ValueError('Direction must be either  "1" or "-1"')
        
        self.trend_direction = trend_direction

    def act(self, market: Market):
        if market.price >= market.last_iterarion_price * (1 + self.trend_direction * 0.01):
            action = random.choices([Action.BUY, Action.HOLD], weights=[75, 25], k=1)[0]
        else:
            action = random.choices([Action.SELL, Action.HOLD], weights=[20, 80], k=1)[0]
    
        self._base_act(action=action, market=market)

class CustomAgent(Agent):
    def __init__(self, name: str, balance: float):
        super().__init__(name, balance)
        self.max_buy_price: int = 0

    def act(self, market: Market):

        if market.iteration == self.graphics_cards:
            action = Action.SELL

        elif market.iteration == self.graphics_cards + 1:
            action = Action.HOLD

        elif market.price >= market.last_iterarion_price * (1 + 0.01) or \
        market.price >= market.last_iterarion_price * (1 - 0.01):

            if random.randint(0,100) < self.position and self.balance <= market.price:
                action = Action.BUY
            elif self.graphics_cards > 0:
                action = Action.SELL
            else:
                action = Action.HOLD

        elif random.randint(0,100) > self.position and self.balance <= market.price:
                action = Action.BUY

        elif self.max_buy_price * 1.7 < market.price and self.graphics_cards > 0:
            action = Action.SELL

        elif self.max_buy_price * 1.1 < market.price and self.graphics_cards > 0 and self.balance <= market.price:
            action = Action.SELL

        elif market.iteration < 4:
            action = Action.BUY
        else:
            action = Action.HOLD

        if action == Action.BUY:
            self.max_buy_price = max(self.max_buy_price, market.price)

        self._base_act(action=action, market=market)
        