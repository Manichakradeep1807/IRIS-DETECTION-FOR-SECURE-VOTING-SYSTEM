# Iris Recognition Deep Learning System - Installation Guide

## 🎯 Overview
This guide will help you set up the full deep learning functionality for the Iris Recognition system.

## ⚠️ Important Note
**TensorFlow/Keras requires Python 3.11 or 3.12**. Python 3.13 is not yet supported.

## 📋 Prerequisites
- Windows 10/11
- Python 3.11 or 3.12 installed
- At least 4GB RAM
- 2GB free disk space

## 🚀 Quick Setup (Recommended)

### Option 1: Automatic Setup
1. **Download Python 3.11**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.11.9 (recommended)
   - During installation, check "Add Python to PATH"

2. **Run the setup script**:
   ```bash
   # Double-click or run in command prompt:
   setup_python311.bat
   ```

3. **Run the application**:
   ```bash
   # Double-click or run:
   run_iris_recognition.bat
   ```

### Option 2: Manual Setup
1. **Install Python 3.11**
2. **Create virtual environment**:
   ```bash
   py -3.11 -m venv iris_env
   iris_env\Scripts\activate.bat
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python Main.py
   ```

## 🧪 Testing the System

### 1. Create Sample Dataset
```bash
# After activating the environment:
python create_sample_dataset.py
```

### 2. Test the GUI
1. Click "Upload Iris Dataset" - select the `sample_dataset` folder
2. Click "Generate & Load CNN Model" - this will train the model
3. Click "Accuracy & Loss Graph" - view training progress
4. Click "Upload Iris Test Image & Recognize" - test recognition

## 📁 File Structure
```
mini project/
├── Main.py                    # Main application
├── requirements.txt           # Python dependencies
├── setup_python311.bat       # Automatic setup script
├── run_iris_recognition.bat   # Run script
├── create_sample_dataset.py   # Dataset generator
├── create_sample_image.py     # Sample image creator
├── model/                     # Model files (created automatically)
├── testSamples/              # Test images
├── sample_dataset/           # Training dataset (created by script)
└── iris_env/                 # Virtual environment (created by setup)
```

## 🔧 Features Available

### ✅ With Python 3.11/3.12:
- Full CNN deep learning model
- Real iris recognition
- Model training and saving
- Accuracy graphs from real training data
- Voting system with person identification

### ⚠️ With Python 3.13:
- GUI interface only
- Iris feature extraction
- Demo/simulated recognition
- Basic functionality

## 🐛 Troubleshooting

### Common Issues:

1. **"Python 3.11 not found"**
   - Install Python 3.11 from python.org
   - Make sure "Add to PATH" was checked during installation

2. **"TensorFlow installation failed"**
   - Make sure you're using Python 3.11 or 3.12
   - Try: `pip install --upgrade pip` first

3. **"Virtual environment creation failed"**
   - Run command prompt as Administrator
   - Make sure you have write permissions

4. **"Model training is slow"**
   - This is normal for CPU training
   - Consider reducing epochs in the code for faster testing

### Performance Tips:
- Close other applications during model training
- Use SSD storage for better performance
- Consider using GPU version of TensorFlow for faster training

## 📞 Support
If you encounter issues:
1. Check that you're using Python 3.11 or 3.12
2. Ensure all dependencies are installed correctly
3. Try running the setup script as Administrator

## 🎉 Success Indicators
When everything is working correctly, you should see:
- GUI opens without errors
- Model training shows progress in console
- Accuracy graphs display real training data
- Iris recognition provides actual predictions
- Voting system tracks recognized persons

Enjoy your fully functional Iris Recognition system! 🚀
