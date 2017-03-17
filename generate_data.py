#!/usr/bin/python3
"""Script for generating data for use in java_coffee.mos"""

import numpy as np


DATAFILE_TEMPLATE = """
N_MONTHS: %(N_MONTHS)s ! Number of months.
N_CONSTRAINTS: %(N_CONSTRAINTS)s ! Number of constraints (N_MONTHS * 4 + 1)

MONTH_NAMES: [%(MONTH_NAMES)s] ! String data labels.
CONSTRAINT_NAMES: [%(GENERATE_CONSTRAINT_NAMES)s]
SELLING_PRICES: [%(SELLING_PRICES)s] ! Euros
PURCHASE_PRICES: [%(PURCHASE_PRICES)s] ! Euros

INITIAL_CASH_BALANCE: %(INITIAL_CASH_BALANCE)s ! Euros
INITIAL_STOCK: %(INITIAL_STOCK)s ! Units

WAREHOUSE_SIZE_LIMIT: %(WAREHOUSE_SIZE_LIMIT)s ! Units

FINAL_STOCK_TARGET: %(FINAL_STOCK_TARGET)s ! Units
"""

SIZES = [12, 60, 120, 1200, 12000]

FILENAME = "gendata_%s_month.dat"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
          "Nov", "Dec"]

def stringify_list(input_list):
  return ' '.join(['"%s"' % element for element in input_list])

def get_month_list(n_months):
  full = n_months//12
  remaining = n_months % 12
  return MONTHS * full + MONTHS[0:remaining]


def generate_constraints(month_list):
  constraints = []
  constraints.extend(["Warehouse Capacity %s" % month for month in month_list])
  constraints.extend(["Sales in %s Less Than Stock at the beginning of %s" %
      (month, month) for month in month_list])
  constraints.extend(["Target Final Stock"])
  constraints.extend([
      "Stock Must be Positive %s" % month for month in month_list])
  constraints.extend([
      "Cash Balance Must be Positive %s" % month for month in month_list])
  return constraints

def generate_string_data(n_months, initial_cash, initial_stock, warehouse_size,
                         final_stock):
  """Generate the string for the datafile."""
  months = get_month_list(n_months)
  purchase_prices_np = np.around(np.random.normal(
      2.85, .05, n_months), decimals=2)
  selling_prices_np = np.around(np.random.normal(
      3.1, .15, n_months), decimals=2)
  selling_prices = ["%s" % number for number in selling_prices_np]
  purchase_prices = ["%s" % number for number in purchase_prices_np]

  constraints = generate_constraints(months)
  values = {
      'N_MONTHS': n_months, 'N_CONSTRAINTS': 4 * n_months + 1,
      'MONTH_NAMES': stringify_list(months),
      'GENERATE_CONSTRAINT_NAMES': stringify_list(constraints),
      'SELLING_PRICES': ' '.join(selling_prices),
      'PURCHASE_PRICES': ' '.join(purchase_prices),
      'INITIAL_CASH_BALANCE': initial_cash,
      'INITIAL_STOCK': initial_stock, 'WAREHOUSE_SIZE_LIMIT':
      warehouse_size, 'FINAL_STOCK_TARGET': final_stock}

  return DATAFILE_TEMPLATE % values


if __name__ == '__main__':
  for size in SIZES:
    generated_data_string = generate_string_data(size, 20000, 1000, 5000, 2000)
    text_file = open(FILENAME % size, "w")
    text_file.write(generated_data_string)
    text_file.close()
