import pytest, subprocess
#     ###################### LOAD TESTING MODULE  ###########################
from importlib.machinery import SourceFileLoader
from os import getenv
test = SourceFileLoader("run_command", f"{getenv('HOME')}/common/src/my_functions_beatzaplenty/general_purpose.py").load_module()
  #############################################################################

#from my_functions_beatzaplenty.general_purpose import run_command

def test_run_command_successful_execution():
    command = ["echo", "Hello, World!"]
    assert test.run_command(command) is True

def test_run_command_failure():
    command = ["nonexistent_command"]
    assert test.run_command(command) is False

def test_run_command_exception_handling():
    command = ["command_with_syntax_error"]
    # Replace the command above with one that would cause an exception
    # in your run_command function, e.g., by having invalid syntax.
    with pytest.raises(Exception):
        test.run_command(subprocess.CalledProcessError)

# You can add more tests based on the specific scenarios you want to cover.
