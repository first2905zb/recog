import os
import cv2
from mtcnn import MTCNN

# กำหนดโฟลเดอร์ที่มีรูปภาพและโฟลเดอร์สำหรับบันทึก labels
image_folder = 'dataset/images'
label_folder = 'dataset/labels'

# สร้างโฟลเดอร์สำหรับบันทึก labels ถ้ายังไม่มี
os.makedirs(label_folder, exist_ok=True)

# สร้างตัวตรวจจับใบหน้า MTCNN
detector = MTCNN()

# โหลด haarcascade สำหรับการตรวจจับใบหน้า
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# วนลูปผ่านไฟล์ในโฟลเดอร์
for image_file in os.listdir(image_folder):
    if image_file.endswith(('.jpg', '.jpeg', '.png')):
        # โหลดรูปภาพ
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)

        # ตรวจจับใบหน้าด้วย MTCNN
        results = detector.detect_faces(image)

        # สร้างชื่อไฟล์ label
        label_file_name = os.path.splitext(image_file)[0] + '.txt'
        label_file_path = os.path.join(label_folder, label_file_name)

        # รับ class_id จากชื่อไฟล์
        class_id = 0  # สามารถเพิ่มเงื่อนไขตามชื่อไฟล์ได้ที่นี่
        if 'Fahfon' in image_file:
            class_id = 0
        elif 'First' in image_file:
            class_id = 1
        elif 'J' in image_file:
            class_id = 2
        elif 'Muay' in image_file:
            class_id = 3
        elif 'Nine' in image_file:
            class_id = 4

        # เปิดไฟล์ label สำหรับเขียน
        with open(label_file_path, 'w') as f:
            # ถ้า MTCNN ไม่พบใบหน้า ลองใช้ haarcascade
            if not results:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = haar_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # ถ้าพบใบหน้าโดย haarcascade
                if len(faces) > 0:
                    # เลือกใบหน้าที่ใหญ่ที่สุด
                    largest_face = max(faces, key=lambda face: face[2] * face[3])
                    (x, y, w, h) = largest_face

                    # คำนวณพิกัดตามสัดส่วน
                    x_center = (x + w / 2) / image.shape[1]
                    y_center = (y + h / 2) / image.shape[0]
                    width = w / image.shape[1]
                    height = h / image.shape[0]

                    # เขียนข้อมูลลงในไฟล์
                    f.write(f'{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
                else:
                    f.write('No faces detected\n')
            else:
                # เลือกใบหน้าที่ใหญ่ที่สุดจาก MTCNN
                largest_face = max(results, key=lambda result: result['box'][2] * result['box'][3])
                bounding_box = largest_face['box']

                # คำนวณพิกัดตามสัดส่วน
                x_center = (bounding_box[0] + bounding_box[2] / 2) / image.shape[1]
                y_center = (bounding_box[1] + bounding_box[3] / 2) / image.shape[0]
                width = bounding_box[2] / image.shape[1]
                height = bounding_box[3] / image.shape[0]

                # เขียนข้อมูลลงในไฟล์
                f.write(f'{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')

        print(f'Annotations saved for {image_file} to {label_file_path}')

print('All annotations saved successfully.')
