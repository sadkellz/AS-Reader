import pymem
from pymem.memory import read_bytes

import helper
from helper import read_int

# Could do a more sophisticated check to see if its either Slippi Dolphin or regular Dolphin.
pm = pymem.Pymem("Dolphin.exe")
EMU_SIZE = 0x2000000
PTR_CONVERT = 0x80000000
EMU_START = None


# Scans memory pages that us the same size as EMU_SIZE, this is our dolphin emulator page.
# It is possible that their are multiple pages with the same size.
def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0
    found = []

    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = pymem.pattern.scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )

        if not return_multiple and page_found:
            if (next_region - page_found) == int(EMU_SIZE):
                return page_found

        if page_found:
            if (next_region - page_found) == int(EMU_SIZE):
                found += page_found

    if not return_multiple:
        return None

    return found


# Finds 'GALE01' in memory.
# This is used to jump to specific functions in Melee ie: GALE01 + CAM_START
def find_emu_mem():
    handle = pm.process_handle
    byte_pattern = bytes.fromhex("47 41 4C 45 30 31 00 02")
    found = pattern_scan_all(handle, byte_pattern)
    return found


# data sheet https://docs.google.com/spreadsheets/d/1MIcQkeoKeXdZEoaz9EWIP1FNXSDjT3_DtHNbH3WkQMs
PLAYER_BLOCKS = [0x453080, 0x453F10, 0x454DA0, 0x455C30]
ENTITY_PTRS = [0x453130, 0x453FC0, 0x454E50, 0x455CE0]


# example function
def get_char_ids(base_addr):
    for player in PLAYER_BLOCKS:
        cid = read_int(pm, base_addr + player)
        print(cid)


def get_player_data(base_addr, port):
    # offset from:
    # https://docs.google.com/spreadsheets/d/1MIcQkeoKeXdZEoaz9EWIP1FNXSDjT3_DtHNbH3WkQMs/edit?gid=5#gid=5&range=B354
    DATA_PTR_OFST = 0x2C
    # read our pointer as bytes, not a "true" pointer because we're in emulated space
    player = pm.read_bytes(base_addr + ENTITY_PTRS[port], 4)
    # convert our ptr
    player = int.from_bytes(player, byteorder='big')
    if not player:
        return 0
    # this will get our new offset from the start of melee, "GALE01"
    ofst = player - PTR_CONVERT
    # read our next pointer, this time its to the character data
    data_ptr = pm.read_bytes(base_addr + ofst + DATA_PTR_OFST, 4)
    data_ptr = int.from_bytes(data_ptr, byteorder='big')
    if not data_ptr:
        return 0
    data_ptr = data_ptr - PTR_CONVERT
    return data_ptr


def get_action_state(base_addr, port):
    # https://docs.google.com/spreadsheets/d/1MIcQkeoKeXdZEoaz9EWIP1FNXSDjT3_DtHNbH3WkQMs/edit?gid=5#gid=5&range=A368
    STATE_OFST = 0x10
    player_data = get_player_data(base_addr, port)
    return read_int(pm, base_addr + player_data + STATE_OFST)


if __name__ == '__main__':
    EMU_START = find_emu_mem()
    data = get_player_data(EMU_START, 2)
    if not data:
        print("returned 0, probably not an active port")

    while True:
        action = get_action_state(EMU_START, 0)
        print(action)
