# Railway Deploy Fix

แก้ปัญหา Application failed to respond บน Railway

## สิ่งที่แก้
- เพิ่ม `gunicorn` ใน requirements.txt
- เพิ่ม `Procfile`
- เพิ่ม `railway.toml`
- เปลี่ยน `app.run(debug=True)` เป็น bind `0.0.0.0` และใช้ `$PORT`
- ปิด debug เป็นค่าเริ่มต้นบน production

## Railway Variables ที่ควรมี
```env
SECRET_KEY=ใส่ค่าสุ่มยาวๆ
PROMPTPAY_ID=1400700151189
DATABASE_URL=ค่าจาก Railway PostgreSQL ถ้ามี
```

ถ้ายังไม่มี PostgreSQL ให้ไม่ต้องตั้ง DATABASE_URL ใน Railway
