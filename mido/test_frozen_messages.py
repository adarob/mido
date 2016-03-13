from pytest import raises
from .messages import Message, FrozenMessage

def test_new_frozen_message():
    msg = FrozenMessage('clock')
    assert msg.frozen

    assert repr(msg) == '<frozen message clock time=0>'

def test_frozen_message_from_message():
    msg = Message('note_on', channel=1, note=2, velocity=3, time=3)
    fmsg = FrozenMessage(msg)
    assert isinstance(fmsg, FrozenMessage)
    assert str(msg) == str(fmsg)

def test_frozen_message_copy_is_frozen_message():
    msg1 = FrozenMessage('clock')
    msg2 = msg1.copy()
    assert isinstance(msg2, FrozenMessage)

def test_frozen_message_immutability():
    # Passing attributes should work.
    msg = FrozenMessage('note_on', note=1)
    
    # Setting attributes should not.
    with raises(ValueError): msg.note = 2

def test_hashability():
    msg1 = FrozenMessage('songpos', pos=1)
    msg2 = FrozenMessage('songpos', pos=2)
    
    assert hash(msg1)
    assert hash(msg1) != hash(msg2)

    # Message can be placed in a set.
    {msg1}

def test_time_ignored():
    msg1 = FrozenMessage('clock', time=1)
    msg2 = FrozenMessage('clock', time=2)

    # Time should be ignored in hash.
    assert hash(msg1) == hash(msg2)
