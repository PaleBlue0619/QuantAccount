import pandas as pd
from src.entity.Model import Model
from typing import List, Dict, Callable, Tuple

class User:
    def __init__(self, user_name: str = None):
        # 系统属性
        self.user_name = user_name  # 用户名称
        self.pnl = 0.0  # 累计pnl
        self.asset = 0.0    # 累计总资产
        self.deposit = 0.0  # 累计入金
        self.withdraw = 0.0  # 累计出金
        self.asset_dict: Dict[pd.Timestamp, float] = {}
        self.deposit_dict: Dict[pd.Timestamp, float] = {}
        self.withdraw_dict: Dict[pd.Timestamp, float] = {}

        # 配置项
        self.model: Callable = Model.linear_ratio
        self.create_time: pd.Timestamp = None
        self.profit_share: float = 1.0
        self.loss_comp: float = 0.0
        self.fee_rate: float = 0.0

        # 日志项
        self.log: List[Dict[str, str]] = []

    # 对象行为绑定
    def init(self, cfg: Dict[str, any]):
        """用户初始化"""
        self.create_time: pd.Timestamp = cfg["create_time"]
        self.model: Callable = Model().__getattribute__(cfg["model"])
        self.profit_share = cfg["profit_share"]
        self.loss_comp = cfg["loss_comp"]
        self.fee_rate = cfg["fee_rate"]

    def onDeposit(self, amount: float, current_time: pd.Timestamp):
        """用户入金"""
        if amount <= 0:
            raise ValueError("入金金额需为正数")
        self.deposit += amount
        self.asset += amount
        self.log.append({"time": current_time, "oper": "deposit", "value": amount})

    def onWithdraw(self, amount: float, current_time: pd.Timestamp):
        """用户出金"""
        if amount <= 0:
            raise ValueError("出金金额需为正数")
        self.withdraw += amount
        self.asset -= amount
        self.log.append({"time": current_time, "oper": "withdraw", "value": amount})

    def onPnl(self, pnl: float, current_time: pd.Timestamp) -> Tuple[float, float]:
        to_pay, to_pnl = self.model(pnl=pnl, profit_share=self.profit_share,
                          loss_comp=self.loss_comp, fee_rate=self.fee_rate)
        self.pnl += to_pnl
        self.asset += to_pnl
        self.log.append({"time": current_time, "oper": "onPnl", "value": [to_pnl, to_pnl]})
        return to_pay, to_pnl

    def record(self, current_time: pd.Timestamp):
        """清算记录"""
        # if current_time in self.asset_dict:
        #     raise KeyError(f"asset_dict 已存在 {current_time}键值")
        # if current_time in self.deposit_dict:
        #     raise KeyError(f"deposit_dict 已存在 {current_time}键值")
        # if current_time in self.withdraw_dict:
        #     raise KeyError(f"withdraw_dict 已存在 {current_time}键值")
        self.asset_dict[current_time] = self.asset
        self.deposit_dict[current_time] = self.deposit
        self.withdraw_dict[current_time] = self.withdraw

