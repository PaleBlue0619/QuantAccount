import pandas as pd
from src.entity.User import User
from src.entity.Account import Manager

if __name__ == "__main__":
    M = Manager()
    M.load_cfg(r".\src\cons\config.json5")
    daily_pnl = pd.read_csv(r".\src\record\dailyPnl.csv", index_col=None, header=0)
    behavior = pd.read_csv(r".\src\record\behavior.csv", index_col=None, header=0)
    print(M.config)
    M.replay(hist_pnl=daily_pnl, hist_behavior=behavior)
    print(M.state["i"].__dict__)
    print(M.state["me"].__dict__)
    print(M.state["aligatou"].__dict__)