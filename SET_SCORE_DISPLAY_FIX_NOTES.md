# Set Score Display Fix

ปรับการแสดงผลคะแนนรายเซต ไม่ให้โชว์ JSON ดิบในหน้ารายการแข่งขัน

## แก้ไข

- เพิ่ม helper `set_score_rows(match)` เพื่อแปลง `set_scores` จาก JSON เป็นรายการอ่านง่ายสำหรับ template
- ส่ง `set_score_rows` และ `set_point_totals` เข้า Jinja context
- ปรับ `templates/round_robin/detail.html`
  - จากเดิมแสดง `[{"set":1,"a":15,"b":0}, ...]`
  - เปลี่ยนเป็น badge เช่น `S1 15–0`, `S2 15–0`
  - แสดงผลรวมเซต เช่น `2 - 0 เซต`
  - แสดงแต้มรวม เช่น `แต้มรวม 30–0`
- ปรับ `templates/knockout/detail.html` ให้แสดงคะแนนรายเซตแบบเดียวกัน
- เพิ่ม CSS class สำหรับ set score chip ใน `static/css/app.css`

## ตัวอย่างหน้าจอใหม่

- ผล: `2 - 0 เซต`
- คะแนนรายเซต: `S1 15–0` `S2 15–0`
- แต้มรวม: `30–0`
