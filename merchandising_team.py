import datetime
import pandas as pd
from data_fetcher import *
from googleSpreadSheet import *

# Getting epoch of one month back
current_date = datetime.datetime.now().replace(microsecond=0)
date_limit = current_date - datetime.timedelta(30)
time_limit_epochs = date_limit.timestamp() * 1000

# spreadsheet_key
spreadsheet_key = '1yT8FKPPVa8pWtjkD2jLrg-CHP4QS_VzoM-FltRQZFu4'

# Creating a googleSheet instance
googleSheet = GoogleSheetConnector(spreadsheet_key)

# Clearing data on the sheet
googleSheet.clear_sheet()

# Adding the header data
googleSheet.add_header("merch")

# GETTING SKU COUNTS OF THE PAST MONTH

# Creating a dictionary with the count of sku values of all the orders
sku_count_monthly_all = dict()

# Creating a list of high_demand_skus whose count is more than 3
sku_count_monthly_all_high_demand = list()

# Populating the data into the created dict
for sku in orderLines[orderLines["orderDate"] > time_limit_epochs]["sku"]:
    if sku in sku_count_monthly_all.keys():
        sku_count_monthly_all[sku] += 1
    else:
        sku_count_monthly_all[sku] = 1

# Updating Sheet
googleSheet.update_sheet(sku_count_monthly_all, "A", 1, 1)
googleSheet.update_sheet(sku_count_monthly_all, "B", 1, 0)

# Populating the list of high demand sku's
for key, value in sorted(sku_count_monthly_all.items(), key=lambda item: item[1], reverse=True):
    if value >= 3:
        sku_count_monthly_all_high_demand.append(key)

# Updating Sheet
googleSheet.update_sheet(sku_count_monthly_all_high_demand, "D")

# Creating a dictionary with the count of sku values of all the confirmed orders
sku_count_monthly_confirmed = dict()

# Creating a list of high_demand_skus whose count is more than 3
sku_count_monthly_confirmed_high_demand = list()

# Populating the data into the created dict
for sku in orderLines[(orderLines["orderDate"] > time_limit_epochs) & (orderLines["isCancelled"] == False)]["sku"]:
    if sku in sku_count_monthly_confirmed.keys():
        sku_count_monthly_confirmed[sku] += 1
    else:
        sku_count_monthly_confirmed[sku] = 1

# Updating Sheet
googleSheet.update_sheet(sku_count_monthly_confirmed, "F", 1, 1)
googleSheet.update_sheet(sku_count_monthly_confirmed, "G", 1, 0)

# Populating the list of high demand sku's
for key, value in sorted(sku_count_monthly_confirmed.items(), key=lambda item: item[1], reverse=True):
    if value >= 3:
        sku_count_monthly_confirmed_high_demand.append(key)

googleSheet.update_sheet(sku_count_monthly_confirmed_high_demand, "I")

# GETTING PAST MONTH DESGINER'S COUNT

# Creating a dictionary with the count of designer's name of all the orders
designer_count_monthly_all = dict()

for designer in orderLines[orderLines["orderDate"] > time_limit_epochs]["designer"]:
    if designer in designer_count_monthly_all.keys():
        designer_count_monthly_all[designer] += 1
    else:
        designer_count_monthly_all[designer] = 1

# Updating Sheets
googleSheet.update_sheet(designer_count_monthly_all, "K", 1, 1)
googleSheet.update_sheet(designer_count_monthly_all, "L", 1, 0)

# Creating a dictionary with the count of designer's name of all the confirmed orders
designer_count_monthly_confirmed = dict()

for designer in orderLines[(orderLines["orderDate"] > time_limit_epochs) & (orderLines["isCancelled"] == False)]["designer"]:
    if designer in designer_count_monthly_confirmed.keys():
        designer_count_monthly_confirmed[designer] += 1
    else:
        designer_count_monthly_confirmed[designer] = 1

# Updating Sheets
googleSheet.update_sheet(designer_count_monthly_confirmed, "N", 1, 1)
googleSheet.update_sheet(designer_count_monthly_confirmed, "O", 1, 0)

# GETTING PAST MONTH'S TYPE OF OUTFIT COUNT

# Creating a dictionary with the count of outfit's category of all the orders
category_count_monthly_all = dict()

for sku in orderLines[orderLines["orderDate"] > time_limit_epochs]["sku"]:
    for category in catalogue[catalogue["sku"] == sku]["categories"]:
        for category2 in category:

            if category2 in category_count_monthly_all:
                category_count_monthly_all[category2] += 1
            else:
                category_count_monthly_all[category2] = 1

# Updating Sheets
googleSheet.update_sheet(category_count_monthly_all, "Q", 1, 1)
googleSheet.update_sheet(category_count_monthly_all, "R", 1, 0)

# Creating a dictionary with the count of outfit's category of all the confirmed orders
category_count_monthly_confirmed = dict()

for sku in orderLines[(orderLines["orderDate"] > time_limit_epochs) & (orderLines["isCancelled"] == False)]["sku"]:
    for category in catalogue[catalogue["sku"] == sku]["categories"]:
        for category2 in category:
            if category2 in category_count_monthly_confirmed:
                category_count_monthly_confirmed[category2] += 1
            else:
                category_count_monthly_confirmed[category2] = 1

# Updating Sheets
googleSheet.update_sheet(category_count_monthly_confirmed, "T", 1, 1)
googleSheet.update_sheet(category_count_monthly_confirmed, "U", 1, 0)

# GETTING CITY COUNT

# Creating a dictionary with the count of outfit's location of all the orders
location_count_monthly_all = dict()

for city in orderLines[orderLines["orderDate"] > time_limit_epochs]["orderCity"]:
    if city in location_count_monthly_all.keys():
        location_count_monthly_all[city] += 1
    else:
        location_count_monthly_all[city] = 1

# Updating Sheets
googleSheet.update_sheet(location_count_monthly_all, "W", 1, 1)
googleSheet.update_sheet(location_count_monthly_all, "X", 1, 0)

# Creating a dictionary with the count of outfit's category of all the confirmed orders
location_count_monthly_confirmed = dict()

for city in orderLines[(orderLines["orderDate"] > time_limit_epochs) & (orderLines["isCancelled"] == False)][
    "orderCity"]:
    if city in location_count_monthly_confirmed.keys():
        location_count_monthly_confirmed[city] += 1
    else:
        location_count_monthly_confirmed[city] = 1

# Updating Sheets
googleSheet.update_sheet(location_count_monthly_confirmed, "Z", 1, 1)
googleSheet.update_sheet(location_count_monthly_confirmed, "AA", 1, 0)

# GETTING PRICE POINT RANGE

# Creating a dictionary with the count of outfit's location of all the orders
price_count_monthly_all = dict()


# A function to get the price's round off
def get_range_thousands(num):
    num2 = round(num, -3)
    if num - num2 > 0:
        temp_final = num2 + 1000
    else:
        temp_final = num2
    return temp_final


# A function to get the price's round off
def get_range_hundreds(num):
    num2 = round(num, -2)
    if num - num2 > 0:
        temp_final = num2 + 100
    else:
        temp_final = num2
    return temp_final


for price in orderLines[orderLines["orderDate"] > time_limit_epochs]["rentPaid"]:
    price = get_range_hundreds(price)
    if price in price_count_monthly_all.keys():
        price_count_monthly_all[price] += 1
    else:
        price_count_monthly_all[price] = 1

# Updating Sheets
googleSheet.update_sheet(price_count_monthly_all, "AC", 1, 1)
googleSheet.update_sheet(price_count_monthly_all, "AD", 1, 0)

# Creating a dictionary with the count of outfit's category of all the confirmed orders
price_count_monthly_confirmed = dict()

for price in orderLines[(orderLines["orderDate"] > time_limit_epochs) & (orderLines["isCancelled"] == False)]["rentPaid"]:
    price = get_range_hundreds(price)
    if price in price_count_monthly_confirmed.keys():
        price_count_monthly_confirmed[price] += 1
    else:
        price_count_monthly_confirmed[price] = 1

# Updating Sheets
googleSheet.update_sheet(price_count_monthly_confirmed, "AF", 1, 1)
googleSheet.update_sheet(price_count_monthly_confirmed, "AG", 1, 0)

# GETTING ALL THE NON-PERFORMING SKU'S DETAILS

# Getting epoch of 6 month back
current_date = datetime.datetime.now()
date_limit = current_date - datetime.timedelta(180)

filtered_catalogue = catalogue[(pd.isna(catalogue["latestScan"]) == True) & (catalogue["status"] == True) & (catalogue["updateddate"] > date_limit) & (catalogue["disabled"] == False)]

## RETAIL PRICE DISTRIBUTION RANGE

# Creating a dictionary with the count of retail price of all the orders
retail_price_count_non_performing_all = dict()

for price in filtered_catalogue["retailprice"]:
    price = get_range_hundreds(price)
    if price in retail_price_count_non_performing_all.keys():
        retail_price_count_non_performing_all[price] += 1
    else:
        retail_price_count_non_performing_all[price] = 1

googleSheet.update_sheet(retail_price_count_non_performing_all, "AI", 1, 1)
googleSheet.update_sheet(retail_price_count_non_performing_all, "AJ", 1, 0)

## DEPOSIT PRICE DISTRIBUTION RANGE

# Creating a dictionary with the count of deposit price of all the orders
deposit_price_count_non_performing_all = dict()

for price in filtered_catalogue["depositprice"]:
    price = get_range_hundreds(price)
    if price in deposit_price_count_non_performing_all.keys():
        deposit_price_count_non_performing_all[price] += 1
    else:
        deposit_price_count_non_performing_all[price] = 1

googleSheet.update_sheet(deposit_price_count_non_performing_all, "AL", 1, 1)
googleSheet.update_sheet(deposit_price_count_non_performing_all, "AM", 1, 0)


##  CATEGORY COUNT

# Creating a dictionary with the count of category of all the orders
category_count_non_performing_all = dict()

for cat in filtered_catalogue["categories"]:
    for categories in cat:
        if categories in category_count_non_performing_all:
            category_count_non_performing_all[categories] += 1
        else:
            category_count_non_performing_all[categories] = 1

googleSheet.update_sheet(category_count_non_performing_all, "AO", 1, 1)
googleSheet.update_sheet(category_count_non_performing_all, "AP", 1, 0)

## DESIGNER COUNT

# Creating a dictionary with the count of designer of all the orders
designer_count_non_performing_all = dict()

for designer_name in filtered_catalogue["designer"]:
    if designer_name in designer_count_non_performing_all.keys():
        designer_count_non_performing_all[designer_name] += 1
    else:
        designer_count_non_performing_all[designer_name] = 1

googleSheet.update_sheet(designer_count_non_performing_all, "AR", 1, 1)
googleSheet.update_sheet(designer_count_non_performing_all, "AS", 1, 0)
