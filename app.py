from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

orders = []

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    table = request.args.get('table', '')  # get table number from ?table=1
    return render_template("menu.html", table_number=table)

@app.route('/submit_order', methods=["POST"])
def submit_order():
    table_number = request.args.get("table", " ")
    phone = request.form.get("phone")

    # 🥢 Read main and sub-options
    rice = request.form.get("rice")
    rice_option = request.form.get("rice_option", "正常")

    drink = request.form.get("drink")
    drink_option = request.form.get("drink_option", "正常")

    snacks = request.form.getlist("snacks")

    # 💰 Pricing rules
    rice_prices = {
        "香茅豬扒飯": 58,
        "西冷牛扒飯": 58,
        "秘製雞扒飯": 58,
        "頂盛雜扒飯": 68,
        "極上鰻魚飯": 58
    }

    total = 0
    rice_price = rice_prices.get(rice, 0)
    total += rice_price

    if drink:
        total += 8  # Add $8 if drink is selected

    if len(snacks) == 1:
        total += 24
    elif len(snacks) >= 2:
        total += 36

    order = {
        "table_number": table_number,
        "phone": phone,
        "rice": rice,
        "rice_option": rice_option,
        "drink": drink,
        "drink_option": drink_option,
        "snacks": snacks,
        "total": total
    }

    orders.append(order)
    return render_template("confirmation.html", **order)

@app.route('/orders')
def order_list():
    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
