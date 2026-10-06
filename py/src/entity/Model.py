from typing import Tuple

class Model:
    """
    资金转移算法:
    返回的值有二,
    第一个值为用户需要支付给资金管理员多少的费用
        为正：用户需要向管理员支付的资金费用
        为0：没有资金转移
        为负: 管理员需要向用户支付的资金费用
    第二个值为用户自身获得的pnl
        为正：用户得到的pnl
        为0：不赚不亏
        为负：用户需要扣除的pnl
    """
    @staticmethod
    def linear_ratio(pnl: float, profit_share: float, loss_comp: float, fee_rate: float) -> Tuple[float, float]:
        val_1 = 0.0
        val_2 = 0.0

        # case-1: 亏钱场景
        if pnl < 0 and loss_comp == 0:
            val_1 = 0.0
            val_2 = -abs(pnl)
        if pnl < 0 and loss_comp > 0:
            val_1 = -abs(pnl * loss_comp)
            val_2 = -abs(pnl) + val_1

        # case-2: 赚钱场景
        if pnl > 0:
            val_1 = int(pnl * (1-profit_share + fee_rate))
            val_2 = pnl-val_1
        return val_1, val_2