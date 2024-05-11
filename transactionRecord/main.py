# main.py

from src.csv_parser import parse_zfb_csv
from src.csv_parser import parse_wx_csv
import heapq
from rich.console import Console
from datetime import datetime
from rich.table import Table
from collections import defaultdict

def main():
    file_path = 'data/alipay_34月份账单.csv'
    zfb_transaction_list = parse_zfb_csv(file_path)
    file_path = 'data/wx_34月份账单.csv'
    wx_transaction_list = parse_wx_csv(file_path)

    transaction_list = zfb_transaction_list + wx_transaction_list

    sorted_transactions = sorted(transaction_list, key=lambda record: record.date)

    print(len(sorted_transactions))

    # 创建控制台实例
    console = Console()
    table = Table(show_header=True)
    table.add_column("类型")
    table.add_column("支出总额")
    table.add_column("支出Top7")

    # 按支出类型分组，val 是列表
    dif_type_map = defaultdict(list)

    for transaction in sorted_transactions:
        if transaction.transaction_type == '收入':
             continue
        dif_type_map[transaction.expend_type].append(transaction)

    # 遍历字典的键值对
    for expend_type, value_list in dif_type_map.items():
        total_expense = sum(transaction.amount for transaction in value_list)
        top_7 = heapq.nlargest(15, value_list, key=lambda _v: _v.amount)
        num = 1
        for top in top_7:
            if num == 1:
                table.add_row(str(expend_type), str(f"{total_expense:.2f}"), str(top))
                num += 1
                continue
            table.add_row('', '', str(top))

    console.print(table)
if __name__ == "__main__":
    main()
