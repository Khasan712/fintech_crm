import binascii
import os

import base64


def code_decoder(code, decode=False):
    if decode:
        return base64.b64decode(code).decode()
    else:
        return base64.b64encode(f"{code}".encode("utf-8")).decode()






def generate_key(cls: int):
    return binascii.hexlify(os.urandom(cls)).decode()


