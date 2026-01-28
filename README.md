# 🔍 Advanced Iris Recognition System

A comprehensive biometric iris recognition system with deep learning capabilities and modern GUI.

## 🌟 Features

### Core Functionality
- **🧠 Deep Learning Models**: Advanced CNN architectures with ResNet-inspired design
- **👁️ Iris Recognition**: Real-time biometric identification and verification

- **🎥 Live Recognition**: Real-time video-based iris recognition
- **🗄️ Database Integration**: Persistent storage with SQLite
- **⚡ Performance Monitoring**: Real-time system health and metrics tracking

### Enhanced Capabilities
- **🔄 Data Augmentation**: Specialized augmentation for biometric data
- **📈 Training Visualization**: Real-time training progress and accuracy graphs
- **🔒 Security Features**: Anti-spoofing detection and secure template storage
- **🌐 API Ready**: RESTful API endpoints for integration
- **📱 Modern GUI**: Professional interface with ttk styling

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# 1. Download Python 3.11 or 3.12 from python.org
# 2. Run the setup script:
setup_python311.bat

# 3. Start the application:
run_iris_recognition.bat
```

### Option 2: Manual Setup
```bash
# Create virtual environment
py -3.12 -m venv iris_env
iris_env\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run application
python Main.py
```

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.11 or 3.12 (for full functionality)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Camera**: USB webcam (for live recognition)

### Recommended Requirements
- **Python**: 3.12 with virtual environment
- **RAM**: 16GB for large dataset training
- **GPU**: NVIDIA GPU with CUDA support (optional)
- **Storage**: SSD for better performance

## 🛠️ Installation Guide

### Step 1: Python Installation
1. Download Python 3.12 from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Verify installation: `py --version`

### Step 2: Project Setup
```bash
# Clone or download the project
cd "mini project"

# Check compatibility
python check_compatibility.py

# Run setup (Windows)
setup_python311.bat

# Or manual setup
py -3.12 -m venv iris_env
iris_env\Scripts\activate.bat
pip install -r requirements.txt
```

### Step 3: Initial Configuration
```bash
# Create sample dataset
python create_sample_dataset.py

# Test the system
python Main.py
```

## 📖 Usage Guide

### Basic Workflow
1. **Upload Dataset**: Load training images using "📁 Upload Dataset"
2. **Train Model**: Create CNN model with "🧠 Train/Load Model"

4. **Test Recognition**: Verify system with "🔍 Test Recognition"
5. **Live Recognition**: Start real-time recognition with "📹 Live Recognition"

### Advanced Features

#### Live Video Recognition
```python
from live_recognition import start_live_recognition
start_live_recognition(model=your_model, iris_extractor=getIrisFeatures)
```



#### Performance Monitoring
```python
from performance_monitor import monitor
stats = monitor.get_system_health()
```

## 🏗️ Architecture

### Project Structure
```
mini project/
├── Main.py                    # Main application with modern GUI
├── advanced_models.py         # Advanced CNN architectures
├── data_augmentation.py       # Specialized data augmentation
├── performance_monitor.py     # System monitoring and metrics
├── database_manager.py        # Database operations and management
├── live_recognition.py        # Real-time video recognition

├── requirements.txt           # Python dependencies
├── setup_python311.bat       # Automated setup script
├── check_compatibility.py     # System compatibility checker
├── create_sample_dataset.py   # Sample data generator
├── model/                     # Model files and training data
├── testSamples/              # Test images
└── sample_dataset/           # Training dataset
```

### Technology Stack
- **Deep Learning**: TensorFlow/Keras with custom CNN architectures
- **Computer Vision**: OpenCV for image processing and feature extraction
- **GUI**: Tkinter with ttk for modern interface
- **Database**: SQLite for data persistence

- **Monitoring**: psutil for system metrics

## 🔧 Configuration

### Model Configuration
```python
# In advanced_models.py
model = create_advanced_iris_model(
    input_shape=(64, 64, 3),
    num_classes=108
)
```

### Database Configuration
```python
# In database_manager.py
db = IrisDatabase(db_path='iris_system.db')
```

### Performance Monitoring
```python
# In performance_monitor.py
monitor = PerformanceMonitor(
    db_path='performance.db',
    max_history=1000
)
```

## 📊 Performance Metrics

### Recognition Accuracy
- **Training Accuracy**: >95% on sample dataset
- **Validation Accuracy**: >90% on test data
- **Real-time Performance**: <500ms per recognition

### System Performance
- **Memory Usage**: <2GB during training
- **CPU Usage**: <50% during inference
- **Storage**: <100MB for model files

## 🐛 Troubleshooting

### Common Issues

#### "TensorFlow not found"
```bash
# Solution: Use compatible Python version
py -3.12 -m pip install tensorflow
```

#### "Camera not detected"
```bash
# Solution: Check camera permissions and drivers
# Test with: python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

#### "Model training slow"
```bash
# Solution: Reduce dataset size or use GPU
# Check: nvidia-smi (for GPU availability)
```

### Performance Optimization
1. **Use SSD storage** for faster I/O
2. **Close unnecessary applications** during training
3. **Use GPU acceleration** if available
4. **Reduce image resolution** for faster processing

## 🤝 Contributing

### Development Setup
```bash
# Fork the repository
git clone your-fork-url
cd "mini project"

# Create development environment
py -3.12 -m venv dev_env
dev_env\Scripts\activate.bat
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings for all functions
- Include unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TensorFlow/Keras** for deep learning framework
- **OpenCV** for computer vision capabilities
- **scikit-image** for image processing utilities
- **Tkinter** for GUI framework

## 📞 Support

For support and questions:
1. Check the troubleshooting section
2. Review the installation guide
3. Run the compatibility checker
4. Check system requirements

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Advanced CNN architectures
- ✅ Modern GUI with ttk
- ✅ Performance monitoring
- ✅ Database integration
- ✅ Live video recognition


### v1.0.0 (Original)
- ✅ Basic iris recognition
- ✅ Simple GUI
- ✅ CNN model training
- ✅ Image processing

---

**🎯 Ready to get started? Run `python check_compatibility.py` to verify your system!**
