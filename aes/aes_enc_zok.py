#!/usr/bin/env python3
"""
This is an exercise in secure symmetric-key encryption, implemented in pure
Python (no external libraries needed).

Original AES-128 implementation by Bo Zhu (http://about.bozhu.me) at
https://github.com/bozhu/AES-Python . PKCS#7 padding, CBC mode, PKBDF2, HMAC,
byte array and string support added by me at https://github.com/boppreh/aes.
Other block modes contributed by @righthandabacus.


Although this is an exercise, the `encrypt` and `decrypt` functions should
provide reasonable security to encrypted messages.
"""


s_box = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]


def sub_bytes(s):
    # s: field[4][4]
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


def shift_rows(s):
    # s: field[4][4]
    s1 = []
    for i in range(4):
        s1.append(list(s[i]))
    s[0][1] = s1[1][1]
    s[1][1] = s1[2][1]
    s[2][1] = s1[3][1]
    s[3][1] = s1[0][1]

    s[0][2] = s1[2][2]
    s[1][2] = s1[3][2]
    s[2][2] = s1[0][2]
    s[3][2] = s1[1][2]

    s[0][3] = s1[3][3]
    s[1][3] = s1[0][3]
    s[2][3] = s1[1][3]
    s[3][3] = s1[2][3]


def add_round_key(s, k):
    # s, k: field[4][4]
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
def xtime(a):
    # a: field
    if (a & 0x80):
        return ((a << 1) ^ 0x1B) & 0xFF
    else:
        return a << 1


def mix_single_column(a):
    # a: field[4]
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    # s: field[4][4]
    for i in range(4):
        mix_single_column(s[i])


r_con = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
]


def bytes2matrix(text):
    # text: feild[16]
    """ Converts a 16-byte array into a 4x4 matrix.  """
    l = []
    for i in range(0, 16, 4):
        l.append(list(v for v in text[i:i+4]))
    return l


def matrix2bytes(matrix):
    # matrix: field[4][4]
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))


def xor4(a, b):
    # field[4]
    l = []
    for i in range(4):
        l.append(a[i] ^ b[i])
    return l


def xor16(a, b):
    # field[16]
    l = []
    for i in range(16):
        l.append(a[i] ^ b[i])
    return l


def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    l = []
    for i in range(0, len(message), block_size):
        l.append(message[i:i+16])
    return l


# ==================AES================

def helper_in_expand_key(word, i):
    temp = word[0]
    word[0] = word[1]
    word[1] = word[2]
    word[2] = word[3]
    word[3] = temp
    # Map to S-BOX.
    # word = [s_box[b] for b in word]
    for j in range(4):
        word[j] = s_box[word[j]]
    # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
    word[0] ^= r_con[i]
    return word


def _expand_key(master_key, n_rounds):
    """
    Expands and returns a list of key matrices for the given master_key.
    """
    # Initialize round keys with raw key material.
    key_columns = bytes2matrix(master_key)
    iteration_size = 4

    len_key_columns = len(key_columns)
    var_key_colums = list(key_columns)
    i = 1
    for len_key_columns in range(4, (n_rounds+1)*4):
        # Copy previous word.
        word = list(var_key_colums[len_key_columns-1])  # copy

        # Perform schedule_core once every "row".
        if len_key_columns % iteration_size == 0:
            word = helper_in_expand_key(word, i)
            i += 1
        # XOR with equivalent word from previous iteration.
        word = xor4(word, var_key_colums[len_key_columns-iteration_size])
        var_key_colums.append(word)
    return [var_key_colums[4*i: 4*(i+1)] for i in range(11)]


def encrypt_block(plaintext, _key_matrices, n_rounds):
    # _key_matrices: u8[11][4]
    """
    Encrypts a single block of 16 byte long plaintext.
    """
    assert len(plaintext) == 16

    plain_state = bytes2matrix(plaintext)

    add_round_key(plain_state, _key_matrices[0])

    for i in range(1, n_rounds):
        sub_bytes(plain_state)
        shift_rows(plain_state)
        mix_columns(plain_state)
        add_round_key(plain_state, _key_matrices[i])

    sub_bytes(plain_state)
    shift_rows(plain_state)
    add_round_key(plain_state, _key_matrices[-1])

    return matrix2bytes(plain_state)


def encrypt_cbc(plaintext, master_key, iv):
    def pad(plaintext):
        # 客户端做
        """
        Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
        Note that if the plaintext size is a multiple of 16,
        a whole block will be added.
        """
        padding_len = 16 - (len(plaintext) % 16)
        padding = bytes([padding_len] * padding_len)
        return plaintext + padding

    # plaintext = pad(plaintext)  # 这一步在客户端做

    # plaintext: field[]
    # master_key: field[16]
    # iv: field[16]
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}
    n_rounds = rounds_by_key_size[len(master_key)]  # 取决于密钥长度
    _key_matrices = _expand_key(master_key, n_rounds)
    print("plain text: ", [v for v in plaintext])
    print("master key: ", [v for v in master_key])

    assert len(iv) == 16
    return encrypt_block(plaintext, _key_matrices, n_rounds)
    # return encrypt_block(xor16(plaintext, iv), _key_matrices, n_rounds)

    blocks = []
    previous = iv
    for plaintext_block in split_blocks(plaintext):
        # CBC mode encrypt: encrypt(plaintext_block XOR previous)
        block = encrypt_block(
            xor16(plaintext_block, previous), _key_matrices, n_rounds)
        blocks.append(block)
        previous = block

    return b''.join(blocks)


if __name__ == "__main__":
    key = b'12345678abcdefgh'
    # iv = os.urandom(16)
    iv = b'12345678abcdefgh'
    encrypted = encrypt_cbc(b'12345678abcdefgh', key, iv)
    print("cipher: ", [v for v in encrypted])
    # print(encrypted)
