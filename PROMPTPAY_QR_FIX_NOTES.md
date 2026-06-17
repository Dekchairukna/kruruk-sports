# PromptPay QR Fix

แก้ปัญหาหน้า Payment แสดงเป็นข้อความ payload แต่ไม่ขึ้น QR Code

## สิ่งที่แก้
- เพิ่มฟังก์ชัน `make_promptpay_qr_png()` ให้คืน error ชัดเจนเมื่อไม่มี qrcode/Pillow
- หน้า Payment แสดง QR แบบรูปภาพจริง ถ้าสร้างได้
- เพิ่มปุ่ม “เปิด QR เต็มจอ”
- เพิ่ม route `/payments/<txn_id>/promptpay-qr.png`
- เพิ่ม `Pillow>=10.0.0` ใน requirements.txt

## ถ้ายังไม่ขึ้น QR
รันคำสั่งนี้ใน venv:

```bash
pip install -r requirements.txt
# หรือ
pip install "qrcode[pil]" Pillow
```

แล้วปิด/เปิด Flask ใหม่
