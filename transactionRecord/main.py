# main.py

from src.csv_parser import parse_zfb_csv
from src.csv_parser import parse_wx_csv
import os
import openpyxl  # 导入 openpyxl 库，用于处理 Excel 文件
from rich.console import Console
from datetime import datetime
from rich.table import Table
from collections import defaultdict

def main():
    home_directory = os.path.expanduser("~");
    print(home_directory)
    handle_wx_excel(home_directory + '/Downloads/8月账单/')
    handle_zfb_excel('/Users/zhoust/Downloads/8月账单/')

def handle_zfb_excel(path):
    file_path = path + 'Me支付宝.csv'
    my_zfb_tx_list = parse_zfb_csv(file_path, "Me支付宝 ")
    file_path = path + 'Wife支付宝.csv'
    wife_zfb_tx_list = parse_zfb_csv(file_path, "Wife支付宝 ")

    all_zfb_tx_list = sorted(my_zfb_tx_list + wife_zfb_tx_list, key=lambda tx: -tx.amount)
    xlsx_export(path + "账单合并-支付宝.xlsx", all_zfb_tx_list)

def handle_wx_excel(path):
    file_path = path + 'Me微信支付账单.csv'
    my_wx_transaction_list = parse_wx_csv(file_path, 'MeWeChat ')
    file_path = path + 'Wife微信支付账单.csv'
    wife_wx_transaction_list = parse_wx_csv(file_path, 'WifeWeChat ')
    
    transaction_list = merge_wx_tx(wife_wx_transaction_list, my_wx_transaction_list)
    sorted_transactions = sorted(transaction_list, key=lambda tx: -tx.amount)
    
    export_wx_file = path + '账单合并-wx.xlsx'
    xlsx_export(export_wx_file, sorted_transactions)

def merge_wx_tx(wife_wx_tx_list, my_wx_tx_list):
    # 合并两个交易列表，过滤掉我交易列表中的 "亲属卡交易"
    return wife_wx_tx_list + list(filter(lambda tx : tx.is_family_card() == False, my_wx_tx_list))

def xlsx_export(file_path, tx_data_array):
    workbook = openpyxl.Workbook()

    # 获取工作簿中的活动工作表（默认是第一个工作表）
    sheet = workbook.active

    # 写入表头
    sheet['A1'] = '日期'
    sheet['B1'] = '消费类型'
    sheet['C1'] = '消费方式'
    sheet['D1'] = '金额'
    sheet['E1'] = '备注'

    # 写入数据
    for row_idx, tx in enumerate(tx_data_array, start=2):  # 遍历数据，从第二行开始写入
        sheet.cell(row=row_idx, column=1, value=tx.date)
        sheet.cell(row=row_idx, column=2, value=tx.consume_type())
        sheet.cell(row=row_idx, column=3, value=tx.consume_way)
        sheet.cell(row=row_idx, column=4, value=tx.amount)
        sheet.cell(row=row_idx, column=5, value=tx.note)

    # 保存工作簿到文件
    workbook.save(file_path)

if __name__ == "__main__":
    main()
