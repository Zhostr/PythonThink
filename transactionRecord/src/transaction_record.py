# src/transaction_record.py

class TransactionRecord:
    def __init__(self, date, note, amount, transaction_type, expend_type):
        self.date = date
        self.note = note
        # 金额
        self.amount = amount
        # 交易类型：支出/收入
        self.transaction_type = transaction_type
        # 消费类型：餐饮、购物等
        self.expend_type = expend_type

    def __repr__(self):
        return f"{self.date}, {self.amount}, note={self.note})"

    


