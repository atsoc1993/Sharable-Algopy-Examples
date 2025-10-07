from algopy import ARC4Contract, arc4, UInt64, BigUInt, Bytes, op
from algopy.arc4 import abimethod


class Test(ARC4Contract):
    def __init__(self) -> None:
        pass

    @abimethod
    def test_arc4_uint64(self, bytes_1: Bytes) -> arc4.UInt64:
        return arc4.UInt64.from_bytes(bytes_1)

    @abimethod
    def test_arc4_uint256(self, bytes_1: Bytes) -> arc4.UInt256:
        return arc4.UInt256.from_bytes(bytes_1)
    
    @abimethod
    def test_biguint(self, bytes_1: Bytes) -> BigUInt:
        return BigUInt.from_bytes(bytes_1)
    
    @abimethod
    def test_arc4_uint64_w_padding(self, bytes_1: Bytes) -> arc4.UInt64:
        bytes_length = bytes_1.length
        uint64_padding_length_needed = UInt64(8) - bytes_length
        padded_bytes = op.bzero(uint64_padding_length_needed) + bytes_1
        return arc4.UInt64.from_bytes(padded_bytes) # If you're sure it'll be in the uint64 range you can just use op.btoi which pads for you
    
    @abimethod
    def test_arc4_uint256_w_padding(self, bytes_1: Bytes) -> arc4.UInt256:
        bytes_length = bytes_1.length
        uint256_padding_length_needed = UInt64(32) - bytes_length
        padded_bytes = op.bzero(uint256_padding_length_needed) + bytes_1
        return arc4.UInt256.from_bytes(padded_bytes)
    
    @abimethod
    def test_bigint_w_padding(self, bytes_1: Bytes) -> BigUInt:
        bytes_length = bytes_1.length
        uint256_padding_length_needed = UInt64(32) - bytes_length
        padded_bytes = op.bzero(uint256_padding_length_needed) + bytes_1 
        return BigUInt.from_bytes(padded_bytes)

    
