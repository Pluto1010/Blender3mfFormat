#!/usr/bin/env python3
"""
Test runner for the Blender 3MF Format add-on tests.
"""

import sys
import os
import unittest
import unittest.mock

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def setup_comprehensive_blender_mocks():
    """Set up comprehensive mocks for all Blender API modules."""
    # Create a comprehensive mock for bpy
    bpy_mock = unittest.mock.MagicMock()
    bpy_mock.__path__ = []  # Make it a package
    
    # Set up all the bpy submodules
    bpy_mock.types = unittest.mock.MagicMock()
    bpy_mock.props = unittest.mock.MagicMock()
    bpy_mock.utils = unittest.mock.MagicMock()
    bpy_mock.data = unittest.mock.MagicMock()
    bpy_mock.context = unittest.mock.MagicMock()
    bpy_mock.ops = unittest.mock.MagicMock()
    
    # Mock bpy_extras
    bpy_extras_mock = unittest.mock.MagicMock()
    bpy_extras_mock.__path__ = []
    bpy_extras_mock.io_utils = unittest.mock.MagicMock()
    bpy_extras_mock.node_shader_utils = unittest.mock.MagicMock()
    
    # Mock other Blender-specific modules
    mathutils_mock = unittest.mock.MagicMock()
    idprop_mock = unittest.mock.MagicMock()
    idprop_mock.__path__ = []
    idprop_mock.types = unittest.mock.MagicMock()
    
    # Install all mocks in sys.modules
    modules_to_mock = [
        ('bpy', bpy_mock),
        ('bpy.types', bpy_mock.types),
        ('bpy.props', bpy_mock.props),
        ('bpy.utils', bpy_mock.utils),
        ('bpy.data', bpy_mock.data),
        ('bpy.context', bpy_mock.context),
        ('bpy.ops', bpy_mock.ops),
        ('bpy_extras', bpy_extras_mock),
        ('bpy_extras.io_utils', bpy_extras_mock.io_utils),
        ('bpy_extras.node_shader_utils', bpy_extras_mock.node_shader_utils),
        ('mathutils', mathutils_mock),
        ('idprop', idprop_mock),
        ('idprop.types', idprop_mock.types),
    ]
    
    for module_name, mock_obj in modules_to_mock:
        sys.modules[module_name] = mock_obj

if __name__ == '__main__':
    # Set up comprehensive Blender mocks first
    setup_comprehensive_blender_mocks()
    
    test_dir = os.path.join(project_root, 'test')
    sys.path.insert(0, test_dir)
    
    try:
        # Import the mock modules
        from mock.bpy import MockOperator, MockExportHelper, MockImportHelper
        
        # Set up the mocks
        import bpy.types
        import bpy_extras.io_utils
        bpy.types.Operator = MockOperator
        bpy_extras.io_utils.ImportHelper = MockImportHelper
        bpy_extras.io_utils.ExportHelper = MockExportHelper
        
        # Now try to use unittest discovery but with proper setup
        print("Discovering and running tests...")
        
        # Use unittest discovery but start from a specific pattern
        loader = unittest.TestLoader()
        
        # Just run the annotations test file by importing it correctly
        # We'll modify the content on the fly
        annotations_file = os.path.join(test_dir, 'annotations.py')
        with open(annotations_file, 'r') as f:
            content = f.read()
        
        # Replace the problematic relative import
        content = content.replace('from .mock.bpy import', 'from mock.bpy import')
        
        # Write to a temporary file or execute in a custom namespace
        temp_namespace = {}
        exec(content, temp_namespace)
        
        # Extract the test class
        test_class = temp_namespace.get('TestAnnotations')
        if test_class:
            suite = loader.loadTestsFromTestCase(test_class)
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            print(f"\nTest Results:")
            print(f"Tests run: {result.testsRun}")
            print(f"Failures: {len(result.failures)}")
            print(f"Errors: {len(result.errors)}")
            
            if result.failures:
                print("\nFailures:")
                for test, traceback_str in result.failures:
                    print(f"{test}: {traceback_str}")
            
            if result.errors:
                print("\nErrors:")  
                for test, traceback_str in result.errors:
                    print(f"{test}: {traceback_str}")
            
            # Exit with appropriate code
            sys.exit(not result.wasSuccessful())
        else:
            print("Could not find TestAnnotations class")
            sys.exit(1)
        
    except Exception as e:
        print(f"Error setting up or running test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
