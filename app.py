from flask import Flask, render_template, request, redirect, url_for

from datetime import datetime
import pytz

app = Flask(__name__)

orders = []  # store all orders

# === Route: Menu Page ===
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    table = request.args.get('table', '')

    if request.method == 'POST':
        name = request.form['name']
        lunch = request.form['lunch']
        drink = request.form.get('drink', '無飲品')
        snack = request.form.getlist('snack')

        # Calculate total
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
            "name": name,
            "table": table,
            "lunch": lunch,
            "drink": drink,
            "snack": snack,
            "total": total
        }

        orders.append(order)
 

        return redirect(url_for('thank_you', table=table, total=total))

    return render_template('menu.html', table=table)


# === Route: Thank You Page ===
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


# === Route: Orders Dashboard ===
@app.route('/orders')
def orders_dashboard():
    return render_template('orders.html', orders=orders)


# === Run App Locally ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
