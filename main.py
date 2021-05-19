from sys import argv


class Item:
    def __init__(self, id_: str, name: str, price: float) -> None:
        self.id = id_
        self.name = name
        self.price = price


class PriceRule:
    def __init__(self, item_id: str) -> None:
        self.item_id = item_id

    def compute_amount(self, price_per_item: float, quantity: int) -> float:
        return price_per_item * quantity


class PriceRule_BuyX_PayForY(PriceRule):
    def __init__(self, item_id: str, buy_quantity: int, pay_for_quantity: int) -> None:
        super().__init__(item_id)
        self.buy_quantity = buy_quantity
        self.pay_for_quantity = pay_for_quantity

    def compute_amount(self, price_per_item: float, quantity: int) -> float:
        # divmod function gives quotient and remainder of x / y operation
        q, r = divmod(quantity, self.buy_quantity)
        # Compute discounted amount for q * buy_quantity
        amount = price_per_item * self.pay_for_quantity * q
        # Compute normal for remainder (r) items
        amount += super().compute_amount(price_per_item, quantity=r)
        return amount


class PriceRule_BulkDiscount(PriceRule):
    def __init__(self, item_id: str, buy_quantity: int, discounted_price: float) -> None:
        super().__init__(item_id)
        self.buy_quantity = buy_quantity
        self.discounted_price = discounted_price

    def compute_amount(self, price_per_item: float, quantity: int) -> float:
        if quantity >= self.buy_quantity:
            return self.discounted_price * quantity
        return super().compute_amount(price_per_item, quantity)


class PriceRule_BuyThis_GetThatFree(PriceRule):
    def __init__(self, item_id: str, free_item_id: str) -> None:
        super().__init__(item_id)
        self.item_id = item_id
        self.free_item_id = free_item_id

    def compute_amount(self, price_per_item: float, quantity: int) -> float:
        return super().compute_amount(price_per_item, quantity)


class Store:
    def __init__(self) -> None:
        self.items_dict = {
            'stv': Item('stv', 'Sony TV', 549.99),
            'cac': Item('cac', 'Central AC', 1399.99),
            'nsh': Item('nsh', 'Nike Shoe', 109.50),
            'mch': Item('mch', 'Charger', 30.00),
        }
        print('Store created')

    def get_item(self, item_id: str) -> Item:
        return self.items_dict[item_id]

    def get_price_per_item(self, item_id: str) -> float:
        return self.get_item(item_id).price


class Checkout(Store):
    Pricing_Rules = list[PriceRule]

    def __init__(self, pricing_rules: Pricing_Rules = []) -> None:
        super().__init__()
        self.__pricing_rules_dict__ = {
            pricing_rule.item_id: pricing_rule for pricing_rule in pricing_rules}
        self.__item_id_count__ = {}
        self.__item_processed__ = {}
        print('Checkout created')

    def scan(self, item_id: str) -> None:
        if item_id not in self.__item_id_count__:
            self.__item_id_count__[item_id] = 0
        self.__item_id_count__[item_id] += 1
        self.__display_item__(item_id, prefix='Scanned')

    def total(self) -> None:
        self.__total__ = 0.0
        for item_id, quantity in self.__item_id_count__.items():
            amount = self.__compute_amount__(item_id, quantity)
            self.__total__ += amount
            self.__item_processed__[item_id] = quantity
        print('Total: ${0:.2f}'.format(self.__total__))

    def __compute_amount__(self, item_id: str, quantity: int) -> float:
        price_per_item = self.get_price_per_item(item_id)
        if item_id in self.__pricing_rules_dict__:
            pricing_rule = self.__pricing_rules_dict__[item_id]
            if not isinstance(pricing_rule, PriceRule_BuyThis_GetThatFree):
                return pricing_rule.compute_amount(price_per_item, quantity)
            else:
                return self.__compute_amount_buy_this_get_that_free__(price_per_item, quantity, pricing_rule)

        return price_per_item * quantity

    def __compute_amount_buy_this_get_that_free__(self,
                                                  price_per_item: float,
                                                  quantity: int,
                                                  pricing_rule: PriceRule_BuyThis_GetThatFree) -> float:
        self.__remove_item__(pricing_rule.free_item_id, quantity)
        return pricing_rule.compute_amount(price_per_item, quantity)

    def __display_item__(self, item_id: str, prefix: str = '') -> None:
        item = self.get_item(item_id)
        print(f'{prefix} : {item.name:<10} | {item_id}'.strip())

    def __remove_item__(self, item_id: str, quantity: int) -> None:
        if item_id in self.__item_id_count__:
            existing_quantity = self.__item_id_count__[item_id]
            self.__item_id_count__[item_id] = max(
                0, existing_quantity - quantity)
        # Handle already processed items
        if item_id in self.__item_processed__:
            processed_quantity = self.__item_processed__[item_id]
            price_per_item = self.get_price_per_item(item_id)
            if processed_quantity <= quantity:
                self.__total__ -= processed_quantity * price_per_item
            else:
                self.__total__ -= quantity * price_per_item


if __name__ == '__main__':
    # Get Command-line arguments
    item_ids = ['nsh', 'nsh', 'nsh', 'mch']
    if len(argv) > 1:
        item_ids = argv[1:]

    print('Welcome to Consumer store')
    pricing_rules = [
        PriceRule_BuyX_PayForY('nsh', buy_quantity=3, pay_for_quantity=2),
        PriceRule_BulkDiscount('stv', buy_quantity=4, discounted_price=499.99),
        PriceRule_BuyThis_GetThatFree('cac', 'mch')
    ]
    co = Checkout(pricing_rules)
    for item_id in item_ids:
        co.scan(item_id)
    co.total()
