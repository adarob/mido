from pytest import raises
from .midifiles_meta import MetaMessage, FrozenMetaMessage

def test_new_frozen_message():
    msg = FrozenMetaMessage('track_name', name='Track 1')
    assert msg.frozen

    assert repr(msg).startswith('<frozen meta message ')

def test_frozen_message_from_message():
    msg = MetaMessage('track_name', name='Track 1')
    fmsg = FrozenMetaMessage(msg)
    assert isinstance(fmsg, FrozenMetaMessage)
    
def test_copy_is_frozen_message():
    msg1 = FrozenMetaMessage('track_name')
    msg2 = msg1.copy()
    assert isinstance(msg2, FrozenMetaMessage)

def test_immutability():
    # Passing attributes should work.
    msg = FrozenMetaMessage('track_name')
    
    # Setting attributes should not.
    with raises(ValueError): msg.name = 'Test'

def test_hashability():
    msg1 = FrozenMetaMessage('track_name', name='Track 1')
    msg2 = FrozenMetaMessage('track_name', name='Track 2')
    
    assert hash(msg1)
    assert hash(msg1) != hash(msg2)

    # Message can be placed in a set.
    {msg1}

def test_time_ignored():
    msg1 = FrozenMetaMessage('track_name', time=1)
    msg2 = FrozenMetaMessage('track_name', time=2)

    # Time should be ignored in hash.
    assert hash(msg1) == hash(msg2)
