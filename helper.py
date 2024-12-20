import struct
# These functions are here to easily call read and writes with the correct endianess
# as Pymem does not support changing it on the fly.


def read_int(pm, address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>i', raw)[0]


def read_uint(pm, address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>I', raw)[0]


def read_float(pm, address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>f', raw)[0]


def read_short(pm, address):
    raw = pm.read_bytes(address, 2)
    return struct.unpack('>h', raw)[0]


def read_ushort(pm, address):
    raw = pm.read_bytes(address, 2)
    return struct.unpack('>H', raw)[0]


def read_long(pm, address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>l', raw)[0]


def read_ulong(pm, address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>L', raw)[0]


def write_int(pm, value, address):
    raw = struct.pack(">i", value)
    pm.write_bytes(address, raw, len(raw))


def write_uint(pm, value, address):
    raw = struct.pack(">I", value)
    pm.write_bytes(address, raw, len(raw))


def write_float(pm, value, address):
    raw = struct.pack(">f", value)
    pm.write_bytes(address, raw, len(raw))


def write_short(pm, value, address):
    raw = struct.pack(">h", value)
    pm.write_bytes(address, raw, len(raw))


def write_ushort(pm, value, address):
    raw = struct.pack(">H", value)
    pm.write_bytes(address, raw, len(raw))


def write_long(pm, value, address):
    raw = struct.pack(">l", value)
    pm.write_bytes(address, raw, len(raw))


def write_ulong(pm, value, address):
    raw = struct.pack(">L", value)
    pm.write_bytes(address, raw, len(raw))



