Messages
========

A Mido message is a Python object with methods and attributes. The
attributes will vary depending on message type.

To create a new message::

    >>> mido.Message('note_on')
    <message note_on channel=0 note=0 velocity=64 time=0>

You can pass attributes as keyword arguments::

    >>> mido.Message('note_on', note=100, velocity=3, time=6.2)
    <message note_on channel=0 note=100 velocity=3 time=6.2>

All attributes will default to 0. The exceptions are ``velocity``,
which defaults to 64 (middle velocity) and ``data`` which defaults to
``()``.

You can set and get attributes as you would expect::

    >>> msg = mido.Message('note_on')
    >>> msg.note
    0
    >>> msg.note = 100
    >>> msg.note
    100

The ``type`` attribute can be used to determine message type::

    >>> msg.type
    'note_on'

To make a copy of a message, optionally overriding one or more
attributes::

    >>> msg.copy(note=99, time=100.0)
    <message note_on channel=0 note=99 velocity=64 time=100.0>

Mido supports all message types defined by the MIDI standard. For a
full list of messages and their attributes, see :doc:`message_types`.


Converting To Bytes
-------------------

You can convert a message to MIDI bytes with one of these methods:

    >>> msg = mido.Message('note_on')
    >>> msg
    <message note_on channel=0 note=0 velocity=64 time=0>
    >>> msg.bytes()
    [144, 0, 64]
    >>> msg.bin()
    bytearray(b'\x90\x00@')
    >>> msg.hex()
    '90 00 40'

You can turn bytes back into messages with the :doc:`parser <parsing>`.


The Time Attribute
------------------

Each message has a ``time`` attribute, which can be set to any value
of type ``int`` or ``float`` (and in Python 2 also ``long``). What you
do with this value is entirely up to you.

Some parts of Mido use the attribute for special purposes. In MIDI
file tracks, it is used as delta time (in ticks).

.. note::

    Proir to 1.1.15 the ``time`` attribute was not considered part of
    the message and was not included in comparison. This led to
    confusing and unexpected behaviour like this:

    .. code-block:: python

        >>> msg1 = Message('note_on', time=0)
        >>> msg2 = Message('note_on', time=1)
        >>> msg1 == msg2
        True
        >>> str(msg1) == str(msg2)
        False

    These now all give the same result. To ignore the time attribute
    you can either of these:

    .. code-block:: python

        >>> msg1.bytes() == msg2.bytes()
        True
        >>> msg1.copy(time=0) == msg2.copy(time=0)
        True

    This means tracks also compare correctly now:

    .. code-block:: python

        >>> track1 == track2
        True

    The change will break code that relied on ignoring the ``time``
    attribute. Workarounds to include it will still work::

    .. code-block:: python

        >>> # New behaviour. Now returns False if time attributes differ:
        >>> msg1 == msg2

        >>> # Still works in all cases:
        >>> (msg1, msg1.time) == (msg2, msg2.time)


System Exclusive Messages
-------------------------

System Exclusive (SysEx) messages are used to send device specific
data. The ``data`` attribute is a tuple of data bytes which serves as
the payload of the message::

    >>> msg = Message('sysex', data=[1, 2, 3])
    >>> msg
    <message sysex data=(1, 2, 3) time=0>
    >>> msg.hex()
    'F0 01 02 03 F7'

You can also extend the existing data::

   >>> msg = Message('sysex', data=[1, 2, 3])
   >>> msg.data += [4, 5]
   >>> msg.data += [6, 7, 8]
   >>> msg
   <message sysex data=(1, 2, 3, 4, 5, 6, 7, 8) time=0>

Any sequence of integers is allowed, and type and range checking is
applied to each data byte. These are all valid::

    (65, 66, 67)
    [65, 66, 67]
    (i + 65 for i in range(3))
    (ord(c) for c in 'ABC')
    bytearray(b'ABC')
    b'ABC'  # Python 3 only.

For example::

    >>> msg = Message('sysex', data=bytearray(b'ABC'))
    >>> msg.data += bytearray(b'DEF')
    >>> msg
    <message sysex data=(65, 66, 67, 68, 69, 70) time=0>
