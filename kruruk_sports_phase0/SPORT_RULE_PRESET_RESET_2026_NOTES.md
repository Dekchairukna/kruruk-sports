# SPORT RULE PRESET RESET 2026

อัปเดตตามคำสั่งครูรัก: ล้างข้อมูลคลังกีฬาตัวอย่างเดิม แล้วสร้างชุดกีฬามาตรฐานใหม่ที่ตรวจจากเว็บกลาง/สหพันธ์ล่าสุดเท่าที่ตรวจได้ ณ 2026-06-19

## เปลี่ยนแนวคิด

เดิมระบบ seed สร้างชนิดกีฬา + รายการย่อยจำนวนมาก เช่น แยกรุ่น/เพศจนกลายเป็นหลายร้อยรายการ ทำให้ผู้ใช้สับสน

รอบนี้เปลี่ยนเป็น:

1. ปุ่ม `ล้างคลังเดิม + สร้างชุดล่าสุด`
2. ล้าง `sport_categories`, `sports`, `sport_divisions` ของอีเว้นท์นั้นก่อน
3. ไม่ลบทีม/สี และไม่ลบการแข่งขันที่สร้างไว้แล้ว
4. ถ้ามีการแข่งขันเดิมผูกกับ division เก่า ระบบจะตั้ง `sport_division_id = NULL` ให้ก่อนกัน FK ค้าง
5. สร้างคลังใหม่แบบเบา ๆ: 1 กีฬา = 1 division เริ่มต้น `Open / รวม`
6. การแยกรุ่น/เพศจริงให้สร้างตอนหน้า `สร้างการแข่งขัน`

## จำนวนหลังอัปเดต

- หมวดกีฬา: 5
- ชนิดกีฬา: 16
- รายการย่อยเริ่มต้น: 16

ไม่ใช่ 238 รายการย่อยแบบเดิมแล้ว

## กติกา/ค่า default สำคัญ

### เซปักตะกร้อ
- result_type: `set_based`
- max_sets: 3
- points_per_set: 15
- sets_to_win: 2
- note: ISTAF Law of the Game 2024: ชนะ 2 ใน 3 เซต; เซตละ 15 แต้ม; 14-14 เล่นถึง 17 แต้ม
- source: ISTAF Law of the Game 2024, official ISTAF page/PDF

### วอลเลย์บอล
- result_type: `set_based`
- max_sets: 5
- points_per_set: 25
- sets_to_win: 3
- note: FIVB Official Volleyball Rules 2025-2028: ชนะ 3 เซต; เซต 1-4 ถึง 25 แต้ม ต้องห่าง 2; เซตตัดสินถึง 15 แต้ม
- source: FIVB Official Volleyball Rules 2025-2028

### แบดมินตัน
- result_type: `set_based`
- max_sets: 3
- points_per_set: 21
- sets_to_win: 2
- note: BWF Laws ปัจจุบัน: 2 ใน 3 เกม เกมละ 21 แต้ม; BWF อนุมัติ 3x15 เริ่ม 4 ม.ค. 2027
- source: BWF Laws / BWF official news 2026

### เทเบิลเทนนิส
- result_type: `set_based`
- max_sets: 5
- points_per_set: 11
- sets_to_win: 3
- note: ITTF Laws: เกมละ 11 แต้ม ต้องชนะห่าง 2; ค่าเริ่มต้นระบบใช้ 3 ใน 5 เกม
- source: ITTF rules/statutes

### เปตอง
- result_type: `score_only`
- default_format: `knockout`
- note: FIPJP Official Rules: เกมปกติถึง 13 คะแนน; ลีก/รอบคัดเลือกอาจกำหนด 11 คะแนนตามระเบียบงาน
- source: FIPJP Official Rules

### ฟุตซอล
- result_type: `score_only`
- default_format: `round_robin`
- note: FIFA Futsal Laws of the Game 2025/26: ปกติ 2 ครึ่ง ครึ่งละ 20 นาที บันทึกผลเป็นประตูได้-เสีย
- source: FIFA Futsal Laws of the Game 2025/26

### ฟุตบอล
- result_type: `score_only`
- default_format: `round_robin`
- note: IFAB Laws of the Game 2025/26: บันทึกผลเป็นประตูได้-เสีย ระยะเวลาแข่งขันปรับตามระเบียบงานได้
- source: IFAB Laws of the Game 2025/26

## ไฟล์ที่แก้

- `app.py`
- `templates/sports/setup.html`
- `templates/sports/competition_wizard.html`
- `instance/kruruk_sports.db` ใน zip ตัวอย่างถูกล้างและ seed ใหม่แล้ว

## หมายเหตุด้าน schema

ตอนนี้ schema มีช่อง `max_sets`, `points_per_set`, `sets_to_win` แต่ยังไม่มีช่องแยกสำหรับ:
- decisive_set_points เช่น วอลเลย์บอลเซต 5 ถึง 15
- deuce_cap เช่น ตะกร้อ 14-14 ไปถึง 17
- win_by_two
- match_duration

รายละเอียดพวกนี้จึงถูกเก็บไว้ใน `note` ก่อน ถ้าจะทำให้แม่นขึ้นรอบต่อไปควรเพิ่มตาราง/คอลัมน์ `sport_rule_presets` แยกจริง
