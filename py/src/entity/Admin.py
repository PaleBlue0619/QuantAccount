import pandas as pd
from src.entity.User import User
from src.entity.Model import Model
from typing import Dict, Callable

class Admin(User):
    def __init__(self, user_name: str):
        super(Admin, self).__init__(user_name=user_name)

    def receive(self, amount: float):
        """收到用户的钱(amount>0)/补偿用户(amount<0)"""
        self.asset += amount
        self.pnl += amount
