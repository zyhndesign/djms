# coding:utf-8


def to_inventory_unit(amount, unit):
    if unit == 'g':
        return amount
    elif unit == 'kg':
        return amount * 1000
    elif unit == 't':
        return amount * 1000 * 1000
    else:
        raise ValueError()