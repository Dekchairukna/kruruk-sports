# Phase 13J Railway Timeout + DB Fix

อัปเดตจากไฟล์งานปัจจุบัน `phase13I_railway_deploy_fix` โดยแก้เฉพาะปัญหา deploy บน Railway:

- เปลี่ยน PostgreSQL driver จาก `psycopg2-binary` เป็น `psycopg[binary]`
- แปลง `DATABASE_URL` อัตโนมัติจาก `postgresql://...` เป็น `postgresql+psycopg://...`
- เพิ่ม `DB_CONNECT_TIMEOUT` ค่าเริ่มต้น 10 วินาที
- เพิ่ม `SQLALCHEMY_ENGINE_OPTIONS` พร้อม `pool_pre_ping`
- เพิ่ม endpoint `/healthz` สำหรับเช็กว่าเว็บตอบโดยไม่ต้องแตะฐานข้อมูลหนัก ๆ
- เพิ่ม `SKIP_DB_INIT=1` สำหรับข้าม `db.create_all()` / schema upgrade ชั่วคราวเวลาต้องการให้เว็บ boot ก่อน
- ครอบ database initialization ด้วย try/except เพื่อไม่ให้ worker ตายทันทีตอนฐานข้อมูลมีปัญหา

## Railway Variables ที่แนะนำ

```env
SECRET_KEY=kruruk-sports-secret-2026-change-long-random
PROMPTPAY_ID=1400700151189
DATABASE_URL=${{ Postgres.DATABASE_URL }}
DB_CONNECT_TIMEOUT=10
```

ถ้าเว็บยังไม่ตอบ ให้เพิ่มชั่วคราว:

```env
SKIP_DB_INIT=1
```

แล้วทดสอบ:

```text
/healthz
```
