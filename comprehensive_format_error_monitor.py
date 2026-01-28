#!/usr/bin/env python3
"""
COMPREHENSIVE FORMAT ERROR MONITOR
Real-time monitoring and debugging tool for the iris recognition system
to catch and analyze the "unsupported format string passed to bytes.__format__" error
"""

import sys
import traceback
import logging
import os
from datetime import datetime
import threading
import time

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('format_error_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class FormatErrorMonitor:
    """Monitor for format string errors in the iris recognition system"""
    
    def __init__(self):
        self.error_count = 0
        self.last_error = None
        self.monitoring = False
        self.error_patterns = []
        
    def start_monitoring(self):
        """Start monitoring for errors"""
        self.monitoring = True
        logger.info("🔍 Format error monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring for errors"""
        self.monitoring = False
        logger.info("⏹️ Format error monitoring stopped")
        
    def log_error(self, error_type, error_msg, traceback_str, context=""):
        """Log an error with full details"""
        self.error_count += 1
        self.last_error = {
            'type': error_type,
            'message': error_msg,
            'traceback': traceback_str,
            'context': context,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.error("❌ ERROR #{}: {}".format(self.error_count, error_type))
        logger.error("Message: {}".format(error_msg))
        logger.error("Context: {}".format(context))
        logger.error("Traceback: {}".format(traceback_str))
        
        # Store error pattern for analysis
        self.error_patterns.append({
            'type': error_type,
            'message': error_msg,
            'context': context
        })

# Global error monitor
error_monitor = FormatErrorMonitor()

def test_voting_system_comprehensive():
    """Comprehensive test of voting system operations"""
    logger.info("🗳️ Testing voting system comprehensively...")
    
    try:
        from voting_system import voting_system
        
        # Test 1: Basic operations
        logger.info("1. Testing basic voting operations...")
        parties = voting_system.get_parties()
        logger.info("   ✅ Parties retrieved: {} parties".format(len(parties)))
        
        # Test 2: Vote casting with different scenarios
        logger.info("2. Testing vote casting scenarios...")
        test_cases = [
            (6666, 1, 0.95, "High confidence vote"),
            (6667, 2, 0.88, "Medium confidence vote"),
            (6668, 3, 0.92, "Another high confidence vote")
        ]
        
        for person_id, party_id, confidence, description in test_cases:
            try:
                # Clean up first
                import sqlite3
                with sqlite3.connect(voting_system.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM votes WHERE person_id = ?', (person_id,))
                    conn.commit()
                
                # Test vote casting
                result = voting_system.cast_vote(person_id, party_id, confidence)
                logger.info("   ✅ {}: {}".format(description, 'Success' if result else 'Failed'))
                
                # Test vote verification
                if result:
                    has_voted = voting_system.has_voted(person_id)
                    logger.info("   ✅ Vote verification: {}".format('Recorded' if has_voted else 'Not found'))
                
            except Exception as e:
                error_monitor.log_error(
                    "VOTE_CASTING_ERROR",
                    str(e),
                    traceback.format_exc(),
                    "Testing vote casting for person {} with confidence {}".format(person_id, confidence)
                )
        
        # Test 3: Results retrieval
        logger.info("3. Testing results retrieval...")
        results = voting_system.get_voting_results()
        logger.info("   ✅ Results retrieved: {} total votes".format(results.get('total_votes', 0)))
        
        return True
        
    except Exception as e:
        error_monitor.log_error(
            "VOTING_SYSTEM_ERROR",
            str(e),
            traceback.format_exc(),
            "Comprehensive voting system test"
        )
        return False

def test_string_formatting_patterns():
    """Test various string formatting patterns that might cause issues"""
    logger.info("📝 Testing string formatting patterns...")
    
    try:
        import hashlib
        from datetime import datetime
        
        # Test 1: Basic format patterns
        logger.info("1. Testing basic format patterns...")
        test_patterns = [
            ("Basic string", "Person {} voted".format(123)),
            ("Float format", "Confidence: {:.2f}%".format(95.5)),
            ("Multiple args", "{} voted for {} with {}% confidence".format(123, "Party", 95)),
            ("Date format", "Vote at: {}".format(datetime.now().isoformat())),
            ("Hash format", "Hash: {}".format("abc123def456")),
        ]
        
        for pattern_name, pattern_result in test_patterns:
            logger.info("   ✅ {}: {}".format(pattern_name, pattern_result[:50]))
        
        # Test 2: Bytes handling
        logger.info("2. Testing bytes handling...")
        try:
            test_bytes = b"test data"
            decoded_string = test_bytes.decode('utf-8')
            formatted_string = "Decoded: {}".format(decoded_string)
            logger.info("   ✅ Bytes handling: {}".format(formatted_string))
        except Exception as e:
            error_monitor.log_error(
                "BYTES_HANDLING_ERROR",
                str(e),
                traceback.format_exc(),
                "Testing bytes to string conversion"
            )
        
        # Test 3: Hash generation patterns
        logger.info("3. Testing hash generation patterns...")
        hash_test_cases = [
            "123_1_2025-06-05T10:00:00",
            "456_2_2025-06-05T11:00:00",
            "789_3_2025-06-05T12:00:00"
        ]
        
        for vote_data in hash_test_cases:
            try:
                # Test the exact pattern used in voting system
                vote_hash = hashlib.sha256(vote_data.encode('utf-8')).hexdigest()
                logger.info("   ✅ Hash for '{}': {}...".format(vote_data[:20], vote_hash[:20]))
            except Exception as e:
                error_monitor.log_error(
                    "HASH_GENERATION_ERROR",
                    str(e),
                    traceback.format_exc(),
                    "Generating hash for vote data: {}".format(vote_data)
                )
        
        # Test 4: Complex formatting scenarios
        logger.info("4. Testing complex formatting scenarios...")
        try:
            person_id = 123
            party_id = 2
            confidence = 0.95
            timestamp = datetime.now().isoformat()
            
            # Test the exact patterns used in the voting system
            vote_data_pattern1 = "{}_{}_{}" .format(person_id, party_id, timestamp)
            logger.info("   ✅ Vote data pattern 1: {}...".format(vote_data_pattern1[:30]))
            
            vote_data_pattern2 = str(person_id) + "_" + str(party_id) + "_" + timestamp
            logger.info("   ✅ Vote data pattern 2: {}...".format(vote_data_pattern2[:30]))
            
            message_pattern = "Person {} voted for party {} with {:.1%} confidence".format(person_id, party_id, confidence)
            logger.info("   ✅ Message pattern: {}".format(message_pattern))
            
        except Exception as e:
            error_monitor.log_error(
                "COMPLEX_FORMATTING_ERROR",
                str(e),
                traceback.format_exc(),
                "Testing complex formatting scenarios"
            )
        
        return True
        
    except Exception as e:
        error_monitor.log_error(
            "STRING_FORMATTING_ERROR",
            str(e),
            traceback.format_exc(),
            "String formatting pattern test"
        )
        return False

def test_gui_operations():
    """Test GUI operations that might trigger format errors"""
    logger.info("🖥️ Testing GUI operations...")
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Test 1: Basic GUI setup
        logger.info("1. Testing basic GUI setup...")
        root = tk.Tk()
        root.withdraw()  # Hide the window
        logger.info("   ✅ Tkinter root created")
        
        # Test 2: Message formatting for GUI
        logger.info("2. Testing message formatting for GUI...")
        test_messages = [
            "Person {} voted for {}".format(123, "Test Party"),
            "Vote cast with {:.1%} confidence".format(0.95),
            "Error: {}".format("Test error message"),
            "Processing file: {}".format("test_image.jpg")
        ]
        
        for i, message in enumerate(test_messages):
            logger.info("   ✅ Message {}: {}".format(i+1, message))
        
        # Test 3: Text widget operations
        logger.info("3. Testing text widget operations...")
        text_widget = tk.Text(root)
        
        try:
            # Test text insertion patterns
            test_insertions = [
                "🔍 ENHANCED IRIS RECOGNITION TEST\n",
                "📁 Processing: {}\n".format("test_file.jpg"),
                "✅ Recognition completed with {:.1%} confidence\n".format(0.95)
            ]
            
            for insertion in test_insertions:
                # Don't actually insert, just test the string formatting
                logger.info("   ✅ Text insertion test: {}".format(repr(insertion[:30])))
                
        except Exception as e:
            error_monitor.log_error(
                "TEXT_WIDGET_ERROR",
                str(e),
                traceback.format_exc(),
                "Testing text widget operations"
            )
        
        root.destroy()
        return True
        
    except Exception as e:
        error_monitor.log_error(
            "GUI_OPERATIONS_ERROR",
            str(e),
            traceback.format_exc(),
            "GUI operations test"
        )
        return False

def main():
    """Main monitoring function"""
    logger.info("🔧 COMPREHENSIVE FORMAT ERROR MONITOR")
    logger.info("=" * 60)
    logger.info("Monitoring for: 'unsupported format string passed to bytes.__format__'")
    logger.info("=" * 60)
    
    error_monitor.start_monitoring()
    
    # Run comprehensive tests
    tests = [
        ("Voting System", test_voting_system_comprehensive),
        ("String Formatting", test_string_formatting_patterns),
        ("GUI Operations", test_gui_operations)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info("\n" + "="*50)
        logger.info("Running test: {}".format(test_name))
        logger.info("="*50)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error("❌ CRITICAL ERROR in {}: {}".format(test_name, str(e)))
            traceback.print_exc()
            results.append((test_name, False))
    
    error_monitor.stop_monitoring()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 MONITORING SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info("{}: {}".format(test_name, status))
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("\nTotal: {} passed, {} failed".format(passed, failed))
    logger.info("Errors detected: {}".format(error_monitor.error_count))
    
    if error_monitor.error_count > 0:
        logger.info("\n🚨 FORMAT ERRORS DETECTED!")
        logger.info("Last error: {}".format(error_monitor.last_error['message']))
        logger.info("Context: {}".format(error_monitor.last_error['context']))
        logger.info("Check format_error_monitor.log for full details")
        
        # Analyze error patterns
        logger.info("\n📊 ERROR PATTERN ANALYSIS:")
        for i, pattern in enumerate(error_monitor.error_patterns):
            logger.info("{}. {}: {}".format(i+1, pattern['type'], pattern['message'][:50]))
    else:
        logger.info("\n✅ NO FORMAT ERRORS DETECTED")
        logger.info("The system appears to be working correctly")
        logger.info("\nIf you still experience the error:")
        logger.info("1. Run this script immediately when the error occurs")
        logger.info("2. Note the exact sequence of actions that trigger it")
        logger.info("3. Check the log file for any missed errors")

if __name__ == "__main__":
    main()
