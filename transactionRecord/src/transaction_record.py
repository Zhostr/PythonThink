# src/transaction_record.py

class TransactionRecord:
    def __init__(self, date, note, amount, transaction_type, consume_way):
        # self 表示正在创建的对象
        self.date = date
        self.note = note
        # 金额
        self.amount = amount
        # 交易类型：支出/收入
        self.transaction_type = transaction_type
        # 消费方式：亲属卡交易、商户消费等（微信账单用）
        # 支付宝的消费方式，就是消费类型
        self.consume_way = consume_way

    def __repr__(self):
        return f"{self.consume_way} {self.date} 金额={self.amount}, note={self.note})"

    def is_family_card(self) -> bool:
        # 构造方法/实例方法的第一个参数代表当前实例，一般都使用约定成俗的名称`self`
        return self.consume_way == "亲属卡交易"
    
    def consume_type(self):
        # 租房,大额支出,出行,餐饮,水电费,下馆子,购物,医疗,宠物,快递,衣服鞋子,美容美发,日用百货,其他
        if "铁旅" in self.note or "去哪儿网" in self.note or "高德" in self.note or "交通" in self.note:
            return "出行"
        if "刀削面" in self.note or "餐饮" in self.note or "惠邻" in self.note or "麻辣烫" in self.note or "喜家德" in self.note:
            return "餐饮"
        if "煎饼" in self.note:
            return "餐饮"
        if "茶百道" in self.note or "果蔬" in self.note or "水果" in self.note:
            return "餐饮"
        if "顺丰" in self.note or "菜鸟裹裹" in self.note:
            return "快递"
        if "永辉超市" in self.note:
            return "购物"
        if "美团" in self.note:
            return "餐饮"
        # 补充宠物
        return "其他"

    def to_list(self):
        return [self.date, self.consume_type(), self.consume_way, self.amount, self.note]


