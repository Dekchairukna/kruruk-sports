# Phase 13D Sports Real Settings + Knockout Continuation

## ปรับข้อมูลกีฬาให้ตรงกับชนิดกีฬาจริง
ปุ่ม “สร้าง/อัปเดตชุดกีฬาให้ถูกชนิด” ในหน้า Sport Setup จะสร้างและซ่อมข้อมูลเดิมโดยไม่ลบผลการแข่งขันเก่า

### Mapping หลัก
- กรีฑา: `ranking` + `ranking` สำหรับบันทึกอันดับ/เวลา
- กีฬาพื้นบ้าน เช่น ชักเย่อ วิ่งกระสอบ วิ่งสามขา วิ่งเปี้ยว: `ranking` + `ranking`
- ฟุตบอล / ฟุตซอล: `round_robin` + `score_only` สำหรับประตูได้-เสีย
- วอลเลย์บอล: `round_robin` + `set_based`, 5 เซต, 25 แต้ม, ชนะ 3 เซต
- เซปักตะกร้อ: `round_robin` + `set_based`, 3 เซต, 21 แต้ม, ชนะ 2 เซต
- เปตอง: `knockout` + `score_only`
- แบดมินตัน: `knockout` + `set_based`, 3 เกม, 21 แต้ม, ชนะ 2 เกม
- เทเบิลเทนนิส: `knockout` + `set_based`, 5 เกม, 11 แต้ม, ชนะ 3 เกม

## เพิ่มส่วนที่ยังขาด
- เพิ่มโมเดล `KnockoutCompetition` และ `KnockoutMatch`
- เพิ่มหน้า Knockout List / Detail
- เปิดปุ่ม “สร้างรอบ Knockout ต่อ” จากหน้า Round Robin แล้ว
- ระบบจับคู่ทีมเข้ารอบแบบ 1 พบอันดับท้ายสุด, 2 พบรองท้ายสุด
- บันทึกผล Knockout ได้ทั้ง `score_only` และ `set_based`
- เมื่อบันทึกครบทุกคู่ ระบบสร้างรอบถัดไปให้อัตโนมัติจนถึงชิงชนะเลิศ

## Super Admin / Bugfix เดิมยังอยู่
- Login ID: `superadmin`
- Password: `yagami1225`
- Sidebar Teams / Sport Setup / Billing พาไปหน้าปัจจุบันได้
- Sport Setup แก้ไข หมวดกีฬา / ชนิดกีฬา / รุ่นแข่งขัน ได้
