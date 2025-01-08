from sqlalchemy.orm import sessionmaker

from src.db import ExecutionCase, MarketHistory, Transaction
from src.utils import Action, operation_sign


class Market:
    """
    The Market class models a market where agents can perform buy/sell actions, 
    and tracks stock, price, and transaction history.
    """
    def __init__(self, session_maker: sessionmaker,
                 initial_price: float, 
                 stock: int,
                 market_iteration_limit: int):
        """
        Initializes the market with the given parameters and sets up database logging.

        Args:
            session_maker (sessionmaker): A SQLAlchemy sessionmaker instance.
            initial_price (float): The initial price of the stock.
            stock (int): The initial stock quantity.
        """
        
        self.price: float = initial_price
        self.last_iterarion_price: float = initial_price
        self.stock: int = stock
        self.iteration: int = 0
        self.market_iteration_limit: int = market_iteration_limit

        self._market_changes: list = list()
        self._transactions: list = list()

        self.session = session_maker()
        self._start_market_in_db()

    def execute_action(self, action: str, agent_name: str) -> bool:
        """
        Executes a buy or sell action by an agent, adjusts stock and price, and logs the transaction.

        Args:
            action (str): The action to execute (e.g., BUY or SELL).
            agent_name (str): The name of the agent performing the action.

        Returns:
            bool: True if the action was successful, False otherwise.
        """
        if action == Action.BUY and self.stock == 0:
            return False

        self.stock = self.stock + operation_sign[action]
        self._adjust_price(change_percent=0.5 * -operation_sign[action])
        self._log_transaction(agent_name=agent_name, action=action)
        self._log_market_change()

        return True
    
    def new_iteration(self):
        """
        Advances the market to the next iteration, logs the current state, and resets transaction logs.
        """
        self.iteration += 1
        self.last_iterarion_price = self.price
        self._save_and_clear_logs()

    def _adjust_price(self, change_percent: float):
        self.price = round(self.price * (1 + change_percent / 100), 2)

    def _log_transaction(self, agent_name: str, action: str):
        """
        Logs a transaction in memory.

        Args:
            agent_name (str): The name of the agent.
            action (str): The action performed (e.g., BUY or SELL).
        """
        transaction_record: Transaction = Transaction(
                                            iteration=self.iteration,
                                            agent_name=agent_name,
                                            action=action.name,
                                            price=self.price,
                                            execution_case_id=self.market_id
                                        )
        self._transactions.append(transaction_record)

    def _log_market_change(self):
        """
        Logs a market state change in memory.
        """
        market_record: MarketHistory = MarketHistory(
                                      iteration=self.iteration, 
                                      price=self.price, 
                                      stock=self.stock,
                                      execution_case_id=self.market_id
                                      )
        self._market_changes.append(market_record)

    def _save_and_clear_logs(self):
        """
        Saves the logged transactions and market changes to the database, and clears the logs.
        """
        self.session.bulk_save_objects(self._market_changes)
        self.session.bulk_save_objects(self._transactions)
        self.session.commit()

        self._market_changes.clear()
        self._transactions.clear() 

    def _start_market_in_db(self):
        """
        Initializes a new execution case in the database and retrieves its ID.
        """
        new_execution_case = ExecutionCase()
        self.session.add(new_execution_case)
        self.session.commit()
        self.market_id = new_execution_case.id
