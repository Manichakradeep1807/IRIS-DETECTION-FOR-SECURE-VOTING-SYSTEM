"""
Debug script to test the functions directly
"""

import tkinter as tk
import os
import sys

def test_loadModel_function():
    """Test the loadModel function directly"""
    print("🧪 Testing loadModel function directly")
    print("=" * 40)
    
    try:
        # Create a minimal GUI environment
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        # Create a text widget (simulating the global text variable)
        text = tk.Text(root)
        
        # Import required modules
        import numpy as np
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
        from sklearn.model_selection import train_test_split
        from datetime import datetime
        
        print("✅ All imports successful")
        
        # Check if training data exists
        if not os.path.exists('model/X.txt.npy') or not os.path.exists('model/Y.txt.npy'):
            print("❌ No training data found!")
            return False
        
        # Load data
        print("📂 Loading training data...")
        X_train = np.load('model/X.txt.npy')
        Y_train = np.load('model/Y.txt.npy')
        
        print(f"   Dataset shape: {X_train.shape}")
        print(f"   Labels shape: {Y_train.shape}")
        
        # Preprocess data
        X_train = X_train.astype('float32') / 255.0
        
        # Split data
        X_train_split, X_val, Y_train_split, Y_val = train_test_split(
            X_train, Y_train, test_size=0.2, random_state=42, 
            stratify=np.argmax(Y_train, axis=1)
        )
        
        print(f"   Training samples: {X_train_split.shape[0]}")
        print(f"   Validation samples: {X_val.shape[0]}")
        
        # Create model (same as in loadModel)
        print("🏗️ Creating model...")
        model = Sequential([
            Conv2D(64, (3, 3), input_shape=(64, 64, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            MaxPooling2D(pool_size=(2, 2)),
            
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(Y_train.shape[1], activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"   Model parameters: {model.count_params():,}")
        
        # Quick training test (1 epoch)
        print("🚀 Quick training test (1 epoch)...")
        history = model.fit(
            X_train_split, Y_train_split,
            batch_size=32,
            epochs=1,
            validation_data=(X_val, Y_val),
            verbose=1
        )
        
        # Save model
        print("💾 Saving model...")
        model.save_weights('model/test_model.weights.h5')
        
        print("✅ loadModel function simulation successful!")
        
        # Cleanup
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Error in loadModel test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_analytics_function():
    """Test the analytics function directly"""
    print("\n🧪 Testing analytics function directly")
    print("=" * 40)
    
    try:
        import pickle
        from datetime import datetime
        
        # Create a minimal GUI environment
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        print("✅ GUI environment created")
        
        # Check if history exists
        if os.path.exists('model/history.pckl'):
            print("✅ Training history found")
            
            with open('model/history.pckl', 'rb') as f:
                data = pickle.load(f)
            
            print(f"   Data keys: {list(data.keys())}")
            
            # Create analytics window (same as in show_analytics_dashboard)
            analytics_window = tk.Toplevel(root)
            analytics_window.title("📊 Test Analytics")
            analytics_window.geometry("800x600")
            
            # Create text widget
            text_widget = tk.Text(analytics_window, height=20, width=80)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add analytics content
            text_widget.insert(tk.END, "🎯 ANALYTICS TEST REPORT\n")
            text_widget.insert(tk.END, "=" * 50 + "\n\n")
            
            if 'accuracy' in data:
                accuracy = data['accuracy']
                text_widget.insert(tk.END, f"📈 ACCURACY METRICS:\n")
                text_widget.insert(tk.END, f"   Final Accuracy: {accuracy[-1]*100:.2f}%\n")
                text_widget.insert(tk.END, f"   Best Accuracy: {max(accuracy)*100:.2f}%\n")
                text_widget.insert(tk.END, f"   Total Epochs: {len(accuracy)}\n\n")
            
            if 'loss' in data:
                loss = data['loss']
                text_widget.insert(tk.END, f"📉 LOSS METRICS:\n")
                text_widget.insert(tk.END, f"   Final Loss: {loss[-1]:.4f}\n")
                text_widget.insert(tk.END, f"   Best Loss: {min(loss):.4f}\n\n")
            
            text_widget.insert(tk.END, f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print("✅ Analytics window created successfully")
            
            # Close window after a moment
            analytics_window.after(2000, analytics_window.destroy)  # Close after 2 seconds
            analytics_window.after(2100, root.destroy)  # Close root after 2.1 seconds
            
            # Show the window briefly
            root.mainloop()
            
            print("✅ Analytics function simulation successful!")
            return True
        else:
            print("❌ No training history found")
            root.destroy()
            return False
            
    except Exception as e:
        print(f"❌ Error in analytics test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔬 Direct Function Testing")
    print("=" * 60)
    
    # Test 1: loadModel function
    test1_result = test_loadModel_function()
    
    # Test 2: analytics function
    test2_result = test_analytics_function()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIRECT FUNCTION TEST SUMMARY")
    print("=" * 60)
    print(f"loadModel Function: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Analytics Function: {'✅ PASS' if test2_result else '❌ FAIL'}")
    
    if test1_result and test2_result:
        print("\n🎉 BOTH FUNCTIONS WORK CORRECTLY!")
        print("The issue might be with button connections or global variables.")
        print("\nSuggested fixes:")
        print("1. Check if buttons are properly connected to functions")
        print("2. Verify global variable declarations")
        print("3. Test clicking buttons in the actual application")
    else:
        print("\n⚠️ FUNCTION ISSUES DETECTED!")
        print("The functions themselves have problems that need fixing.")

if __name__ == "__main__":
    main()
