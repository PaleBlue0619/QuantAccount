import pandas as pd
from src.entity.User import User
from src.entity.Model import Model
from typing import Dict, Callable

class Admin(User):
    def __init__(self, user_name: str):
        super(Admin, self).__init__(user_name=user_name)

    def onPnl(self, pnl: float, current_time: pd.Timestamp) -> None:
        self.pnl += pnl
        self.asset += pnl
        self.log.append({"time": current_time, "oper": "onPnl", "value": pnl})

    def receive(self, amount: float, current_time: pd.Timestamp, user_name: str):
        """收到用户的钱(amount>0)/补偿用户(amount<0)"""
        self.asset += amount
        self.pnl += amount
        self.log.append({"time": current_time, "oper": "receive", "from": user_name, "value": amount})
