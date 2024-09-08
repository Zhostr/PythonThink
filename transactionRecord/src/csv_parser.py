# src/csv_parser.py

import csv
import traceback
import re
import locale
from datetime import datetime
from .transaction_record import TransactionRecord

def parse_zfb_csv(file_path, excel_name):
    '''
    交易时间、交易分类（自己改的）、交易对方(2)、对方账号、商品说明、收/支(5)、金额(6)、收付款方式、交易状态
    收/支：有一项是不计收支，包括余额宝收益、转出银行卡、退款、基金买入卖出等
    '''
    num = 0
    transactions = []
    with open(file_path, 'r', encoding='gb18030') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            num += 1
            # 过滤前后几行与标题列
            if num <= 25:
                continue

            try:
                expend_type = row[1].strip()
                if "亲友代付" in expend_type:
                    # 过滤掉我Excel中给媳妇儿代付的
                    continue
                
                transaction_type = row[5].strip()
                if transaction_type != "支出" and "亲情卡" not in row[7].strip():
                    # 保留媳妇儿Excel中使用亲情卡支付的交易
                    continue

                tx_status = row[8].strip()
                if tx_status != "交易成功":
                    continue

                date = str_to_date(row[0].strip())
                note = excel_name + row[1].strip() + row[2].strip() + '--' + row[4].strip()
                amount = float(row[6].strip())
                if amount == 0:
                    continue
                
                transaction = TransactionRecord(date, note, amount, transaction_type, expend_type)
                transactions.append(transaction)
            except (ValueError, IndexError) as e:
                print(f"An error occurred: {e}")
                print(row)
                traceback.print_exc()  # 打印异常的完整轨迹
                continue
                
    return transactions

def parse_wx_csv(file_path, excel_name):
    transactions = []
    num = 0
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            num += 1
            # 过滤前后几行与标题列
            if num <= 17:
                continue
            
            try:
                date = str_to_date(row[0].strip())
                note = excel_name + row[2].strip() + '--' + row[3].strip()
                amount_str = row[5].strip()[1:] #对字符串进行切片
                amount = locale.atof(amount_str)
                transaction_type = row[4].strip()
                consume_type = row[1].strip()
                if transaction_type == "支出":
                    now_status = row[7].strip()
                    if now_status == "已全额退款":
                        continue
                    
                    # 处理 已退款(￥0.06) 计算最终花费金额
                    match = re.search(r'￥(\d+(\.\d+)?)', now_status)
                    if match:
                         refund_amount = locale.atof(match.group(1))
                         amount -= refund_amount

                    transaction = TransactionRecord(date, note, amount, transaction_type, consume_type)
                    transactions.append(transaction)
            except (ValueError, IndexError) as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()  # 打印异常的完整轨迹
                # break
                continue
                
    return transactions

def str_to_date(date_str):
     # 定义两种可能的日期格式
    formats = ['%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M:%S']
    
    for fmt in formats:
        try:
            # 尝试将字符串转换为日期对象
            return datetime.strptime(date_str, fmt)
        except ValueError:
            # 如果格式不匹配，继续尝试下一种格式
            continue
    
    # 如果所有格式都不匹配，抛出异常
    raise ValueError(f"无法解析日期字符串: {date_str}")