import json, json5
import pandas as pd
from src.entity.User import User
from src.entity.Admin import Admin
from src.entity.Model import Model
from typing import Dict, Optional

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
    def __init__(self):
        self.config: Dict[str, any] = {}
        self.state: Dict[str, User] = {}    # 用户名称: 用户对象
        self.weight: Dict[str, float] = {}  # 用户名称: 仓位权重(每期按照每个user的deposit - withdraw - pnl的val重新分配权重)
        self.admin: Admin = Admin("")
        self.model: Model = Model()

    def load_cfg(self, json_path: str) -> None:
        """加载系统配置"""
        with open(json_path, "r", encoding="utf-8") as f:
            cfg = json5.load(f)
        self.config = cfg
        for name, d in self.config["user"].items():
            if d["admin"]:  # 初始化管理员对象
                self.admin: Admin = Admin(user_name=name)
                self.state[name] = self.admin
            else:   # 初始化用户对象
                user = User(user_name=name)
                user.init(cfg=d)
                self.state[name] = user

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

    def rebalance(self) -> Dict[str, float]:
        """重新计算权重"""
        weight_dict: Dict[str, float] = {}
        for user_name in self.state.keys():
            user: Optional[User, Admin] = self.state[user_name]
            weight_dict[user_name] = user.deposit - user.withdraw - user.pnl
        weight_sum = sum(weight_dict.values())
        return {i: weight_dict[i] / weight_sum for i in weight_dict.keys()}

    def replay(self, hist_pnl: pd.DataFrame, hist_behavior: pd.DataFrame):
        """
        输入历史净值 + 历史用户行为 -> 回放计算每个用户的pnl
        原则: 先回放User & Admin 的oper 再算根据上一期的权重计算Pnl -> 再
        """
        # step1. lj(hist_pnl, hist_behavior)
        data = pd.merge(hist_pnl, hist_behavior, how="left", on=["date"])

        # step2. for loop
        last_time: pd.Timestamp = None
        for _, row in data.iterrows():
            # 基本信息
            current_time = pd.Timestamp(row["date"])
            user_name = row["user"]
            total_pnl = row["pnl"]
            user = self.state[user_name]
            oper = row["oper"]
            # step1. 执行oper
            amount = float(row["value"])
            if oper == "deposit":
                user.onDeposit(amount=amount)
            elif oper == "withdraw":
                user.onWithdraw(amount=amount)

            # step2. 分配资金权重
            if last_time != current_time: # 时间发生了变更
                self.weight = self.rebalance()
                last_time = current_time

            # step 3.-> 进入分支
            # 分支-1: admin
            if user_name == self.admin.user_name:   # 该用户为管理员
                # 3.1 直接分配 pnl
                self.admin.onPnl(pnl=total_pnl * self.weight[user_name])
                continue

            # 分支-2: user
            # 3.2 分配 pnl -> 转移 pnl
            to_pay, _ = user.onPnl(pnl=total_pnl * self.weight[user_name])
            self.admin.receive(amount=to_pay)