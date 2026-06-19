# PUBLIC PROMO + SUPER ADMIN UPDATE

## สิ่งที่เพิ่ม

### 1) หน้าโปรโมท/แนะนำระบบในโปรแกรม
- เปลี่ยนหน้า `/` สำหรับผู้ที่ยังไม่ล็อกอินให้เป็นหน้าแนะนำระบบ KRURUK SPORTS แทนการเด้งเข้า Login ทันที
- เพิ่มหน้า `/features` ใช้หน้าแนะนำระบบเดียวกัน
- เพิ่มหน้า `/guide` สำหรับอธิบายวิธีใช้งานแบบเข้าใจง่าย
- เพิ่มหน้าในระบบ `/about-system` ให้ผู้ใช้ที่ล็อกอินแล้วกลับมาอ่านภาพรวมและคู่มือได้

เนื้อหาที่ใส่ในโปรแกรม:
- จุดเด่นของระบบ
- วิธีใช้งาน 5 ขั้นตอน
- สิทธิ์การใช้งานหลายระดับ
- ช่องทางติดต่อผู้พัฒนา: ครูรัก, niyomp@kkumail.com, @niyomp
- ป้ายช่วงทดลองใช้

### 2) หน้า Super Admin Management
เพิ่มเมนูและ route:
- `/super-admin` ศูนย์บริหารระบบรวม
- `/super-admin/users` จัดการผู้ใช้และสิทธิ์องค์กร

Super Admin ทำได้:
- ดูจำนวนองค์กร ผู้ใช้ งานแข่งขัน และ subscription active
- ดูงานล่าสุด ผู้ใช้ล่าสุด และแพ็กเกจ
- เปลี่ยน role ผู้ใช้: superadmin, organization_admin, event_admin, viewer
- ผูกผู้ใช้กับองค์กร
- ลบสิทธิ์ผู้ใช้ในองค์กร

### 3) สิทธิ์ผู้ใช้
- Super Admin เห็นทุกองค์กรและทุกงาน
- ผู้สมัคร/organization admin เห็นเฉพาะองค์กรที่ตนเองเป็นสมาชิก
- ระบบเดิมที่ filter ด้วย `user_org_ids()` และ `can_access_org()` ยังทำงานเหมือนเดิม

### 4) Sidebar
เพิ่มเมนู:
- แนะนำระบบ/คู่มือ
- Super Admin
- Users

### 5) Styling
เพิ่ม CSS สำหรับ:
- public landing page
- guide page
- super admin dashboard
- user management table

## ตรวจสอบแล้ว
- `python3 -m py_compile app.py models.py extensions.py forms.py` ผ่าน
- Jinja template parse ผ่าน
- Local default port ยังคงใช้ 5050
