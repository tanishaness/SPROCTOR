# Backend/Offline-capabilities/model_training.py

import torch
import torch.nn as nn
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models import resnet50
import cv2
import numpy as np
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from pathlib import Path
import os

class ExamDataset(Dataset):
    def __init__(self, image_paths, annotations, transform=None):
        """
        Dataset class for exam monitoring images
        
        Args:
            image_paths (list): List of paths to images
            annotations (list): List of dictionaries containing boxes and labels
            transform (callable, optional): Optional transform to be applied on images
        """
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

class SPROCTORModelTrainer:
    def __init__(self, data_dir=None, known_faces_path=None):
        """
        Initialize the SPROCTOR model trainer
        
        Args:
            data_dir (str): Path to the dataset directory
            known_faces_path (str): Path to known faces database
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.data_dir = Path(data_dir) if data_dir else Path('Backend/Dataset')
        self.known_faces = self._load_known_faces(known_faces_path)
        
        # Initialize models
        self.initialize_models()
        
    def _load_known_faces(self, known_faces_path):
        """Load known faces database"""
        if known_faces_path and os.path.exists(known_faces_path):
            return pd.read_csv(known_faces_path)
        return pd.DataFrame()  # Empty DataFrame if no database exists
        
    def initialize_models(self):
        """Initialize FRCNN and Face Recognition models"""
        # Initialize FRCNN for behavior detection
        self.frcnn = fasterrcnn_resnet50_fpn(pretrained=True)
        num_classes = 3  # background, cheating, not_cheating
        in_features = self.frcnn.roi_heads.box_predictor.cls_score.in_features
        self.frcnn.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        
        # Initialize CNN for face recognition
        self.face_cnn = resnet50(pretrained=True)
        num_features = self.face_cnn.fc.in_features
        self.face_cnn.fc = nn.Linear(num_features, len(self.known_faces))
        
        # Move models to device
        self.frcnn.to(self.device)
        self.face_cnn.to(self.device)
        
    def prepare_data_loaders(self, train_ratio=0.8):
        """Prepare train and validation data loaders"""
        # Load and split dataset
        image_paths = list(self.data_dir.glob('images/*.jpg'))
        annotations_path = self.data_dir / 'annotations.json'
        
        if not annotations_path.exists():
            raise FileNotFoundError(f"Annotations file not found at {annotations_path}")
            
        # Load annotations
        import json
        with open(annotations_path) as f:
            annotations = json.load(f)
            
        # Split dataset
        num_train = int(len(image_paths) * train_ratio)
        train_paths = image_paths[:num_train]
        train_annotations = annotations[:num_train]
        val_paths = image_paths[num_train:]
        val_annotations = annotations[num_train:]
        
        # Create transforms
        transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Create datasets
        train_dataset = ExamDataset(train_paths, train_annotations, transform)
        val_dataset = ExamDataset(val_paths, val_annotations, transform)
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=2,
            shuffle=True,
            collate_fn=self.collate_fn
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=2,
            shuffle=False,
            collate_fn=self.collate_fn
        )
        
        return train_loader, val_loader
        
    @staticmethod
    def collate_fn(batch):
        """Custom collate function for data loader"""
        images = []
        targets = []
        for image, target in batch:
            images.append(image)
            targets.append(target)
        return images, targets
        
    def train_models(self, num_epochs=10, learning_rate=0.005):
        """Train both FRCNN and Face Recognition models"""
        # Prepare data loaders
        train_loader, val_loader = self.prepare_data_loaders()
        
        # Optimizers
        frcnn_params = [p for p in self.frcnn.parameters() if p.requires_grad]
        face_params = [p for p in self.face_cnn.parameters() if p.requires_grad]
        
        frcnn_optimizer = torch.optim.SGD(frcnn_params, lr=learning_rate, momentum=0.9)
        face_optimizer = torch.optim.Adam(face_params, lr=learning_rate)
        
        # Training loop
        for epoch in range(num_epochs):
            # Train FRCNN
            self.frcnn.train()
            total_loss = 0
            
            for images, targets in train_loader:
                images = [image.to(self.device) for image in images]
                targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]
                
                frcnn_optimizer.zero_grad()
                loss_dict = self.frcnn(images, targets)
                losses = sum(loss for loss in loss_dict.values())
                
                losses.backward()
                frcnn_optimizer.step()
                
                total_loss += losses.item()
            
            # Validate
            self.frcnn.eval()
            val_loss = 0
            
            with torch.no_grad():
                for images, targets in val_loader:
                    images = [image.to(self.device) for image in images]
                    targets = [{k: v.to(self.device) for k, v in t.items()} for t in targets]
                    
                    loss_dict = self.frcnn(images, targets)
                    losses = sum(loss for loss in loss_dict.values())
                    val_loss += losses.item()
            
            print(f"Epoch [{epoch+1}/{num_epochs}]")
            print(f"Training Loss: {total_loss/len(train_loader):.4f}")
            print(f"Validation Loss: {val_loss/len(val_loader):.4f}")
            
    def save_models(self, frcnn_path='models/frcnn.pth', face_cnn_path='models/face_cnn.pth'):
        """Save trained models"""
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save models
        torch.save(self.frcnn.state_dict(), frcnn_path)
        torch.save(self.face_cnn.state_dict(), face_cnn_path)
        
    def load_models(self, frcnn_path='models/frcnn.pth', face_cnn_path='models/face_cnn.pth'):
        """Load trained models"""
        if os.path.exists(frcnn_path):
            self.frcnn.load_state_dict(torch.load(frcnn_path))
        if os.path.exists(face_cnn_path):
            self.face_cnn.load_state_dict(torch.load(face_cnn_path))

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