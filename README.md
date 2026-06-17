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
