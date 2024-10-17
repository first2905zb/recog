import os
from PIL import Image, ImageEnhance

# กำหนดโฟลเดอร์ที่เก็บรูปต้นฉบับและโฟลเดอร์ที่จะเก็บรูปที่ประมวลผลแล้ว
input_folder = 'output'
output_folder = 'dataset/images'

# สร้างโฟลเดอร์ output หากยังไม่มี
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ฟังก์ชันในการประมวลผลรูปภาพ
def process_image(image_path, image_name):
    # เปิดรูปภาพ
    img = Image.open(image_path)

    # บันทึกรูปต้นฉบับ
    original_image_path = os.path.join(output_folder, f"{image_name}_original.jpg")
    img.save(original_image_path)

    # ปรับขนาดภาพสำหรับ ESP32-CAM (QVGA 320x240)
    qvga_image = img.resize((320, 240))
    qvga_image.save(os.path.join(output_folder, f"{image_name}_qvga_320x240.jpg"))

    # ปรับขนาดภาพสำหรับ ESP32-CAM (VGA 640x480)
    vga_image = img.resize((640, 480))
    vga_image.save(os.path.join(output_folder, f"{image_name}_vga_640x480.jpg"))

    # หมุนรูปภาพ 90, 180, 270 องศา
    rotations = [90, 180, 270]
    for angle in rotations:
        rotated_image = img.rotate(angle, expand=True)
        rotated_image.save(os.path.join(output_folder, f"{image_name}_rotated_{angle}.jpg"))

    # Flip รูปภาพ
    flipped_image = img.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_image.save(os.path.join(output_folder, f"{image_name}_flipped.jpg"))

    # เพิ่ม Brightness/Contrast
    enhancer = ImageEnhance.Brightness(img)
    for brightness_factor in [0.5, 1.5]:  # ลดและเพิ่มความสว่าง
        bright_image = enhancer.enhance(brightness_factor)
        bright_image.save(os.path.join(output_folder, f"{image_name}_brightness_{brightness_factor}.jpg"))

    enhancer = ImageEnhance.Contrast(img)
    for contrast_factor in [0.5, 1.5]:  # ลดและเพิ่มคอนทราสต์
        contrast_image = enhancer.enhance(contrast_factor)
        contrast_image.save(os.path.join(output_folder, f"{image_name}_contrast_{contrast_factor}.jpg"))

# ประมวลผลทุกรูปภาพในโฟลเดอร์ input
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # ตรวจสอบนามสกุลของไฟล์
        image_path = os.path.join(input_folder, filename)
        process_image(image_path, os.path.splitext(filename)[0])  # ส่งชื่อไฟล์โดยไม่รวม .jpg

print("ประมวลผลภาพเสร็จสิ้น!")
