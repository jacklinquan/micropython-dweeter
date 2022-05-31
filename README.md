# micropython-dweeter
[![PayPal Donate][paypal_img]][paypal_link]
[![PyPI version][pypi_img]][pypi_link]
[![Downloads][downloads_img]][downloads_link]

  [paypal_img]: https://github.com/jacklinquan/images/blob/master/paypal_donate_badge.svg
  [paypal_link]: https://www.paypal.me/jacklinquan
  [pypi_img]: https://badge.fury.io/py/micropython-dweeter.svg
  [pypi_link]: https://badge.fury.io/py/micropython-dweeter
  [downloads_img]: https://pepy.tech/badge/micropython-dweeter
  [downloads_link]: https://pepy.tech/project/micropython-dweeter

A python module for messaging through the free dweet service.
Dweet is a simple machine-to-machine (M2M) service from [dweet.io](https://dweet.io).

This module works under MicroPython and it is tested with MicroPython V1.18.
It requires [micropython-cryptodweet](https://github.com/jacklinquan/micropython-cryptodweet).

For a compatible CPython version, please find [Python package dweeter](https://github.com/jacklinquan/dweeter).

## Installation
``` Python
>>> import upip
>>> upip.install('micropython-dweeter')
```
Alternatively just copy dweeter.py and its dependency to the MicroPython device.

## Usage
``` python
>>> from dweeter import Dweeter
>>> dwtr = Dweeter("YOUR MAILBOX", "YOUR KEY")
>>> dwtr.send_data({"STRING DATA": "STRING VALUE", "INT DATA": 100, "FLOAT DATA": 3.14, "BOOL DATA": True})
{'thing': '3e7cb39f82fb1ac29e40b935a3cbbaed', 'created': '2022-05-30T04:15:54.787Z', 'content': {'68fcbe24759c8aeb21633df279049eb441eb7c7bcb8b4645f206f55f659fd198': '3aef3ed5ce517e4da35874b765c989256adf568525d43f8da6c2bab602ec5934c667da430fc4e43705699e57ced03d20a270fef33bfc7d1cc2b4f00255c794f00497d29717499ec0c2296b8b52fbef6e015ac0be42de9c8fdfb5f85a5455412cc14bb40acb0f9eaeb606a027b2de1acf94c630f86b5eac56add50048cad47fe5f1b2a699088153e0bf8aa3247192badc'}, 'transaction': '342e85f2-c4dc-4831-a746-e45f50885092'}
>>> dwtr.get_new_data()
{'STRING DATA': 'STRING VALUE', 'INT DATA': 100, 'FLOAT DATA': 3.14, 'BOOL DATA': True, 'remote_time': '2022-05-30T04:15:49.000Z', 'created_time': '2022-05-30T04:15:54.787Z'}
```

## On messaging security
The free dweet service is public.
By "public", it means:
- Every one on Internet can see what you are sending.
- Every one can send something for the same "thing" name to confuse you.

The publicly exposed user information:
- The "thing" name, which you can think of as the unique virtual mailbox name.
- The keys of the "content" dictionary.
- The values of the "content" dictionary.

The dweeter module wraps the contents as a single key-value pair.
So there is only one key and one value in the "content" dictionary.
And the "thing" name and the "content" dictionary are encrypted.
So no one knows what they mean.

Without knowing what the information means,
potential attackers can still send something for the same "thing" name.
Because the "content" dictionary is encrypted,
the only way to do this is to capture a bunch of messages
and send them randomly.
The key and the value of the "content" dictionary both include
the same time stamp.
A mismatch of them will result in an error that is handled by dweeter.
But a copy of the whole "content" dictionary could
still be passed on to the receiver.
This is often referred to as "replay attack".

The decrypted user data dictionary includes 2 extra key-value pairs:
- "created_time", the timestamp from the dweet service.
- "remote_time", the timestamp from the sending device.

You can compare these two timestamps to decide if a "replay attack" happened.
On a micropython device, you can use `ntptime.settime()` to set the local time.
Be aware of a normal gap between "created_time" and "remote_time".
On a PC I observed 4 to 5 seconds difference.
On a micropython device I observed 8 to 9 seconds difference.
This time difference could vary from case to case.
