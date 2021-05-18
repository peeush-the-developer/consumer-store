class Item:
    def __init__(self, id_: str, name: str, price: float) -> None:
        self.id = id_
        self.name = name
        self.price = price


class Store:
    def __init__(self) -> None:
        self.items_dict = {
            'stv': Item('stv', 'Sony TV', 549.99),
            'cac': Item('cac', 'Central AC', 1399.99),
            'nsh': Item('nsh', 'Nike Shoe', 109.50),
            'mch': Item('mch', 'Charger', 30.00),
        }
        print('Store created')


class PriceRule:
    def __init__(self, item_id: str) -> None:
        self.item_id = item_id


class PriceRule_BuyX_PayForY(PriceRule):
    def __init__(self, item_id: str, buy_quantity: int, pay_for_quantity: int) -> None:
        super().__init__(item_id)
        self.buy_quantity = buy_quantity
        self.pay_for_quantity = pay_for_quantity


class PriceRule_BulkDiscount(PriceRule):
    def __init__(self, item_id: str, buy_quantity: int, discounted_price: float) -> None:
        super().__init__(item_id)
        self.buy_quantity = buy_quantity
        self.discounted_price = discounted_price


class PriceRule_BuyThis_GetThatFree(PriceRule):
    def __init__(self, item_id: str, free_item_id: str) -> None:
        super().__init__(item_id)
        self.item_id = item_id
        self.free_item_id = free_item_id


class Checkout(Store):
    def __init__(self, pricing_rules=[]) -> None:
        super().__init__()
        self.pricing_rules = pricing_rules
        self.item_ids = []
        print('Checkout created')

    def scan(self, id_: str) -> None:
        self.item_ids.append(id_)
        print(f'{self.items_dict[id_].name} added')

    def total(self) -> float:
        pass


if __name__ == '__main__':
    print('Welcome to Consumer store')
    pricing_rules = [
        PriceRule_BuyX_PayForY('nsh', buy_quantity=3, pay_for_quantity=2),
        PriceRule_BulkDiscount('stv', buy_quantity=4, discounted_price=499.99),
        PriceRule_BuyThis_GetThatFree('cac', 'mch')
    ]
    co = Checkout(pricing_rules)
    co.scan('stv')
    co.scan('stv')
    co.scan('nsh')
    print('Total: {}'.format(co.total()))
