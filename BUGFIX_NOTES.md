# KRURUK SPORTS Bugfix + Admin Patch

## แก้ตามคำขอ

### 1) Super Admin กลางระบบ
- Login ID: `superadmin`
- Password: `yagami1225`
- Email ภายในระบบ: `superadmin@kruruksports.local`
- ระบบจะสร้าง/ซ่อมบัญชีนี้ตอนเปิดแอปผ่าน `seed_default_admin()`
- หน้า Login เปลี่ยนจาก Email อย่างเดียวเป็น `Email / ID`

### 2) Sport Setup กดแล้วไม่ไปหน้าเดิมผิด ๆ
- แก้ sidebar แล้ว:
  - `Teams / Colors` จะพาไปหน้างานปัจจุบันและเลื่อนไปส่วนทีม
  - `Sport Setup` จะพาไปหน้าตั้งค่ากีฬาของงานปัจจุบัน
  - `Billing` จะพาไป Billing ขององค์กรปัจจุบัน
- ถ้าอยู่นอกบริบทงาน จะยังกลับไปหน้า Events / Organizations ตามเดิม

### 3) แก้ไข Sport / Result Setup ได้แล้ว
เดิมมีแค่เพิ่มกับลบ ตอนนี้เพิ่ม route และปุ่มแก้ไขให้:
- แก้หมวดกีฬา
- แก้ชนิดกีฬา
- แก้รายการย่อย/รุ่น/เพศ
- แก้ระบบแข่งขัน เช่น ranking, round_robin, knockout
- แก้วิธีบันทึกผล เช่น score_only, set_based, ranking, contest
- แก้ค่าเซตสูงสุด แต้มต่อเซต ชนะกี่เซต

### 4) ตรวจ syntax
- `python3 -m py_compile app.py models.py` ผ่านแล้ว

## ไฟล์ที่แก้หลัก
- `app.py`
- `models.py`
- `templates/base.html`
- `templates/auth/login.html`
- `templates/events/detail.html`
- `templates/sports/setup.html`
- `.env.example`
