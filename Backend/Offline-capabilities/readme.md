# S-Proctor: Offline Exam Proctoring

**S-Proctor** is an AI-based smart proctoring system designed for **offline exams** that ensures fairness, equity, and limited resources during examination by leveraging real-time cheat detection using machine learning and computer vision. The offline proctoring feature enhances its ability to operate even without continuous internet access, making it adaptable to low-infrastructure areas.

---

## **Table of Contents**

- [Overview](#overview)
- [Features](#features)
- [Offline Capabilities](#offline-capabilities)
  - [Local Data Storage (SQLite)](#local-data-storage-sqlite)
  - [Efficient Video Processing](#efficient-video-processing)
  - [Batch Data Syncing](#batch-data-syncing)
  - [Lightweight ML Models (TensorFlow Lite)](#lightweight-ml-models-tensorflow-lite)
  - [Resource Management](#resource-management)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Installation](#installation)
  - [How to Run](#how-to-run)
- [How the Offline Feature Works](#how-the-offline-feature-works)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

---

## **Overview**

**S-Proctor** leverages **machine learning (ML)** algorithms to monitor student behavior during offline exams and detect possible cheating activities using just a device camera. The offline proctoring system stores behavior logs locally when the internet is unavailable and synchronizes them when connectivity is restored.

---

## **Features**

1. **AI-Driven Proctoring:** Automatically monitors student behavior using computer vision and ML algorithms.
2. **Real-Time Cheat Detection:** Continuously assesses behavior to detect suspicious activities.
3. **Offline Proctoring:** Works seamlessly without requiring internet access during the exam.
4. **Efficient Syncing:** Stores data locally and syncs it when internet access is restored.

---

## **Offline Capabilities**

The offline proctoring feature enhances the existing capabilities of S-Proctor by ensuring that exams can be proctored without continuous internet connectivity. The solution involves using **local storage** to store video and behavior logs, optimizing the video processing pipeline, and efficiently syncing data once the connection is restored.

### **Local Data Storage (SQLite)**

The offline mode uses **SQLite** to store behavior logs locally. This enables S-Proctor to continue functioning smoothly in areas with limited or no internet connection.

```python
# Initialize a local SQLite database
def setup_local_database():
    # Creates or connects to an SQLite database to store logs locally
```

Behavior logs, including **student actions** and **cheat probabilities**, are stored in a table and synced later to the server once the connection is restored.

### **Efficient Video Processing**

Video feeds are processed efficiently using **OpenCV**. To reduce the workload and enable real-time analysis even on low-spec machines, only every nth frame is processed, making the system lighter and faster.

```python
# Process video efficiently by only analyzing every nth frame
def process_video_offline(video_source, frame_interval=30):
    # Efficient video processing pipeline
```

This feature ensures that the proctoring system remains responsive, even during offline exams.

### **Batch Data Syncing**

When internet connectivity is restored, the system will sync the stored logs to the server. Until then, logs are kept safe in the local SQLite database.

```python
# Sync data to the server when internet is available
def sync_data_to_server():
    # Automatically syncs logs when the connection is restored
```

The system uses the `ping` method to check for internet connectivity and uploads all pending data once the connection is available.

### **Lightweight ML Models (TensorFlow Lite)**

To ensure the offline feature runs smoothly, **TensorFlow Lite** is used for running lightweight machine learning models that detect cheating. These models are smaller, faster, and work efficiently on local machines, reducing dependency on heavy cloud-based models.

```python
# Load a TensorFlow Lite model for efficient local processing
def load_tflite_model(model_path):
    # Loading lightweight model
```

The optimized models ensure that cheat detection can happen in real-time, even in offline conditions.

### **Resource Management**

The system dynamically adjusts based on available **CPU and memory resources**. This ensures that if resources are limited, the video processing frame rate or resolution is reduced to maintain performance.

```python
# Dynamically adjust processing based on CPU and memory usage
def adjust_processing_based_on_resources():
    # Adjust video processing dynamically
```

---

## **Technologies Used**

- **Python**: The primary language used to implement the offline capabilities.
- **SQLite**: For local storage of data and logs during offline mode.
- **OpenCV**: Used for capturing and processing video frames.
- **MediaPipe**: Employed for facial and gesture recognition.
- **TensorFlow Lite**: Used to run optimized ML models offline.
- **psutil**: For monitoring system resources like CPU and memory usage.

---

## **Setup Instructions**

### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/s-proctor.git
   cd s-proctor
   ```

2. **Install Dependencies**:
   Inside your **GitHub Codespace** or local environment, install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

### **How to Run**

1. **Set Up Local Database**:
   Run the script to initialize the SQLite database.
   ```bash
   python setup_local_db.py
   ```

2. **Run the Proctoring System**:
   Start the offline proctoring feature by running the following command:
   ```bash
   python proctoring_system.py
   ```

3. **Sync Data When Internet is Available**:
   Sync your offline data logs once you’re connected to the internet.
   ```bash
   python sync_data.py
   ```

---

## **How the Offline Feature Works**

1. **Start Exam Monitoring**: When an exam starts, S-Proctor monitors student behavior using the device camera.
2. **Capture and Process Video**: Using **OpenCV**, video feeds are captured and analyzed. Instead of processing every frame, the system processes key frames to balance accuracy and efficiency.
3. **Log Behavior Locally**: All behavior data and cheat probabilities are stored locally in an SQLite database.
4. **Sync Data**: Once the exam is over or the internet connection is restored, all logs are synced to the server.

---

## **Contribution Guidelines**

We welcome contributions to enhance **S-Proctor**. To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add offline-capabilities"`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a pull request.

Ensure your code adheres to the following guidelines:
- Write clear, concise, and commented code.
- Include tests for new features.
- Ensure backward compatibility.

For more details, check out our [contribution guidelines](CONTRIBUTING.md).

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.