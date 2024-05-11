# src/csv_parser.py

import csv
import traceback
from datetime import datetime
from .transaction_record import TransactionRecord

def parse_zfb_csv(file_path):
    # 交易号(0)、商家订单号、交易创建时间、付款时间(3)、最近修改时间、交易来源地、类型、交易对方(7)、商品名称、金额(9)、收/支、交易状态、服务费、成功退款(13)、备注(14)、资金状态
    # 类型：将支付宝原来的即时到账、支付宝担保交易啥的，手动改成了 餐饮、购物、大额支出、房租、水电网费、出行、医疗、其他
    # 收/支：有一项是不计收支，包括余额宝收益、转出银行卡、退款、基金买入卖出等
    # 有退款的可以从成功退款列（index=13）计算
    
    # 如何做到分类统计支出？餐饮、购物、大额支出、房租、水电网费、出行、医疗、其他
    # 餐饮关键字："餐饮"、"饭"、"厨房"、"食堂"、"辣子王"、
    # 购物关键字：
    # 出行关键字："打车"、
    # 水电网费关键字：
    transactions = []
    with open(file_path, 'r', encoding='gb18030') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # 过滤前后几行与标题列
            if any(cell == '' for cell in row):
                continue
            if "交易号" in row[0].strip():
                continue

            try:
                transaction_type = row[10].strip()
                if transaction_type == "不计收支":
                    continue

                date = datetime.strptime(row[2].strip(), '%Y/%m/%d %H:%M')
                if date < datetime(2024, 4, 1, 0, 0, 0):
                    continue
                note = 'Ali--' + row[7].strip() + '--' + row[8].strip()
                refund = float(row[13].strip())
                amount = float(row[9].strip()) - refund
                expend_type = row[6].strip()
                transaction = TransactionRecord(date, note, amount, transaction_type, expend_type)
                transactions.append(transaction)
            except (ValueError, IndexError) as e:
                print(f"An error occurred: {e}")
                print(row)
                traceback.print_exc()  # 打印异常的完整轨迹
                continue
                
    return transactions

def parse_wx_csv(file_path):
    # 交易时间、类型（餐饮、购物等自定义的）、交易类型（微信自己添加的，不要）、交易对方、商品、收支、金额
    transactions = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # 过滤前后几行与标题列
            if any(cell == '' for cell in row):
                continue
            if "时间" in row[0].strip():
                continue

            try:
                date = datetime.strptime(row[0].strip(), '%Y/%m/%d %H:%M')
                if date < datetime(2024, 4, 1, 0, 0, 0):
                    continue
                note = 'WX--' + row[3].strip() + '--' + row[4].strip()
                amount_str = row[6].strip()[1:]
                amount = float(amount_str)
                transaction_type = row[5].strip()
                expend_type = row[1].strip()
                if transaction_type != "/":
                    transaction = TransactionRecord(date, note, amount, transaction_type, expend_type)
                    transactions.append(transaction)
            except (ValueError, IndexError) as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()  # 打印异常的完整轨迹
                # break
                continue
                
    return transactions
