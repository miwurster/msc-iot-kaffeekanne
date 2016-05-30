
# IoT Kaffeekanne - Sensor

## Hardware

The amount of remaining coffee inside the coffeepot can be measured using the current weight of the
pot and comparing it with the weight it has when it is empty/full.
We used the [GRAM RK-30](http://gram.es/eng/productos012.php?idc=46&idp=217) scale for measuring
the weight. The scale has a RS-232 serial output and comes with an USB adapter. The USB adapter
is implemented as keyboard emulator, meaning it exposes itself as a HID keyboard device and
(virtually) "presses" keys to transmit data.

### Keyboard Output Format

The _GRAM RK-30_ scale supports various output formats for the serial output port.
Here, we choose the **UKEY** output format, which looks as follows:

```
<Digit>     ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<Number>    ::= <Digit> | <Digit> <Number>
<EOL>       ::= \n
<Space>     ::= ' ' | ' ' <Space>
<Line>      ::= <Space> <Number> <EOL>
<UKEY>      ::= <Line> | <UKEY> <Line>
```

Where each `<Line>` is interpreted as single measurement sample and the `<Number>` is the weight,
currently measured by the scale (in gram `g`). Lines have a fixed length. Numbers are right-aligned
on the line and prepended by spaces.

```
Example output:

         0
         0
        12
       200
```

The last line, shown in the example above, corresponds to a weight of 200g. The USB keyboard adapter
would in this case "press" the following keys:

```
KEY_SPACE
KEY_SPACE
KEY_SPACE
KEY_SPACE
KEY_SPACE
KEY_SPACE
KEY_SPACE
KEY_2
KEY_0
KEY_0
KEY_EOL
```

**TODO:** _Document the exact length of a line._

### Measurement Rate

The scale supports three printing modes: _Keypress_, _Stable_ and _Continous_. In the _Keypress_
mode, it only prints when pressing a specific key on the scale. The _Stable_ mode prints the
weight as soon as the scale detects that weight doesn't change anylonger. Here, the _Continous_
mode was chosen where the scale continously prints the current weight.
The USB keyboard adapter of the _GRAM RK-30_ scale forwards **6 Lines/Second** in the format
described above.

## Capturing Input Data

We chose to use Linux on a _Raspberry Pi_ for capturing data from the scale and to forward it to
a cloud-based service for further processing. When plugging in the USB keyboard adapter, the Linux
_usbhid_ kernel module recognizes a new HID (Human Interface Device) keyboard and as the scale
was set to _Continous_ printing mode, soon the Linux console gets spammed with keypresses.

Therefore, we chose to directly capture the events from the Linux keyboard device using a Python
script. The script exclusively grabs the device, so the console doesn't get spammed with keypresses.
It therefore uses _udev_ (Userspace Devices) to detect when the USB keyboard adapter gets plugged-in
and immediately afterwards requests the exclusive access for the device.

The Linux kernel exposes the keyboard device in the filesystem tree under `/dev/input/eventXX`
(where `XX` is replaced by an incremental number -- e.g. `/dev/input/event19`). It can be opened
like a file and data can be read from it, e.g. using the POSIX `select` and `read` functions. The
data is in a binary format, which is described on the [Linux Kernel Website](https://www.kernel.org/doc/Documentation/input/input.txt).

We chose to use the _Python_ programming language to read the data from the device input file as
there are already good and easy-to-use modules available that implement the parsing of the binary
input event format. Here, we use the [`python-evdev` module](http://python-evdev.readthedocs.io/en/latest/).

![Reading Keypress Activity Diagram](http://yuml.me/77b125cb)
