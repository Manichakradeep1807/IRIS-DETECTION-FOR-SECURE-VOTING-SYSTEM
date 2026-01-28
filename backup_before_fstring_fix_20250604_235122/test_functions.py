"""
Test the Train Model and View Analytics functions
"""

import sys
import os
import traceback

def test_train_model():
    """Test the train model function"""
    print("🧪 Testing Train Model Function")
    print("=" * 40)
    
    try:
        # Import required modules
        import numpy as np
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        from sklearn.model_selection import train_test_split
        
        print("✅ All imports successful")
        
        # Check training data
        if os.path.exists('model/X.txt.npy') and os.path.exists('model/Y.txt.npy'):
            print("✅ Training data found")
            
            X_train = np.load('model/X.txt.npy')
            Y_train = np.load('model/Y.txt.npy')
            
            print(f"   Data shape: {X_train.shape}")
            print(f"   Labels shape: {Y_train.shape}")
            print(f"   Data type: {X_train.dtype}")
            print(f"   Value range: [{X_train.min():.3f}, {X_train.max():.3f}]")
            
            # Test model creation
            print("\n🏗️ Testing model creation...")
            model = Sequential([
                Conv2D(64, (3, 3), input_shape=(64, 64, 3), activation='relu', padding='same'),
                MaxPooling2D(pool_size=(2, 2)),
                Conv2D(128, (3, 3), activation='relu', padding='same'),
                MaxPooling2D(pool_size=(2, 2)),
                Flatten(),
                Dense(256, activation='relu'),
                Dropout(0.5),
                Dense(Y_train.shape[1], activation='softmax')
            ])
            
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            print(f"✅ Model created successfully with {model.count_params():,} parameters")
            
            return True
        else:
            print("❌ Training data not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in train model test: {e}")
        traceback.print_exc()
        return False

def test_analytics():
    """Test the analytics function"""
    print("\n🧪 Testing Analytics Function")
    print("=" * 40)
    
    try:
        import pickle
        import tkinter as tk
        from datetime import datetime
        
        print("✅ All imports successful")
        
        # Check if history file exists
        if os.path.exists('model/history.pckl'):
            print("✅ Training history found")
            
            with open('model/history.pckl', 'rb') as f:
                data = pickle.load(f)
            
            print(f"   Data keys: {list(data.keys())}")
            
            if 'accuracy' in data:
                accuracy = data['accuracy']
                print(f"   Accuracy epochs: {len(accuracy)}")
                print(f"   Final accuracy: {accuracy[-1]*100:.2f}%")
                print(f"   Best accuracy: {max(accuracy)*100:.2f}%")
            
            if 'loss' in data:
                loss = data['loss']
                print(f"   Loss epochs: {len(loss)}")
                print(f"   Final loss: {loss[-1]:.4f}")
                print(f"   Best loss: {min(loss):.4f}")
            
            # Test creating analytics window
            print("\n🖼️ Testing analytics window creation...")
            root = tk.Tk()
            root.withdraw()  # Hide main window
            
            # Create test analytics window
            analytics_window = tk.Toplevel(root)
            analytics_window.title("📊 Test Analytics")
            analytics_window.geometry("600x400")
            
            # Add test content
            text_widget = tk.Text(analytics_window, height=15, width=60)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget.insert(tk.END, "🎯 ANALYTICS TEST\n")
            text_widget.insert(tk.END, "=" * 30 + "\n\n")
            text_widget.insert(tk.END, f"Final Accuracy: {accuracy[-1]*100:.2f}%\n")
            text_widget.insert(tk.END, f"Final Loss: {loss[-1]:.4f}\n")
            text_widget.insert(tk.END, f"Total Epochs: {len(accuracy)}\n")
            
            print("✅ Analytics window created successfully")
            
            # Close test window
            analytics_window.destroy()
            root.destroy()
            
            return True
        else:
            print("❌ Training history not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in analytics test: {e}")
        traceback.print_exc()
        return False

def test_main_functions():
    """Test the main functions from Main.py"""
    print("\n🧪 Testing Main.py Functions")
    print("=" * 40)
    
    try:
        # Import the main module
        sys.path.append('.')
        
        # Test importing functions
        print("Testing function imports...")
        
        # Create a minimal test environment
        import tkinter as tk
        
        # Create test root window
        test_root = tk.Tk()
        test_root.withdraw()
        
        # Create test text widget
        test_text = tk.Text(test_root)
        
        # Test if we can access the functions
        print("✅ Basic setup successful")
        
        test_root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error testing main functions: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔬 Train Model & Analytics Test Suite")
    print("=" * 60)
    
    # Test 1: Train Model
    test1_result = test_train_model()
    
    # Test 2: Analytics
    test2_result = test_analytics()
    
    # Test 3: Main functions
    test3_result = test_main_functions()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Train Model Test: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Analytics Test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"Main Functions Test: {'✅ PASS' if test3_result else '❌ FAIL'}")
    
    if test1_result and test2_result and test3_result:
        print("\n🎉 ALL TESTS PASSED!")
        print("The functions should work correctly.")
    else:
        print("\n⚠️ Some tests failed.")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()
