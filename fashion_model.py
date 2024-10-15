# fashion_model.py
from ultralytics import YOLO
import cv2
import os


class FashionDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image_path):
        pred_img = self.model.predict(image_path, device='cpu')

        # Load image for drawing boxes
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        detected_items = []  # List to store detected item names
        for result in pred_img:
            objects = result.names
            for box in result.boxes:
                _, _, _, _, _, obj_key = box.data[0].tolist()
                detected_items.append(objects[int(obj_key)])  # Add detected item to the list
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
                cv2.putText(image, objects[int(obj_key)], (x1, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Save the result image
        result_path = os.path.join('static/upload', os.path.basename(image_path))
        cv2.imwrite(result_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        return result_path, list(set(detected_items))  # Return the result path and unique detected items


