# Set Score UI Fix

เพิ่มหน้าบันทึกคะแนนรายเซตแบบแตะชื่อทีมเพื่อเพิ่มแต้ม

## เพิ่ม/แก้

- Round Robin set-based match result
  - เลือกเซตด้วยปุ่ม เซต 1..n
  - กดชื่อโรงเรียน/การ์ดทีมเพื่อเพิ่มแต้มทีละ 1
  - แสดงคะแนนสดของเซตที่เลือก
  - ย้อนแต้มล่าสุดได้
  - ล้างแต้มเฉพาะเซตที่เลือกได้
  - เก็บประวัติแต้มแบบ point-by-point ลง `score_history`
  - แสดงประวัติว่าเซตไหน ทีมไหนได้แต้ม คะแนนยืนอยู่เท่าไหร่
  - แสดงตารางยืนในกลุ่มปัจจุบันด้านข้าง

- Knockout set-based match result
  - เพิ่มหน้า `/knockout/matches/<match_id>/result`
  - ใช้ UI แตะชื่อทีมเพื่อเพิ่มแต้มเหมือน Round Robin
  - เก็บ `set_scores` และ `score_history`
  - บันทึกแล้วสรุปผู้ชนะและเลื่อนรอบอัตโนมัติตามระบบเดิม

## Database upgrade

เพิ่มคอลัมน์ถ้ายังไม่มี:

- `round_robin_matches.score_history TEXT`
- `knockout_matches.set_scores TEXT`
- `knockout_matches.score_history TEXT`
- `knockout_matches.point_diff INTEGER DEFAULT 0`

ระบบเพิ่มให้เองตอนเปิดแอปผ่าน `ensure_schema_upgrades()` ไม่ลบข้อมูลเดิม
