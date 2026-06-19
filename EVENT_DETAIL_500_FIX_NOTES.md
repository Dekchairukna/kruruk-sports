# EVENT DETAIL 500 FIX

แก้ปัญหา Internal Server Error ที่หน้า `/events/<id>` หลังเพิ่มส่วน "การแข่งขันในอีเว้นท์นี้"

สาเหตุ:
- โค้ดนับคู่ที่แข่งเสร็จใช้ `m.winner_team_id` กับ match ของ Round Robin
- แต่ `RoundRobinMatch` ไม่มี field `winner_team_id`
- ถ้าในอีเว้นท์มีรายการ Round Robin อยู่แล้ว หน้า Event จะ 500 ทันที

วิธีแก้:
- เพิ่ม helper `match_done(match)` ใช้กับทุกระบบ
- ตรวจจาก status, winner_team_id ถ้ามี, score_a/score_b, set_a/set_b
- ทำให้ Round Robin, Knockout แสดงจำนวนคู่ที่แข่งแล้วได้โดยไม่พัง

ผล:
- หน้า Event กลับมาเปิดได้
- ส่วน "การแข่งขันในอีเว้นท์นี้" ยังแสดงรายการที่สร้างแล้วได้ตามเดิม
