# Sidebar toggle overflow fix

- ปรับ `.sidebar-toggle` จาก `width:100%` เป็น `width:calc(100% - 16px)` เพราะเดิมมี margin ซ้าย/ขวา 8px ทำให้ปุ่มล้น sidebar
- เพิ่ม `box-sizing:border-box` และ `padding` ให้ขนาดนิ่ง
- เพิ่มการตั้ง `data-nav-label` อัตโนมัติให้ tooltip ตอน sidebar ย่อเหลือไอคอน
- ปรับ aria-expanded และ icon ย่อ/ขยายให้สัมพันธ์กับสถานะ
