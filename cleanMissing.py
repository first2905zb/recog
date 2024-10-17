import os
import shutil

# กำหนดเส้นทางของโฟลเดอร์
image_folder = 'dataset/images'
label_folder = 'dataset/labels'
result_image_folder = 'result/images'
result_label_folder = 'result/labels'

# สร้างโฟลเดอร์ผลลัพธ์ถ้ายังไม่มี
os.makedirs(result_image_folder, exist_ok=True)
os.makedirs(result_label_folder, exist_ok=True)

# วนลูปผ่านไฟล์ annotation ในโฟลเดอร์ labels
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):
        label_file_path = os.path.join(label_folder, label_file)

        # ตรวจสอบว่ามีข้อมูลใบหน้าหรือไม่
        with open(label_file_path, 'r') as f:
            lines = f.readlines()
            # ถ้ามีบรรทัดข้อมูลใบหน้า (ไม่ใช่ "No faces detected")
            if len(lines) > 0 and lines[0].strip() != 'No faces detected':
                # คัดลอกไฟล์รูปภาพไปยังโฟลเดอร์ผลลัพธ์
                image_file = os.path.splitext(label_file)[0] + '.jpg'  # เปลี่ยน .jpg ตามนามสกุลไฟล์ของคุณ
                image_file_path = os.path.join(image_folder, image_file)

                # คัดลอกไฟล์รูปภาพถ้ามีอยู่
                if os.path.exists(image_file_path):
                    shutil.copy(image_file_path, result_image_folder)

                # คัดลอกไฟล์ annotation ไปยังโฟลเดอร์ผลลัพธ์
                shutil.copy(label_file_path, result_label_folder)

print('Completed copying files to the result folders.')
