from sqlalchemy.orm import sessionmaker

from src.db import ExecutionCase, MarketHistory, Transaction
from src.utils import Action, operation_sign


class Market:
    def __init__(self, session_maker: sessionmaker,
                 initial_price: float, 
                 stock: int):
        
        self.price: float = initial_price
        self.last_iterarion_price: float = initial_price
        self.stock: int = stock
        self.iteration: int = 0

        self._market_changes: list = list()
        self._transactions: list = list()

        self.session = session_maker()
        self._start_market_in_db()

    def execute_action(self, action: str, agent_name: str) -> bool:
        if action == Action.BUY and self.stock == 0:
            return False

        self.stock = self.stock + operation_sign[action]
        self._adjust_price(change_percent=0.5 * operation_sign[action])
        self._log_transaction(agent_name=agent_name, action=action)
        self._log_market_change()

        return True
    
    def new_iteration(self):
        self.iteration += 1
        self.last_iterarion_price = self.price
        self._save_logs()

    def _adjust_price(self, change_percent: float):
        self.price *= (1 + change_percent / 100)

    def _log_transaction(self, agent_name: str, action: str):
        transaction_record: Transaction = Transaction(
                                            iteration=self.iteration,
                                            agent_name=agent_name,
                                            action=action.name,
                                            price=self.price,
                                            execution_case_id=self.market_id
                                        )
        self._transactions.append(transaction_record)

    def _log_market_change(self):
        market_record: MarketHistory = MarketHistory(
                                      iteration=self.iteration, 
                                      price=self.price, 
                                      stock=self.stock,
                                      execution_case_id=self.market_id
                                      )
        self._market_changes.append(market_record)

    def _save_logs(self):
        self.session.bulk_save_objects(self._market_changes)
        self.session.bulk_save_objects(self._transactions)
        self.session.commit()

        self._market_changes.clear()
        self._transactions.clear() 

    def _start_market_in_db(self):
        new_execution_case = ExecutionCase()
        self.session.add(new_execution_case)
        self.session.commit()
        self.market_id = new_execution_case.id
