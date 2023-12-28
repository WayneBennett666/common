import os
import configparser
import pytest
# #     ###################### LOAD TESTING MODULE  ###########################
from importlib.machinery import SourceFileLoader
from os import getenv
test = SourceFileLoader("create_config_file", f"{getenv('HOME')}/common/src/my_functions_beatzaplenty/general_purpose.py").load_module()
#   #############################################################################

# from my_functions_beatzaplenty.general_purpose import create_config_file

@pytest.fixture
def sample_config_data():
    return {
        'Section1': {'key1': 'value1', 'key2': 'value2'},
        'Section2': {'key3': 'value3', 'key4': 'value4'}
    }

@pytest.fixture
def temp_config_file(tmp_path):
    return tmp_path / "test_config.ini"

def test_create_config_file(tmp_path, sample_config_data):
    file_path = tmp_path / "test_config.ini"
    
    test.create_config_file(sample_config_data, file_path)

    # Check if the file is created
    assert file_path.exists()

    # Check if the content of the file is correct
    config = configparser.ConfigParser()
    config.read(file_path)
    
    assert config.sections() == ['Section1', 'Section2']
    assert dict(config['Section1']) == {'key1': 'value1', 'key2': 'value2'}
    assert dict(config['Section2']) == {'key3': 'value3', 'key4': 'value4'}

def test_create_config_file_exception_handling(tmp_path, sample_config_data, capsys):
    # Create a file in read-only mode to simulate an exception
    file_path = tmp_path / "test_config.ini"
    file_path.touch()
    os.chmod(file_path, 0o444)  # Make the file read-only

    test.create_config_file(sample_config_data, file_path)

    # Check if an error message is printed
    captured = capsys.readouterr()
    assert "Error:" in captured.out
