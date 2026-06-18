# Phase 13K LINE Team Invite

เพิ่มช่อง LINE สำหรับหัวหน้าสี/หัวหน้าทีม และปุ่มส่งข้อความเชิญกรอกข้อมูลผ่าน LINE Messaging API

## เพิ่มใน Team
- line_contact_name: ชื่อหัวหน้าสี/ผู้รับผิดชอบ
- line_user_id: LINE userId สำหรับ push message
- line_invite_sent_at: เวลาส่งล่าสุด
- line_invite_error: error ล่าสุดจาก LINE API

หมายเหตุ: LINE userId ต้องเป็นค่า userId จาก LINE Official Account/LIFF เช่น `Uxxxxxxxx...` ไม่ใช่ LINE ID หรือ @ไอดีที่ผู้ใช้ตั้งเอง

## เพิ่มหน้าใช้งาน
- เพิ่มช่องกรอกหัวหน้าสีและ LINE userId ในหน้าเพิ่ม/แก้ไขทีม/สี
- เพิ่มปุ่มส่ง LINE รายทีมในหน้า Event Detail
- เพิ่มปุ่มส่ง LINE ทุกสีที่มี LINE userId ในหน้า Event Detail
- ข้อความที่ส่งประกอบด้วยชื่องาน ชื่อทีม/สี รหัสกรอกข้อมูล และลิงก์ `/team-entry`

## Environment Variable
ตั้งค่าใน `.env` หรือ Railway Variables:

```
LINE_CHANNEL_ACCESS_TOKEN=ใส่ channel access token ของ LINE Official Account
```

หากยังไม่ตั้งค่า ระบบจะ disable ปุ่มส่ง LINE และแสดงเตือนว่า `ยังไม่ได้ตั้งค่า LINE_CHANNEL_ACCESS_TOKEN`
