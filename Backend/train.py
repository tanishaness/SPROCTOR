import os
import torch
from torchvision import transforms
from model_training import InvigilationSystem, ExamDataset

def prepare_dataset(data_dir):
    image_paths = []
    annotations = []
    
    # Load images and annotations from your data directory
    for image_file in os.listdir(os.path.join(data_dir, 'images')):
        if image_file.endswith(('.jpg', '.png')):
            image_paths.append(os.path.join(data_dir, 'images', image_file))
            
            # Load corresponding annotation file
            annotation_file = os.path.join(
                data_dir, 
                'annotations', 
                image_file.replace('.jpg', '.json').replace('.png', '.json')
            )
            with open(annotation_file, 'r') as f:
                annotation = json.load(f)
                annotations.append(annotation)
    
    return image_paths, annotations

def main():
    # Set up data transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    # Prepare dataset
    data_dir = 'path/to/your/dataset'
    image_paths, annotations = prepare_dataset(data_dir)
    
    # Create dataset and dataloader
    dataset = ExamDataset(image_paths, annotations, transform=transform)
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=2,
        shuffle=True,
        collate_fn=lambda x: tuple(zip(*x))
    )
    
    # Initialize and train the model
    system = InvigilationSystem()
    system.train_models(dataloader, num_epochs=10)
    
    # Save the trained model
    torch.save({
        'frcnn_state_dict': system.frcnn.state_dict(),
        'face_cnn_state_dict': system.face_cnn.state_dict()
    }, 'invigilation_model.pth')

if __name__ == '__main__':
    main()