import json, json5
import pandas as pd
from src.entity.User import User
from typing import Dict

class Manager:
    """
    业务口径:
        - 所有用户共享同一份 pnl.csv
        - 总资产 = 入金 - 出金 + 累计净 PnL
        - 用户状态字段：
            net_value：净值
            total_asset：总资产
            pnl：累计净盈亏
            deposit：累计入金
            withdraw：累计出金
            last_settled_time：已经结算到的时间
    """
    def __init__(self, config: Dict[str, any] = None, state: Dict[str, User] = None):
        self.config = config
        self.state = state

    def load_cfg(self, json_path: str) -> None:
        """加载系统配置"""
        with open(json_path, "r", encoding="utf-8") as f:
            cfg = json5.load(f)
        self.config = cfg

    def persist_cfg(self, json_path: str) -> None:
        """配置项用户状态"""
        with open(json_path, "w", encoding="utf-8") as f:
            json5.dump(self.config, f)

    def load_state(self, json_path: str) -> None:
        """加载用户状态"""
        with open(json_path, "r", encoding="utf-8") as f:
            state = json5.load(f)
        self.state = state

    def persist_state(self, json_path: str) -> None:
        """持久化用户状态"""
        with open(json_path, "w", encoding="utf-8") as f:
            json5.dump(self.state, f)

    def deposit(self, user_name: str, amount: float):
        """
        用户入金: 总资产+=金额，不改变pnl
        """
        user: User = self.state[user_name]
        user.deposit(amount=amount)

    def withdraw(self, user_name: str, amount: float):
        """
        用户出金：总资产-=金额，不改变pnl
        """
        user: User = self.state[user_name]
        user.withdraw(amount=amount)

    def replay(self, hist_pnl: pd.DataFrame, hist_behavior: pd.DataFrame):
        """
        输入历史净值 + 历史用户行为 -> 回放计算每个用户的pnl
        """
        for _,row in hist_pnl:
