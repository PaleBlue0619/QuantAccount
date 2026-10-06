import pandas as pd
from src.entity.Account import Manager

if __name__ == "__main__":
    M = Manager()
    M.load_cfg(r".\src\cons\config.json5")
    daily_pnl = pd.read_csv(r".\src\record\dailyPnl.csv", index_col=None, header=0)
    behavior = pd.read_csv(r".\src\record\behavior.csv", index_col=None, header=0)
    print(M.config)
    M.replay(hist_pnl=daily_pnl, hist_behavior=behavior)
    log_file = M.state["lsf"].log
    for log in log_file:
        print(log)
    print(M.state["mxy"].asset_dict)
    print(M.state["lsf"].asset_dict)
    # print(M.state["mxy"].log)