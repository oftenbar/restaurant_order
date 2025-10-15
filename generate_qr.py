import qrcode

BASE_URL = "https://often-lunchorder.onrender.com/menu?table="  # 👈 replace with your Render URL

for i in range(1, 11):  # for tables 1–10
    table_url = f"{BASE_URL}{i}"
    img = qrcode.make(table_url)
    img.save(f"table_{i}_qr.png")
    print(f"✅ QR code generated for Table {i}: {table_url}")
