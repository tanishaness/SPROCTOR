import torch
import torch.nn as nn
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models import resnet50
import cv2
import numpy as np
from torch.utils.data import Dataset, DataLoader
import pandas as pd

class ExamDataset(Dataset):
    def __init__(self, image_paths, annotations, transform=None):
        self.image_paths = image_paths
        self.annotations = annotations
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
        
    def __getitem__(self, idx):
        # Load image
        image = cv2.imread(self.image_paths[idx])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Get annotations
        boxes = self.annotations[idx]['boxes']
        labels = self.annotations[idx]['labels']
        
        if self.transform:
            image = self.transform(image)
            
        target = {
            'boxes': torch.FloatTensor(boxes),
            'labels': torch.LongTensor(labels)
        }
        
        return image, target

class InvigilationSystem:
    def __init__(self):
        # Initialize FRCNN for student detection and behavior analysis
        self.frcnn = fasterrcnn_resnet50_fpn(pretrained=True)
        num_classes = 3  # background, cheating, not_cheating
        in_features = self.frcnn.roi_heads.box_predictor.cls_score.in_features
        self.frcnn.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        
        # Initialize CNN for face recognition
        self.face_cnn = resnet50(pretrained=True)
        num_features = self.face_cnn.fc.in_features
        self.face_cnn.fc = nn.Linear(num_features, len(self.known_faces))
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.frcnn.to(self.device)
        self.face_cnn.to(self.device)

    def train_models(self, train_loader, num_epochs=10):
        # Training parameters
        params = [p for p in self.frcnn.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
        
        for epoch in range(num_epochs):
            self.frcnn.train()
            total_loss = 0
            
            for images, targets in train_loader:
                images = [image.to(self.device) for image in images]
                targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]
                
                loss_dict = self.frcnn(images, targets)
                losses = sum(loss for loss in loss_dict.values())
                
                optimizer.zero_grad()
                losses.backward()
                optimizer.step()
                
                total_loss += losses.item()
                
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/len(train_loader):.4f}")

    def process_frame(self, frame):
        self.frcnn.eval()
        self.face_cnn.eval()
        
        # Transform frame
        transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        
        frame_tensor = transform(frame).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            predictions = self.frcnn(frame_tensor)
            
        # Process predictions
        boxes = predictions[0]['boxes'].cpu().numpy()
        scores = predictions[0]['scores'].cpu().numpy()
        labels = predictions[0]['labels'].cpu().numpy()
        
        results = []
        for box, score, label in zip(boxes, scores, labels):
            if score > 0.5:  # Confidence threshold
                x1, y1, x2, y2 = box.astype(int)
                face_crop = frame[y1:y2, x1:x2]
                
                # Face recognition
                face_tensor = transform(face_crop).unsqueeze(0).to(self.device)
                face_prediction = self.face_cnn(face_tensor)
                student_id = torch.argmax(face_prediction).item()
                
                results.append({
                    'box': box,
                    'score': score,
                    'is_cheating': label == 1,
                    'student_id': student_id
                })
                
        return results

    def generate_report(self, results):
        report_data = []
        for result in results:
            report_data.append({
                'timestamp': pd.Timestamp.now(),
                'student_id': result['student_id'],
                'confidence': result['score'],
                'behavior': 'Suspicious' if result['is_cheating'] else 'Normal'
            })
        
        df = pd.DataFrame(report_data)
        df.to_excel('invigilation_report.xlsx', index=False)
        return df

class FastRCNNPredictor(nn.Module):
    def __init__(self, in_channels, num_classes):
        super(FastRCNNPredictor, self).__init__()
        self.cls_score = nn.Linear(in_channels, num_classes)
        self.bbox_pred = nn.Linear(in_channels, num_classes * 4)

    def forward(self, x):
        if x.dim() == 4:
            torch.flatten(x, start_dim=1)
        scores = self.cls_score(x)
        bbox_deltas = self.bbox_pred(x)
        return scores, bbox_deltas