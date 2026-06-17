# Phase 13B / 13C — Social Login + Payment Gateway

## Phase 13B Social Login
เพิ่ม Social Login ให้หน้า Login เดิม โดยรองรับ provider หลัก:

- Google
- LINE
- Facebook

ไฟล์/ส่วนที่เพิ่ม:

- `models.py`
  - `OAuthAccount`
  - เพิ่ม field ใน `User`: `avatar_url`, `social_provider`, `social_id`, `last_login_at`
- `app.py`
  - `/auth/<provider>`
  - `/auth/<provider>/callback`
  - helper สำหรับ OAuth profile และผูกบัญชีเดิมด้วย email
- `templates/auth/login.html`
  - ปุ่ม Social Login แสดงอัตโนมัติ ถ้าตั้งค่า `.env` ครบ

ตั้งค่า `.env` ตัวอย่าง:

```env
SOCIAL_LOGIN_ENABLED=1
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
LINE_CLIENT_ID=
LINE_CLIENT_SECRET=
FACEBOOK_CLIENT_ID=
FACEBOOK_CLIENT_SECRET=
```

Callback URL ที่ต้องใส่ใน console ของแต่ละ provider:

```text
https://YOUR_DOMAIN/auth/google/callback
https://YOUR_DOMAIN/auth/line/callback
https://YOUR_DOMAIN/auth/facebook/callback
```

## Phase 13C Payment Gateway
ต่อยอดจาก Invoice/Billing ของ Phase 13A โดยเพิ่ม Transaction และหน้า Payment

รองรับตอนนี้:

- `manual` — ใช้โอนเงิน/ตรวจรับชำระโดย Super Admin
- `promptpay` — สร้าง PromptPay QR จาก `PROMPTPAY_ID`
- `stripe` — โครง Stripe Checkout + Webhook `/payments/webhook/stripe`
- `omise` — เตรียมฐาน Transaction ไว้ต่อ Omise ภายหลัง

ไฟล์/ส่วนที่เพิ่ม:

- `models.py`
  - `PaymentTransaction`
  - เพิ่มความสัมพันธ์กับ `Invoice` และ `Organization`
- `app.py`
  - `/invoices/<id>/pay`
  - `/payments/<id>`
  - `/payments/<id>/mark-paid`
  - `/payments/webhook/stripe`
  - helper สร้าง PromptPay EMV payload และ QR
- `templates/billing/payment_transaction.html`
- `templates/billing/organization_billing.html`
  - เลือก gateway ตอนสร้าง invoice
  - ปุ่ม “ชำระเงิน” ในตาราง invoice

ตั้งค่า `.env` ตัวอย่าง:

```env
PAYMENT_GATEWAYS=manual,promptpay
PROMPTPAY_ID=0812345678
PAYMENT_RETURN_BASE_URL=https://YOUR_DOMAIN
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

> หมายเหตุ: PromptPay QR ไม่สามารถยืนยันการชำระเงินอัตโนมัติได้เอง ต้องให้ Super Admin ตรวจหลักฐานและกด “รับชำระ” หรือเชื่อมต่อผู้ให้บริการ Payment Gateway ที่มี webhook จริงเพิ่มภายหลัง

## Dependencies ที่เพิ่ม

```text
Authlib==1.3.2
qrcode[pil]==7.4.2
stripe==10.12.0
```

หลังอัปโหลดขึ้น Railway ให้รัน deploy ใหม่เพื่อ install requirements เพิ่ม
