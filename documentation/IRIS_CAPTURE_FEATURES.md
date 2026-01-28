# 👁️ Enhanced Live Recognition with Iris Image Capture

## 🆕 New Features Added

The live recognition system has been enhanced with comprehensive iris image capture and display capabilities. Now when the system recognizes a person, it automatically captures and displays the iris images for better visibility and analysis.

## 📸 Automatic Image Capture

### What happens during live recognition:
1. **Real-time Processing**: Camera captures frames continuously
2. **Eye Detection**: System detects eyes in each frame
3. **Iris Extraction**: Extracts iris features from detected eyes
4. **Recognition**: Compares features against trained model
5. **🆕 Automatic Capture**: When recognition occurs (confidence > threshold), the system automatically:
   - Captures the iris image
   - Creates a composite image showing both eye region and extracted iris
   - Saves it with person ID and timestamp
   - Displays it in real-time

## 🖼️ Image Display Features

### 1. Real-time Iris Window
- **Window Name**: "Captured Iris"
- **Content**: Shows the latest captured iris image
- **Updates**: Automatically updates when new iris is captured
- **Size**: Automatically resized for better visibility (minimum 400px width)

### 2. Grid View of All Captures
- **Trigger**: Press 'c' during live recognition
- **Window Name**: "All Captured Images"
- **Layout**: Grid layout showing up to 16 images (4x4)
- **Content**: All captured iris images from current session

## 🎮 New Keyboard Controls

| Key | Function | Description |
|-----|----------|-------------|
| `i` | Toggle Iris Window | Turn the iris capture window ON/OFF |
| `c` | View All Captures | Show grid of all captured iris images |
| `q` | Quit | Exit live recognition (existing) |
| `s` | Screenshot | Save current frame (existing) |
| `r` | Reset Stats | Reset recognition statistics (existing) |

## 💾 File Storage System

### Folder Structure
```
mini project/
├── captured_iris/                    # 🆕 New folder for iris images
│   ├── iris_person1_20241202_143052_123.jpg
│   ├── iris_person2_20241202_143055_456.jpg
│   └── ...
├── screenshot_20241202_143100.jpg    # Screenshots (existing)
├── iris_system.db                    # Database (existing)
└── iris_system.log                   # Logs (existing)
```

### File Naming Convention
- **Format**: `iris_person[ID]_[YYYYMMDD_HHMMSS_mmm].jpg`
- **Example**: `iris_person1_20241202_143052_123.jpg`
- **Components**:
  - `person1`: Recognized person ID
  - `20241202`: Date (Dec 2, 2024)
  - `143052`: Time (14:30:52)
  - `123`: Milliseconds

### Image Content
Each saved image is a **composite** showing:
- **Left side**: Original eye region detected by the system
- **Right side**: Extracted iris features used for recognition
- **Top**: Person ID and confidence score
- **Bottom**: Labels ("Eye Region" and "Extracted Iris")

## 🔧 Technical Implementation

### New Methods Added
1. `_capture_iris_image()` - Captures and saves iris images
2. `_toggle_iris_window()` - Toggles the iris display window
3. `_update_iris_display()` - Updates the real-time iris display
4. `_show_captured_images()` - Shows all captured images in grid

### Memory Management
- **Limit**: Keeps only the last 50 captured images in memory
- **Cleanup**: Automatically removes oldest images when limit exceeded
- **Files**: All images are saved to disk regardless of memory limit

### Enhanced Error Handling
- Comprehensive try-catch blocks for all new functionality
- Detailed logging of capture events and errors
- Graceful degradation if display features fail

## 🚀 How to Use

### 1. Start Live Recognition
```python
# From main application
python Main.py
# Click "📹 LIVE RECOGNITION" button

# Or directly
python live_recognition.py
```

### 2. Position Yourself
- **Distance**: 12-18 inches from camera
- **Lighting**: Ensure good lighting (avoid shadows)
- **Angle**: Look directly at the camera
- **Stability**: Keep your head steady

### 3. Watch for Recognition
- **Green box**: Appears around recognized eye
- **Text display**: Shows "Person X: 0.XX" with confidence
- **Automatic capture**: Iris image captured automatically
- **Console message**: "📸 Iris captured: Person X (Confidence: 0.XX)"

### 4. Use New Controls
- **Press 'i'**: Toggle the iris capture window
- **Press 'c'**: View all captured images
- **Check folder**: Look in `captured_iris/` for saved files

## 📊 What Gets Stored

### During Live Recognition Session:

1. **Database (iris_system.db)**:
   - Recognition results with person ID, confidence, timestamp
   - Access logs for audit trail

2. **🆕 Captured Iris Images (captured_iris/)**:
   - Composite images showing eye region + extracted iris
   - Person ID and confidence score labels
   - Timestamp-based file names

3. **Screenshots (optional)**:
   - Full frame screenshots when 's' is pressed
   - Includes all overlays and detection boxes

4. **Performance Data (performance.db)**:
   - Recognition performance metrics
   - Response times and accuracy statistics

5. **Logs (iris_system.log)**:
   - Error messages and system events
   - Capture events and debugging information

## 💡 Benefits

### For Users:
- **Visual Feedback**: See exactly what the system captured
- **Quality Assessment**: Verify iris extraction quality
- **Audit Trail**: Complete record of recognition events
- **Real-time Monitoring**: Immediate feedback on captures

### For Developers:
- **Debugging**: Visual inspection of iris extraction
- **Quality Control**: Assess recognition accuracy
- **Data Collection**: Gather iris samples for training
- **Performance Analysis**: Monitor system behavior

## 🔍 Troubleshooting

### No Images Captured?
- Ensure good lighting conditions
- Position eye closer to camera (12-18 inches)
- Check if model is properly trained
- Verify confidence threshold (default: 0.7)

### Iris Window Not Showing?
- Press 'i' to toggle window on
- Check console for error messages
- Ensure OpenCV display support is available

### Poor Image Quality?
- Improve lighting conditions
- Reduce camera shake
- Clean camera lens
- Adjust distance from camera

## 🎯 Summary

The enhanced live recognition system now provides:
- ✅ **Automatic iris image capture** when recognition occurs
- ✅ **Real-time display** of captured iris images
- ✅ **Organized storage** with timestamp and person ID
- ✅ **Grid view** of all captured images
- ✅ **Toggle controls** for display windows
- ✅ **Composite images** showing both eye region and extracted iris
- ✅ **Enhanced error handling** and logging
- ✅ **Memory management** with automatic cleanup

This makes the iris recognition system much more transparent and user-friendly, allowing you to see exactly what images are being captured and how the recognition process works!
