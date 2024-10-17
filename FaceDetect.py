import cv2
from mtcnn import MTCNN
import time
import os

# สร้างตัวตรวจจับ MTCNN
detector = MTCNN()

# เปิดการเชื่อมต่อกับกล้อง (ใช้ 0 สำหรับกล้องเริ่มต้น)
cap = cv2.VideoCapture(1)

# ตรวจสอบว่ากล้องสามารถเปิดได้หรือไม่
if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

# สร้างโฟลเดอร์สำหรับเก็บภาพ
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# รายชื่อผู้ใช้
names = ["First", "FhorFon"]  # เพิ่มชื่อที่ต้องการที่นี่
print("ผู้ใช้ที่มีอยู่:")
for index, name in enumerate(names, start=1):
    print(f"{index}: {name}")

# ตัวแปรสำหรับการถ่ายภาพ
capture_interval = 1  # หน่วงเวลาในการจับภาพ (วินาที)
last_capture_time = 0  # เวลาในการจับภาพล่าสุด
capture_enabled = False  # ตัวแปรสำหรับเปิด/ปิดการจับภาพ
name_index = 0  # ดัชนีชื่อปัจจุบัน
capture_count = 1  # ตัวแปรนับจำนวนภาพที่ถ่ายสำหรับแต่ละคน
ready_to_capture = False  # ตัวแปรสำหรับระบุว่าพร้อมถ่ายภาพหรือไม่

print("กด 'c' เพื่อเริ่มจับภาพ, 's' เพื่อหยุดการจับภาพ, 'n' เพื่อเปลี่ยนคน, 'q' เพื่อออก")

while True:
    # อ่านเฟรมจากกล้อง
    ret, frame = cap.read()

    # ถ้าไม่สามารถอ่านเฟรมได้ ให้ออกจากลูป
    if not ret:
        print("ไม่สามารถรับภาพจากกล้องได้")
        break

    frame = cv2.flip(frame, 1)

    # สร้างสำเนาของเฟรมต้นฉบับเพื่อบันทึก
    original_frame = frame.copy()  # สำเนาเฟรมที่ไม่มีกระบวนการวาดกรอบ

    # ตรวจจับใบหน้าในเฟรม (ผลลัพธ์จะเป็นรายการของใบหน้า)
    faces = detector.detect_faces(frame)

    # วาดกรอบสี่เหลี่ยมรอบใบหน้าที่ตรวจจับได้ เฉพาะในการแสดงผล
    if len(faces) > 0:
        for face in faces:
            x, y, width, height = face['box']
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)  # วาดกรอบสีเขียว

    # แสดงเฟรมที่ตรวจจับใบหน้าแล้ว
    cv2.imshow('MTCNN Face Detection', frame)

    # ถ้ามีการจับภาพ เปิดใช้งานถ่ายภาพทุกๆ 1 วินาที
    if capture_enabled and ready_to_capture:
        current_time = time.time()
        if current_time - last_capture_time >= capture_interval:
            if len(faces) > 0:  # ตรวจสอบว่ามีใบหน้าหรือไม่
                selected_name = names[name_index]  # เลือกชื่อจากรายการตามดัชนี
                full_filename = f"{output_folder}/{capture_count}_{selected_name}.jpg"  # ปรับชื่อไฟล์
                cv2.imwrite(full_filename, original_frame)  # บันทึกภาพต้นฉบับ
                print(f"บันทึกภาพ: {full_filename}")
                last_capture_time = current_time  # อัปเดตเวลา
                capture_count += 1  # เพิ่มจำนวนภาพที่บันทึก

    # ตรวจสอบการกดปุ่ม
    key = cv2.waitKey(1) & 0xFF

    # กด 'c' เพื่อเริ่มจับภาพ
    if key == ord('c') and not capture_enabled:
        capture_enabled = True  # เปิดการจับภาพ
        last_capture_time = time.time()  # อัปเดตเวลาเริ่มต้นจับภาพ
        ready_to_capture = True  # ตั้งค่าว่าพร้อมจับภาพ
        print(f"เริ่มจับภาพ {names[name_index]} ทุกๆ 1 วินาที")

    # กด 's' เพื่อหยุดการจับภาพ
    if key == ord('s') and capture_enabled:
        capture_enabled = False  # ปิดการจับภาพ
        ready_to_capture = False  # ตั้งค่าหยุดจับภาพ
        print(f"หยุดจับภาพ {names[name_index]}")

    # กดปุ่ม 'n' เพื่อเปลี่ยนคน
    if key == ord('n'):
        if capture_enabled:
            capture_enabled = False  # ปิดการจับภาพ
            ready_to_capture = False  # หยุดจับภาพก่อนเปลี่ยนคน
        name_index = (name_index + 1) % len(names)  # เปลี่ยนไปยังชื่อถัดไป
        capture_count = 1  # รีเซ็ตนับจำนวนภาพ
        print(f"เปลี่ยนไปถ่ายภาพ {names[name_index]}")

    # กด 'q' เพื่อออกจากลูป
    if key == ord('q'):
        break

# ปิดการเชื่อมต่อกล้องและทำลายหน้าต่างทั้งหมด
cap.release()
cv2.destroyAllWindows()
