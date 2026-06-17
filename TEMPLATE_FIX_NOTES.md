# Template Fix Notes

แก้บั๊ก Jinja TemplateSyntaxError ใน `templates/contests/detail.html`

## สาเหตุ
Jinja ไม่รองรับ syntax แบบ Python format ตรง ๆ เช่น:

```jinja2
{{ cr.max_score:g }}
```

จึงทำให้เกิด error:

```text
jinja2.exceptions.TemplateSyntaxError: expected token 'end of print statement', got ':'
```

## แก้ไข
เปลี่ยนเป็น Jinja filter:

```jinja2
{{ "%g"|format(cr.max_score or 0) }}
```

## ตรวจแล้ว
- Compile template ทุกไฟล์ด้วย Jinja2: ผ่าน
- `python3 -m py_compile app.py models.py`: ผ่าน
