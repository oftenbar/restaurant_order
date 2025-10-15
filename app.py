from flask import Flask, render_template, request, redirect, url_for

import requests
import os

import os

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
print("✅ Render sees Airtable token:", bool(AIRTABLE_TOKEN))

AIRTABLE_BASE_ID = "appK1NRDW4EAHq9PN"
AIRTABLE_TABLE_NAME = "orders"  # or your actual table name


app = Flask(__name__)

orders = []  # store all orders

def send_to_airtable(order):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    print("🧩 Debug Airtable headers:", headers)
    print("🔑 AIRTABLE_TOKEN starts with:", str(AIRTABLE_TOKEN)[:6])


    from datetime import datetime
    import pytz

    hk_tz = pytz.timezone('Asia/Hong_Kong')
    timestamp = datetime.now(hk_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "fields": {
            "Name": order["name"],
            "Table": order.get("table", ""),  # ✅
            "Lunch": order["lunch"],
            "Drink": order["drink"],
            "Snack": ", ".join(order["snack"]),
            "Total": order["total"],
            "Timestamp": datetime.now(hk_tz).isoformat()  # keeps full ISO format
        }
    }   

    response = requests.post(url, json=data, headers=headers)
    print("Airtable response:", response.status_code, response.text)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    table = request.args.get('table', '')  # ✅ keep table number from URL

    if request.method == 'POST':
        name = request.form['name']
        lunch = request.form['lunch']
        drink = request.form.get('drink', '無飲品')
        snack = request.form.getlist('snack')

        total = 0
        if "$" in lunch:
            total += int(lunch.split('$')[-1])
        if "8" in drink:
            total += 8
        if len(snack) == 1:
            total += 24
        elif len(snack) >= 2:
            total += 36

        order = {
            'name': name,
            'table': table,  # ✅ save table
            'lunch': lunch,
            'drink': drink,
            'snack': snack,
            'total': total
        }

        orders.append(order)
        send_to_airtable(order)

        return redirect(url_for('thank_you', table=table, total=total))

    return render_template('menu.html', table=table)



@app.route('/thank_you')
def thank_you():
    table = request.args.get('table', '?')
    total = request.args.get('total', 0)
    return f"""
    <h2>感謝您的訂單！🎉</h2>
    <p>餐桌號碼：{table}</p>
    <p>您的餐點總金額是：<b>${total}</b></p>
    <a href='/menu?table={table}'>返回菜單</a>
    """

@app.route('/orders')
def orders_dashboard():
    return render_template('orders.html', orders=orders)

@app.route('/check_airtable')
def check_airtable():
    import requests, os
    token = os.getenv("AIRTABLE_TOKEN")
    url = "https://api.airtable.com/v0/appK1NRDW4EAHq9PN/orders"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    return f"""
    <h3>✅ Token starts with:</h3> {str(token)[:6]}<br>
    <h3>🔢 Airtable Response:</h3> {r.status_code}<br>
    <pre>{r.text}</pre>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
