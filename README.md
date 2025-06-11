# Meta AI Auto Generator

สคริปต์ Python นี้ใช้ Selenium เพื่อเข้าสู่ระบบเว็บไซต์ [Meta AI](https://www.meta.ai) โดยอัตโนมัติ และทำการสร้างภาพ/วิดีโอจากข้อความที่กำหนด พร้อมดาวน์โหลดมาเก็บไว้ในเครื่อง

## 🧰 Features

* ล็อกอิน Meta AI โดยใช้ Selenium
* ป้อนข้อความ (Prompt) ลงในกล่องข้อความของ Meta AI
* ดาวน์โหลดภาพและวิดีโอที่สร้างขึ้นโดยอัตโนมัติ
* จัดเก็บไฟล์ไว้ในโฟลเดอร์ `genarate_video`

## 🛠️ Requirements

* Python 3.8+
* Google Chrome ติดตั้งในระบบ
* ChromeDriver (จัดการโดย `webdriver_manager`)

### Python Dependencies

ติดตั้งด้วยคำสั่ง:

```bash
pip install selenium webdriver-manager requests
```

## ⚙️ Settings

โปรแกรมจะสร้างไฟล์ `settings.json` อัตโนมัติหากไม่มีอยู่ โดยมีโครงสร้างดังนี้:

```json
{
  "username": "your_meta_email",
  "password": "your_meta_password",
  "headless": false
}
```

* `headless`: หากตั้งค่าเป็น `true` จะไม่แสดงหน้าต่าง Chrome

## ▶️ How to Run

1. ตั้งค่า `settings.json` ด้วยข้อมูลที่ถูกต้อง
2. รันโปรแกรมด้วยคำสั่ง:

```bash
python main.py
```

3. โปรแกรมจะ:

   * ล็อกอิน Meta AI
   * ป้อนข้อความ `"pig flying with children to the moon"`
   * ดาวน์โหลดรูปภาพและวิดีโอที่สร้างโดย Meta AI
   * บันทึกไฟล์ไว้ใน `genarate_video/`

## 📁 Output

* รูปภาพ: `genarate_video/image_0.png` ถึง `image_3.png`
* วิดีโอ: `genarate_video/video_0.mp4` ถึง `video_3.mp4`

## 🧹 Clear Cache

สามารถล้างไฟล์ในโฟลเดอร์ได้โดยใช้ฟังก์ชัน `delete_files_in_directory(folder_path)`

## 🚨 Notes

* สคริปต์อาศัยตำแหน่งขององค์ประกอบในหน้าเว็บ (index) ซึ่งอาจเปลี่ยนได้หาก Meta ปรับ UI
* อาจต้องแก้ตำแหน่ง index หากเกิด error ในอนาคต

## 📜 License

This project is for educational purposes only.

