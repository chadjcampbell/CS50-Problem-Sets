from cs50 import get_float

while True:
    total = get_float("Change owed: ")
    if total > 0:
        break

quarters = 0
dimes = 0
nickles = 0
pennies = 0

if total >= 0.25:
    quarters = total // 0.25
    total = round(total - quarters * 0.25, 2)

if total >= 0.10:
    dimes = total // 0.10
    total = round(total - dimes * 0.10, 2)

if total >= 0.05:
    nickles = total // 0.05
    total = round(total - nickles * 0.05, 2)

if total >= 0.01:
    pennies = total // 0.01
    total = round(total - pennies * 0.01, 2)

coins = int(quarters + dimes + nickles + pennies)
print(coins)