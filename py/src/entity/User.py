import pandas as pd

class User:
    def __init__(self, user_name: str):
        self.user_name = user_name  # 用户名称
        self.pnl = 0.0  # 累计pnl
        self.total_asset = 0.0 # 累计总资产
        self.deposit = 0.0  # 累计入金
        self.withdraw = 0.0  # 累计出金

    # 对象行为绑定
    def deposit(self, amount: float):
        """用户入金"""
        if amount <= 0:
            raise ValueError("入金金额需为正数")
        self.deposit += amount
        self.total_asset += amount

    def withdraw(self, amount: float):
        """用户出金"""
        if amount <= 0:
            raise ValueError("出金金额需为正数")
        self.withdraw += amount
        self.total_asset -= amount
