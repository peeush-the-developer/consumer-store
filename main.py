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
        self.pricing_rules_dict = {}
        print('Store created')

    def display_item(self, item_id: str, prefix: str = '') -> None:
        item = self.items_dict[item_id]
        print(f'{prefix} : {item.name:<10} | {item_id}'.strip())

    def remove_item(self, item_id: str, quantity: int) -> None:
        print('Store remove_item get called')
        pass

    def compute_amount(self, item_id: str, quantity: int) -> float:
        # print(item_id)
        price_per_item = self.items_dict[item_id].price
        if item_id in self.pricing_rules_dict:
            pricing_rule = self.pricing_rules_dict[item_id]
            # print(type(pricing_rule))
            if not isinstance(pricing_rule, PriceRule_BuyThis_GetThatFree):
                return pricing_rule.compute_amount(price_per_item, quantity)
            else:
                # print('PriceRule_BuyThis_GetThatFree detected')
                return self.compute_amount_buy_this_get_that_free(price_per_item, quantity, pricing_rule)

        return price_per_item * quantity

    def compute_amount_buy_this_get_that_free(self,
                                              price_per_item: float,
                                              quantity: int,
                                              pricing_rule: PriceRule_BuyThis_GetThatFree) -> float:
        self.remove_item(pricing_rule.free_item_id, quantity)
        return pricing_rule.compute_amount(price_per_item, quantity)


class Checkout(Store):
    Pricing_Rules = list[PriceRule]

    def __init__(self, pricing_rules: Pricing_Rules = []) -> None:
        super().__init__()
        self.pricing_rules_dict = {
            pricing_rule.item_id: pricing_rule for pricing_rule in pricing_rules}
        self.item_id_count = {}
        print('Checkout created')

    def scan(self, item_id: str) -> None:
        if item_id not in self.item_id_count:
            self.item_id_count[item_id] = 0
        self.item_id_count[item_id] += 1
        self.display_item(item_id, prefix='Scanned')

    def remove_item(self, item_id: str, quantity: int) -> None:
        # print('Checkout remove_item get called')
        if item_id in self.item_id_count:
            count = self.item_id_count[item_id]
            self.item_id_count[item_id] = max(0, count - quantity)
        else:
            super().remove_item(item_id, quantity)

    def total(self) -> None:
        total = 0.0
        for item_id, quantity in self.item_id_count.items():
            total += self.compute_amount(item_id, quantity)
        print('Total: ${0:.2f}'.format(total))


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
