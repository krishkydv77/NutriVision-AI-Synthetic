 # NutriVision-AI

## AI-Powered Food & Nutrition Analyzer

NutriVision-AI is a Deep Learning-based web application that analyzes food images and provides food classification, estimated nutritional information, and an overall health score.

The project uses two specialized Deep Learning models:

* **CNN (Convolutional Neural Network)** for food image classification
* **ANN (Artificial Neural Network)** for nutrition estimation

The application is built using **FastAPI**, **TensorFlow/Keras**, **Python**, and **Docker**, and has been deployed on **AWS EC2**.

> **Important:** The current models are trained using **synthetically generated/demo training data**, not a real-world food image dataset. The project is intended as a Deep Learning prototype and demonstration of an end-to-end ML deployment workflow.



## Project Overview

NutriVision-AI follows a two-stage Deep Learning pipeline:

```text
Food Image
    ↓
Image Preprocessing
    ↓
CNN Model
    ↓
Food Classification + Confidence
    ↓
ANN Model
    ↓
Nutrition Estimation
    ↓
Health Score
    ↓
JSON Response / Web UI
```

The system takes a food image as input and attempts to identify the food category. The detected food class is then passed to the nutrition estimation model to estimate:

* Calories
* Protein
* Carbohydrates
* Fat

Finally, a custom heuristic function generates a health score between **1 and 10**.

## Key Features

* Food image classification using CNN
* Nutrition estimation using ANN
* Synthetic training data generation for model development
* Calories estimation
* Protein estimation
* Carbohydrates estimation
* Fat estimation
* CNN confidence score
* Custom health score from 1–10
* Image preprocessing using Pillow and NumPy
* REST API using FastAPI
* Automatic API documentation using Swagger/OpenAPI
* Nutrition database fallback mechanism
* Modular service-based architecture
* Dockerized application
* AWS EC2 deployment



## Deep Learning Architecture

### 1. CNN — Food Classification

The CNN model is responsible for identifying the food category from the uploaded image.

### Input

```text
128 × 128 × 3 RGB Image
```

### Architecture

```text
Input (128, 128, 3)
        ↓
Conv2D (32)
        ↓
MaxPooling
        ↓
Conv2D (64)
        ↓
MaxPooling
        ↓
Conv2D (128)
        ↓
MaxPooling
        ↓
Flatten
        ↓
Dense (128)
        ↓
Dropout (0.3)
        ↓
Dense (5, Softmax)
```

### Output

The CNN produces probabilities for the supported food classes.

The class with the highest probability is selected as the predicted food.

### Problem Type

```text
Multi-Class Classification
```

### Loss Function

```text
Categorical Crossentropy
```

The CNN training pipeline currently generates synthetic/random image-like arrays and labels for demonstration purposes rather than using real food images.


## 2. ANN — Nutrition Estimation

The ANN model estimates nutritional values based on the detected food class and portion scale.

### Input

```text
5 Food-Class Features + Portion Scale
```

### Architecture

```text
Input (6)
   ↓
Dense (64, ReLU)
   ↓
Dense (32, ReLU)
   ↓
Dense (16, ReLU)
   ↓
Dense (4)
```

### Output

```text
Calories
Protein
Carbohydrates
Fat
```

### Problem Type

```text
Multi-Output Regression
```

### Loss Function

```text
Mean Squared Error (MSE)
```

The ANN training data is also synthetically generated using food classes, portion-scale variations, and nutrition values from the project's nutrition database.



## Why Two Models?

Two separate models are used because food classification and nutrition estimation are different machine learning problems.

| Model | Purpose              | Input                      | Output                        | Problem        |
| ----- | -------------------- | -------------------------- | ----------------------------- | -------------- |
| CNN   | Food Classification  | Food Image                 | Food Class + Confidence       | Classification |
| ANN   | Nutrition Estimation | Food Class + Portion Scale | Calories, Protein, Carbs, Fat | Regression     |

This modular architecture allows the classification and nutrition components to be developed and improved independently.



## System Architecture

```text
                         USER
                          |
                          v
                    WEB BROWSER
                          |
                    Image Upload
                          |
                          v
                  ┌───────────────┐
                  │    FastAPI    │
                  │    Backend    │
                  └───────┬───────┘
                          |
                          v
                   POST /api/predict
                          |
             ┌────────────┴────────────┐
             |                         |
             v                         v
      Image Preprocessing       Prediction Service
             |                         |
             |                         v
             |                    CNN Model
             |                         |
             |                         v
             |                  Food + Confidence
             |                         |
             |                         v
             |                  Nutrition Service
             |                         |
             |                ┌────────┴────────┐
             |                |                 |
             |                v                 v
             |             ANN Model       Nutrition DB
             |                |
             |                v
             |       Calories / Protein /
             |       Carbs / Fat
             |                |
             └────────────────┘
                          |
                          v
                    Health Score
                          |
                          v
                    JSON Response
                          |
                          v
                       FRONTEND
```



## Application Workflow

### Step 1 — Image Upload

The user uploads a food image through the web interface.

### Step 2 — Image Validation

FastAPI validates the uploaded file and checks whether the content type represents an image.

### Step 3 — Image Preprocessing

The uploaded image goes through the following preprocessing steps:

```text
Raw Image Bytes
      ↓
io.BytesIO
      ↓
Pillow Image
      ↓
RGB Conversion
      ↓
Resize to 128 × 128
      ↓
NumPy Array
      ↓
Normalization /255
      ↓
Batch Dimension
      ↓
(1, 128, 128, 3)
```

### Step 4 — CNN Prediction

The processed image is passed to the CNN model.

The model returns class probabilities.

```text
CNN
 ↓
Class Probabilities
 ↓
Highest Probability
 ↓
Predicted Food
 ↓
Confidence Score
```

### Step 5 — Nutrition Estimation

The detected food class is converted into the required input representation and passed to the ANN.

The ANN estimates:

```text
Calories
Protein
Carbohydrates
Fat
```

### Step 6 — Health Score

A custom heuristic function calculates an overall health score between **1 and 10** based on the estimated nutritional values.

### Step 7 — Final Response

The API returns the final prediction as JSON.


## Example API Response

```json
{
    "food": "Pizza",
    "confidence": 0.965,
    "nutrition": {
        "calories": 285,
        "protein": 12,
        "carbs": 36,
        "fat": 10
    },
    "health_score": 6.5,
    "image_url": "/static/uploads/example.jpg"
}
```

> The values above are an example response format and are not intended to represent medically or nutritionally validated measurements.


## API

### Prediction Endpoint

```text
POST /api/predict
```

### Request

The endpoint accepts an image using:

```text
multipart/form-data
```

### Response

The API returns:

```text
Food
Confidence
Nutrition
Health Score
Image URL
```

### Swagger Documentation

FastAPI provides automatic interactive API documentation:

```text
/docs
```

When running locally:

```text
http://localhost:8000/docs
```


## Tech Stack

| Category             | Technology         |
| -------------------- | ------------------ |
| Programming Language | Python             |
| Backend              | FastAPI            |
| ASGI Server          | Uvicorn            |
| Deep Learning        | TensorFlow / Keras |
| Computer Vision      | CNN                |
| Regression           | ANN                |
| Image Processing     | Pillow             |
| Numerical Computing  | NumPy              |
| Data Processing      | Pandas             |
| Template Engine      | Jinja2             |
| API                  | REST / JSON        |
| Containerization     | Docker             |
| Cloud                | AWS EC2            |
| Model Format         | Keras `.keras`     |


## Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/NutriVision-AI.git
```

```bash
cd NutriVision-AI
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Model Training

The project contains separate training scripts for the CNN and ANN models.

### Train CNN

```bash
python -m training.train_cnn
```

The model is saved as:

```text
models/cnn_model.keras
```

### Train ANN

```bash
python -m training.train_ann
```

The model is saved as:

```text
models/ann_model.keras
```

### Training Data Note

The current training pipeline uses **synthetically generated/demo data**.

For the CNN, random image-like arrays and labels are generated for development and demonstration.

For the ANN, synthetic combinations of food classes and portion scales are generated using the project's nutrition database.

Therefore, the current model should **not be considered a real-world food recognition or clinically accurate nutrition prediction system**.



## Docker Deployment

The application is containerized using Docker.

### Build Docker Image

```bash
docker build -t nutrivision-ai .
```

### Run Container

```bash
docker run -d \
  --name nutrivision-ai \
  -p 8000:8000 \
  nutrivision-ai
```

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker logs nutrivision-ai
```

Stop container:

```bash
docker stop nutrivision-ai
```

Remove container:

```bash
docker rm nutrivision-ai
```


## AWS EC2 Deployment

NutriVision-AI has been deployed on an AWS EC2 instance using Docker.

### Deployment Architecture

```text
                  Internet
                     |
                     v
               AWS EC2 Instance
                     |
                     v
                Docker Engine
                     |
                     v
             NutriVision Container
                     |
                     v
                FastAPI App
                     |
          ┌──────────┴──────────┐
          |                     |
          v                     v
      CNN Model             ANN Model
```

### Deployment Process

```text
Create EC2 Instance
        ↓
Configure Security Group
        ↓
Connect through SSH
        ↓
Install Docker
        ↓
Clone GitHub Repository
        ↓
Build Docker Image
        ↓
Run Docker Container
        ↓
Expose Application Port
        ↓
Access Application
```

The deployed application can be accessed using the EC2 public IP/domain and configured application port.


## Fallback Mechanism

NutriVision-AI contains a fallback mechanism to improve application robustness.

If the trained models cannot be loaded, the application can fall back to predefined nutrition data.

```text
              Prediction Request
                     |
                     v
                Load Model
                     |
              ┌──────┴──────┐
              |             |
            Success        Failure
              |             |
              v             v
         Model Output    Fallback Data
              |             |
              └──────┬──────┘
                     |
                     v
                 Final Result
```

This prevents model-loading failures from immediately breaking the complete application flow.

## Health Score

The application includes a custom heuristic health scoring mechanism.

The score is calculated using nutritional values such as:

* Calories
* Protein
* Carbohydrates
* Fat

The final score is constrained between:

```text
1.0 — 10.0
```

The current health score is **rule-based/heuristic** and is not a medically validated health assessment.


## Learning & Engineering Concepts Demonstrated

This project demonstrates practical implementation of:

* Deep Learning
* CNN-based image classification
* ANN-based regression
* Multi-output regression
* Image preprocessing
* REST API development
* FastAPI
* Model serving
* Modular Python architecture
* Docker containerization
* AWS EC2 deployment
* Error handling and fallback design
* Git and GitHub workflow


## Project Objective

The primary objective of NutriVision-AI is to demonstrate an end-to-end Deep Learning application that combines:

```text
Computer Vision
      +
Deep Learning
      +
REST API
      +
Containerization
      +
Cloud Deployment
```

The current implementation focuses on demonstrating the complete technical pipeline, while future versions can replace the synthetic training data with a real-world food image dataset and real nutritional data.

## Disclaimer

NutriVision-AI is an educational and prototype project.

The food predictions and nutritional values generated by the current system are **estimates only**. The current models are trained using synthetic/demo data and should not be used for medical, dietary, or clinical decision-making.



