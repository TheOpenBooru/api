from modules import settings
import pytest

def test_Settings_Preserve_Correct_Value():
    assert settings.get('testing.value.str') == "sample text"
    assert settings.get('testing.value.int') == 64
    assert settings.get('testing.value.float') == 6.4
    assert settings.get('testing.value.bool') == False
    assert settings.get('testing.value.array') == [1,2,3]

def test_Getting_Settings_Preserve_Types():
    assert isinstance(settings.get('testing.type.str'),str)
    assert isinstance(settings.get('testing.type.int'),int)
    assert isinstance(settings.get('testing.type.float'),float)
    assert isinstance(settings.get('testing.type.bool'),bool)
    assert isinstance(settings.get('testing.type.array'),list)

def test_Should_Allow_Non_Terminating_Settings():
    assert isinstance(settings.get('testing.value'),dict)

def test_Raise_Error_On_Invalid_Setting():
    invalid_settings = ['invalid','testing.invalid','testing.value.invalid']
    for setting in invalid_settings:
        with pytest.raises(KeyError):
            settings.get(setting)
