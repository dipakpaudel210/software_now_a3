"""
Smoke Test Suite for HIT137 Assignment 3

This script performs basic integration tests to verify:
1. All modules can be imported
2. Core classes can be instantiated
3. Mock mode functions correctly
4. Basic workflows complete successfully

Run this before submitting to ensure everything works!
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def print_test(test_name, passed, message=""):
    """Helper to print test results in a nice format."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"       {message}")


def test_imports():
    """Test 1: Can we import all our modules?"""
    print("\n" + "="*50)
    print("TEST 1: Module Imports")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test utils imports
    total_tests += 1
    try:
        from utils.decorators import api_call_logger, simple_cache, retry
        print_test("Import decorators", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import decorators", False, str(e))
    
    # Test models imports
    total_tests += 1
    try:
        from models.base_model import BaseModel
        print_test("Import BaseModel", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import BaseModel", False, str(e))
    
    total_tests += 1
    try:
        from models.text_model import TextModel
        print_test("Import TextModel", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import TextModel", False, str(e))
    
    total_tests += 1
    try:
        from models.image_model import ImageModel
        print_test("Import ImageModel", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import ImageModel", False, str(e))
    
    # Test config
    total_tests += 1
    try:
        import config
        print_test("Import config", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import config", False, str(e))
    
    # Test GUI
    total_tests += 1
    try:
        from gui.app import AIModelGUI
        print_test("Import AIModelGUI", True)
        tests_passed += 1
    except Exception as e:
        print_test("Import AIModelGUI", False, str(e))
    
    return tests_passed, total_tests


def test_decorators():
    """Test 2: Do our decorators work?"""
    print("\n" + "="*50)
    print("TEST 2: Decorator Functionality")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    try:
        from utils.decorators import api_call_logger, simple_cache, retry
        
        # Test simple_cache decorator
        total_tests += 1
        @simple_cache(max_size=10)
        def add(a, b):
            return a + b
        
        result1 = add(2, 3)
        result2 = add(2, 3)  # Should use cache
        if result1 == result2 == 5:
            print_test("simple_cache decorator", True, "Cache working correctly")
            tests_passed += 1
        else:
            print_test("simple_cache decorator", False, "Unexpected results")
        
        # Test retry decorator
        total_tests += 1
        attempt_count = 0
        
        @retry(max_attempts=3, delay=0.1)
        def flaky_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("Simulated failure")
            return "Success"
        
        try:
            result = flaky_function()
            if result == "Success" and attempt_count == 2:
                print_test("retry decorator", True, f"Succeeded after {attempt_count} attempts")
                tests_passed += 1
            else:
                print_test("retry decorator", False, "Unexpected behavior")
        except:
            print_test("retry decorator", False, "Failed to retry correctly")
        
        # Test api_call_logger
        total_tests += 1
        @api_call_logger
        def sample_api_call(x):
            return x * 2
        
        result = sample_api_call(5)
        if result == 10:
            print_test("api_call_logger decorator", True, "Logging and execution work")
            tests_passed += 1
        else:
            print_test("api_call_logger decorator", False)
            
    except Exception as e:
        print_test("Decorator tests", False, str(e))
    
    return tests_passed, total_tests


def test_model_structure():
    """Test 3: Can we instantiate model classes?"""
    print("\n" + "="*50)
    print("TEST 3: Model Class Structure")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test TextModel instantiation
    total_tests += 1
    try:
        from models.text_model import TextModel
        from models.hf_client import HFClient
        
        client = HFClient(api_key="test_key", mock_mode=True)
        model = TextModel(client, "test-model")
        print_test("TextModel instantiation", True)
        tests_passed += 1
    except Exception as e:
        print_test("TextModel instantiation", False, str(e))
    
    # Test ImageModel instantiation
    total_tests += 1
    try:
        from models.image_model import ImageModel
        from models.hf_client import HFClient
        
        client = HFClient(api_key="test_key", mock_mode=True)
        model = ImageModel(client, "test-model")
        print_test("ImageModel instantiation", True)
        tests_passed += 1
    except Exception as e:
        print_test("ImageModel instantiation", False, str(e))
    
    return tests_passed, total_tests


def test_mock_workflow():
    """Test 4: Does mock mode work for basic workflows?"""
    print("\n" + "="*50)
    print("TEST 4: Mock Workflow")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test mock HFClient
    total_tests += 1
    try:
        from models.hf_client import HFClient
        
        client = HFClient(api_key="test", mock_mode=True)
        response = client.query("test-model", {"inputs": "Hello"})
        
        if response and "status" in response:
            print_test("Mock HFClient query", True, "Returns structured response")
            tests_passed += 1
        else:
            print_test("Mock HFClient query", False, "Unexpected response format")
    except Exception as e:
        print_test("Mock HFClient query", False, str(e))
    
    # Test TextModel in mock mode
    total_tests += 1
    try:
        from models.text_model import TextModel
        from models.hf_client import HFClient
        
        client = HFClient(api_key="test", mock_mode=True)
        model = TextModel(client, "test-model")
        result = model.process_input("Test input")
        
        if result and result.get("status") == "success":
            print_test("TextModel mock processing", True)
            tests_passed += 1
        else:
            print_test("TextModel mock processing", False)
    except Exception as e:
        print_test("TextModel mock processing", False, str(e))
    
    return tests_passed, total_tests


def test_package_structure():
    """Test 5: Is the package structure correct?"""
    print("\n" + "="*50)
    print("TEST 5: Package Structure")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    required_dirs = ['models', 'gui', 'utils', 'docs', 'smoke']
    required_files = ['main.py', 'config.py', 'requirements.txt', 'README.MD']
    
    # Check directories
    for dir_name in required_dirs:
        total_tests += 1
        dir_path = os.path.join(os.path.dirname(__file__), '..', dir_name)
        if os.path.isdir(dir_path):
            print_test(f"Directory exists: {dir_name}/", True)
            tests_passed += 1
        else:
            print_test(f"Directory exists: {dir_name}/", False)
    
    # Check files
    for file_name in required_files:
        total_tests += 1
        file_path = os.path.join(os.path.dirname(__file__), '..', file_name)
        if os.path.isfile(file_path):
            print_test(f"File exists: {file_name}", True)
            tests_passed += 1
        else:
            print_test(f"File exists: {file_name}", False)
    
    return tests_passed, total_tests


def test_init_files():
    """Test 6: Do __init__.py files exist and work?"""
    print("\n" + "="*50)
    print("TEST 6: Package Init Files")
    print("="*50)
    
    tests_passed = 0
    total_tests = 0
    
    packages = ['models', 'gui', 'utils']
    
    for package in packages:
        total_tests += 1
        init_path = os.path.join(os.path.dirname(__file__), '..', package, '__init__.py')
        if os.path.isfile(init_path):
            print_test(f"__init__.py exists in {package}/", True)
            tests_passed += 1
        else:
            print_test(f"__init__.py exists in {package}/", False)
    
    # Test that packages can be imported
    total_tests += 1
    try:
        import models
        import gui
        import utils
        print_test("All packages importable", True)
        tests_passed += 1
    except Exception as e:
        print_test("All packages importable", False, str(e))
    
    return tests_passed, total_tests


def main():
    """Run all smoke tests."""
    print("\n" + "🔥"*25)
    print("🔥  HIT137 Assignment 3 - SMOKE TESTS  🔥")
    print("🔥"*25)
    
    total_passed = 0
    total_tests = 0
    
    # Run all test suites
    test_suites = [
        test_imports,
        test_decorators,
        test_model_structure,
        test_mock_workflow,
        test_package_structure,
        test_init_files
    ]
    
    for test_suite in test_suites:
        try:
            passed, tests = test_suite()
            total_passed += passed
            total_tests += tests
        except Exception as e:
            print(f"\n❌ Test suite {test_suite.__name__} crashed: {e}")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Ready for submission! 🎉")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed. Please review and fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())