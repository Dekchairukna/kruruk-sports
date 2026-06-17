# Phase 13H PromptPay Scan Fix

แก้บั๊ก QR PromptPay แสดงเป็นรูปได้ แต่แอปธนาคารสแกนจ่ายไม่ได้

## สาเหตุ
Payload เดิมลงท้าย CRC เป็น `6300XXXX` ซึ่งผิดมาตรฐาน EMVCo สำหรับ QR Payment
ต้องเป็น `6304XXXX` เพราะช่อง CRC tag 63 ต้องมีความยาว 04 แล้วคำนวณ CRC จาก payload ที่ลงท้ายด้วย `6304`

## สิ่งที่แก้
- แก้ `build_promptpay_payload()` ให้สร้าง CRC แบบถูกต้อง
- เพิ่ม `is_promptpay_payload_scanable()` สำหรับตรวจ payload เก่า
- เพิ่ม `ensure_promptpay_payload_for_transaction()` เพื่อซ่อม transaction เดิมที่บันทึก QR ผิดไว้แล้ว
- เมื่อเปิดหน้า Payment หรือเปิด QR เต็มจอ ระบบจะ rebuild payload ให้เองถ้าเจอของเก่า

## วิธีใช้หลังอัปเดต
1. แตก zip ทับโปรเจกต์
2. ตรวจ `.env` ว่ามี `PROMPTPAY_ID=1400700151189`
3. ปิด Flask ด้วย Ctrl+C
4. เปิดใหม่ `python app.py`
5. เข้า Payment เดิมซ้ำ หรือสร้างใบใหม่ QR จะเปลี่ยนเป็น payload ที่สแกนได้
