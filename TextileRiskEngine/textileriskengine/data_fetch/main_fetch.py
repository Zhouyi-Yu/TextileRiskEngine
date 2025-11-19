# TextileRiskEngine/textileriskengine/data_fetch/main_fetch.py

from fx_data import run as run_fx
from freight_data import run as run_freight
from trade_data import run as run_trade
from demand_data import run as run_demand


def main():
    tasks = [
        ("FX (World Bank)", run_fx),
        ("Freight (运费指数)", run_freight),
        ("Trade (UN Comtrade 纺织进口)", run_trade),
        ("Demand (电商价格/需求)", run_demand),
    ]

    for name, func in tasks:
        print("\n" + "=" * 60)
        print(f"▶ 开始执行：{name}")
        print("=" * 60)
        try:
            func()
            print(f"✅ 完成：{name}")
        except Exception as e:
            # 不要因为一个失败就退出，把错误打印出来继续下一个
            print(f"❌ 失败：{name}  — 错误：{e}")

    print("\n🎉 所有爬取任务已尝试执行完毕。请检查 data/raw/ 下的文件。")


if __name__ == "__main__":
    main()
