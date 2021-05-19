# Consumer Store

A project for implementing Consumer store based on Python OOPS concept.

## Problem statement

We will be starting a Consumer Store and the checkout system is currently like this:

ITEM_ID | NAME | PRICE
:--- | :--- | ---:
stv | Sony TV | $549.99
cac | Central AC | $1399.99
nsh | Nike Shoe | $109.50
mch | Charger | $30.00

As this is a new store, we would like to have opening day specials.

1. We have a 3 for 2 great deal on Nike Shoes. i.e. if you buy 3 Nike Shoes, you’ll just pay the price of 2.
2. Sony TV will have a Bulk discount, where the price will drop to $499.99 each, if someone buys more
than 4.
3. We will add an additional Charger free of cost with every Central AC sold

Build a system that is flexible enough to change the pricing rules whenever we want in the future(i.e. there should be a very minimal effort to change the rules) - **Make it as generic as possible**

**Also, the Store checkout system can scan items in any order.**

**The interface should look something like this(example in Python):**

```python
co = Checkout(pricing_rules)
co.scan(item1)
co.scan(item2)
co.total()
```

Your task is to implement a system that based on the above conditions provides the final total checkout cost.

**Example scenarios:**  
**ITEM_IDs Scanned:** nsh, nsh, nsh, mch  
**Expected total:** $249.00

**ITEM_IDs Scanned:** nsh, stv, stv, nsh, stv, stv, stv  
**Expected total:** $2718.95

**ITEM_IDs Scanned:** cac, mch, stv  
**Expected total:** $1949.98

## Run the solution

```shell
python main.py
```
