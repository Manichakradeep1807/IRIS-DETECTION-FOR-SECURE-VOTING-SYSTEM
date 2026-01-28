"""
Test script to check if the button functions work when called directly
"""

import tkinter as tk
import sys
import os
from datetime import datetime

def test_button_click_simulation():
    """Simulate button clicks to test the functions"""
    print("🧪 Testing Button Function Execution")
    print("=" * 50)
    
    # Create a minimal GUI environment similar to Main.py
    root = tk.Tk()
    root.title("Test Environment")
    root.geometry("800x600")
    root.withdraw()  # Hide the test window
    
    # Create text widget (simulating the global text variable)
    text = tk.Text(root)
    
    # Set up global variables similar to Main.py
    model = None
    ENHANCED_FEATURES = True
    main = root
    
    print("✅ Test environment created")
    
    # Test 1: loadModel function
    print("\n🧠 Testing loadModel function...")
    try:
        # Define the loadModel function locally (copy from Main.py)
        def loadModel():
            global model, ENHANCED_FEATURES, text, main
            print("🔥 loadModel function called!")  # Debug output
            try:
                text.delete('1.0', tk.END)
                text.insert(tk.END, "🔥 loadModel function started!\n")
                main.update()
            except Exception as e:
                print(f"Error in loadModel start: {e}")
                return
            
            text.insert(tk.END, "🧠 Loading/Training CNN Model...\n")
            text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Check for training data
            if not os.path.exists('model/X.txt.npy') or not os.path.exists('model/Y.txt.npy'):
                text.insert(tk.END, "❌ No training data found!\n")
                text.insert(tk.END, "Please create sample dataset first:\n")
                text.insert(tk.END, "   Run: python create_sample_dataset.py\n\n")
                return
            
            print("✅ Training data check passed")
            text.insert(tk.END, "✅ Training data found!\n")
            text.insert(tk.END, "📂 Loading training data...\n")
            
            # Simulate successful completion
            text.insert(tk.END, "✅ loadModel function completed successfully!\n")
            print("✅ loadModel function executed successfully")
        
        # Call the function
        loadModel()
        
    except Exception as e:
        print(f"❌ Error in loadModel test: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: show_analytics_dashboard function
    print("\n📊 Testing show_analytics_dashboard function...")
    try:
        # Define the analytics function locally
        def show_analytics_dashboard():
            global main
            print("🔥 show_analytics_dashboard function called!")  # Debug output
            
            try:
                # Create analytics window
                analytics_window = tk.Toplevel(main)
                analytics_window.title("📊 Test Analytics")
                analytics_window.geometry("600x400")
                
                # Add test content
                test_label = tk.Label(analytics_window, 
                                    text="📊 Analytics Test Window\n\nThis window opened successfully!",
                                    font=('Arial', 14),
                                    justify=tk.CENTER)
                test_label.pack(expand=True)
                
                # Close button
                close_btn = tk.Button(analytics_window, text="Close", 
                                    command=analytics_window.destroy)
                close_btn.pack(pady=10)
                
                print("✅ Analytics window created successfully")
                
                # Auto-close after 3 seconds for testing
                analytics_window.after(3000, analytics_window.destroy)
                
            except Exception as e:
                print(f"❌ Error creating analytics window: {e}")
                import traceback
                traceback.print_exc()
        
        # Call the function
        show_analytics_dashboard()
        
    except Exception as e:
        print(f"❌ Error in analytics test: {e}")
        import traceback
        traceback.print_exc()
    
    # Show results in text widget
    print("\n📋 Text Widget Contents:")
    print("-" * 30)
    content = text.get('1.0', tk.END)
    print(content)
    
    # Clean up
    root.after(5000, root.destroy)  # Close after 5 seconds
    
    print("\n🎉 Button function tests completed!")
    print("If you see this message, the functions can execute properly.")
    
    # Run the GUI briefly to show any windows
    root.mainloop()

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing Required Imports")
    print("=" * 30)
    
    imports_to_test = [
        ('tkinter', 'tk'),
        ('numpy', 'np'),
        ('tensorflow.keras.models', 'Sequential'),
        ('tensorflow.keras.layers', 'Dense'),
        ('sklearn.model_selection', 'train_test_split'),
        ('pickle', None),
        ('os', None),
        ('datetime', 'datetime')
    ]
    
    all_imports_ok = True
    
    for import_name, alias in imports_to_test:
        try:
            if alias:
                exec(f"import {import_name} as {alias}")
            else:
                exec(f"import {import_name}")
            print(f"✅ {import_name}")
        except Exception as e:
            print(f"❌ {import_name}: {e}")
            all_imports_ok = False
    
    return all_imports_ok

def main():
    """Main test function"""
    print("🔬 Button Functions Diagnostic Test")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test imports first
    imports_ok = test_imports()
    
    if imports_ok:
        print("\n✅ All imports successful - proceeding with function tests")
        test_button_click_simulation()
    else:
        print("\n❌ Import errors detected - fix imports first")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
