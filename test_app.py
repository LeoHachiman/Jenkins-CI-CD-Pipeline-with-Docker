from app import get_message

def test_message_contains_ok():
    result = get_message()
    assert "OK" in result, "Health check message is broken!"

def test_message_contains_name():
    result = get_message()
    assert "Leo Stephen" in result, "Name missing from message!"

def test_message_is_string():
    result = get_message()
    assert isinstance(result, str), "Message should be a string"
