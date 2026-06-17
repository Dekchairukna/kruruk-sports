# KRURUK SPORTS Phase 4 - Sport Setup

ระบบ Flask สำหรับ KRURUK SPORTS ต่อจาก Phase 3 เพิ่มโมดูล Sport Setup

## Login เริ่มต้น

- Email: `admin@kruruksports.com`
- Password: `admin123`

## รันในเครื่อง

```bash
cd kruruk_sports_phase0
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

เปิด `http://127.0.0.1:5000`

## เพิ่มใน Phase 4

- Sport Category / หมวดกีฬา
- Sport / ชนิดกีฬา
- Sport Division / รุ่นแข่งขัน + เพศ + รูปแบบการแข่งขัน
- ปุ่มสร้างชุดกีฬาเริ่มต้น
- ตัวอย่างวิ่งแยก อนุบาล, ป.1 ถึง ม.3 ชาย/หญิง
- ตัวอย่างชักเย่อแยก อนุบาล, ประถมต้น, ประถมปลาย, มัธยมต้น, มัธยมปลาย ชาย/หญิง/ผสม
- นักกีฬาเลือกสมัครจาก Sport Setup แทนพิมพ์ชื่อกีฬาเอง

## เส้นทางสำคัญ

- `/events/<event_id>/sports` ตั้งค่ากีฬา
- `/team-entry` ทีมกรอกรหัส
- `/events/<event_id>/registrations` แอดมินตรวจรายชื่อนักกีฬา/ผู้ฝึกสอน

## หมายเหตุ

ZIP นี้ไม่แนบไฟล์ฐานข้อมูล `.db` เพื่อป้องกันปัญหา readonly database เครื่องจะสร้าง SQLite ใหม่เองใน `instance/kruruk_sports.db`

## Phase 6: Ranking Competition
- เพิ่มระบบ Ranking Competition สำหรับกรีฑาและกีฬาพื้นบ้าน
- สร้างรายการจาก Sport Setup
- บันทึกอันดับ เวลา ระยะ คะแนน
- คำนวณเหรียญทอง/เงิน/ทองแดงจากอันดับ 1/2/3 อัตโนมัติ
- พิมพ์ใบผลการแข่งขัน และ Export Excel

## Phase 7 Medal Table
- ตารางเหรียญรวมจาก Ranking และ Round Robin
- อันดับ 1 = ทอง, อันดับ 2 = เงิน, อันดับ 3 = ทองแดง
- เรียงอันดับรวมตาม ทอง → เงิน → ทองแดง
- กรองตามกีฬา รุ่น และเพศ
- ประกาศแชมป์รวม
- Export Excel และพิมพ์หน้าเว็บได้

## Phase 13B Social Login

เพิ่ม Social Login แบบ OAuth สำหรับ Google และ LINE โดยเปิดใช้ผ่านตัวแปรใน `.env`:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI` ถ้าไม่ใส่ ระบบจะใช้ `/auth/google/callback`
- `LINE_CHANNEL_ID`
- `LINE_CHANNEL_SECRET`
- `LINE_REDIRECT_URI` ถ้าไม่ใส่ ระบบจะใช้ `/auth/line/callback`

ระบบเพิ่มตาราง `social_accounts` เพื่อผูกบัญชี social กับผู้ใช้เดิม ถ้า email ตรงกับผู้ใช้เดิมจะเชื่อมบัญชีให้ ถ้าไม่พบจะสร้างผู้ใช้ใหม่ role `organization_admin` อัตโนมัติ

Callback URL ที่ควรตั้งใน Provider:

- Google: `https://YOUR_DOMAIN/auth/google/callback`
- LINE: `https://YOUR_DOMAIN/auth/line/callback`

## Phase 13C Payment Gateway

เพิ่มระบบชำระเงินต่อจาก Billing/Invoice ของ Phase 13A:

- Manual Transfer: ใช้งานได้ทันที รอ Super Admin กดยืนยันชำระเงิน
- PromptPay QR: ตั้งค่า `PROMPTPAY_ID`
- Stripe Checkout: ตั้งค่า `STRIPE_SECRET_KEY` และ `STRIPE_PUBLIC_KEY`
- Omise: ตั้งค่า `OMISE_PUBLIC_KEY` และ `OMISE_SECRET_KEY`

ตัวแปรเสริม:

- `PAYMENT_RETURN_BASE_URL` ใช้กำหนด domain สำหรับ success/cancel/return URL ตอน deploy เช่น `https://kruruksports.example.com`

ตารางใหม่:

- `payment_transactions` เก็บประวัติรายการชำระเงินแต่ละ gateway

หมายเหตุ: Stripe success route ในเฟสนี้ใช้ return จาก Checkout เป็นตัว mark paid เบื้องต้น ส่วน production ควรเปิด webhook เพิ่มเพื่อยืนยันสถานะจาก Stripe/Omise โดยตรง
