from algopy import ARC4Contract, arc4, subroutine, Account, Global, itxn, UInt64, Txn, BoxMap, gtxn, urange
from algopy.arc4 import Struct, DynamicBytes, DynamicArray, abimethod

class SomeStruct(Struct):
    uint64_1: arc4.UInt64
    uint256_1: arc4.UInt256
    unknown_length_byte_array: DynamicBytes
    unknown_length_uint64_array: DynamicArray[arc4.UInt64]
    uint64_2: arc4.UInt64


@subroutine
def get_mbr() -> UInt64:
    return Global.current_application_address.min_balance

@subroutine
def refund_excess_mbr(excess: UInt64) -> None:
    itxn.Payment(
        receiver=Txn.sender,
        amount=excess
    ).submit()

class Test(ARC4Contract):
    def __init__(self) -> None:
        self.test_box_map = BoxMap(Account, SomeStruct, key_prefix='t1')
        self.test_nested_struct_box_map = BoxMap(Account, DynamicArray[SomeStruct], key_prefix='t2')
        
    @abimethod
    def write_box(
        self, 
        uint64_1: arc4.UInt64, 
        uint256_1: arc4.UInt256, 
        unknown_length_byte_array: DynamicBytes, 
        unknown_length_uint64_array: DynamicArray[arc4.UInt64],
        uint64_2: arc4.UInt64,
        mbr_payment: gtxn.PaymentTransaction
    ) -> None:
        
        box_value = SomeStruct(
            uint64_1=uint64_1,
            uint256_1=uint256_1,
            unknown_length_byte_array=unknown_length_byte_array.copy(),
            unknown_length_uint64_array=unknown_length_uint64_array.copy(),
            uint64_2=uint64_2
        )

        pre_mbr = get_mbr()
        self.test_box_map[Txn.sender] = box_value.copy()
        post_mbr = get_mbr()

        mbr_needed = post_mbr - pre_mbr
        excess_mbr_funded = mbr_payment.amount - mbr_needed
        refund_excess_mbr(excess=excess_mbr_funded)


    @abimethod
    def get_item_by_index_in_uint64_array(self, index: UInt64) -> arc4.UInt64:
        box_value = self.test_box_map[Txn.sender].copy()
        return box_value.unknown_length_uint64_array[index]

    @abimethod
    def find_item_index_in_uint64_array(self, target_uint64: arc4.UInt64) -> tuple[arc4.UInt64, UInt64]:
        box_value = self.test_box_map[Txn.sender].copy()
        uint64_dynamic_array = box_value.unknown_length_uint64_array.copy()
        for i in urange(box_value.unknown_length_uint64_array.length):
            if uint64_dynamic_array[i] == target_uint64:
                return uint64_dynamic_array[i], i
            
        return arc4.UInt64(0), UInt64(0)

    @abimethod
    def adjust_item_at_index(self, index: UInt64, new_num: arc4.UInt64) -> None:
        box_value = self.test_box_map[Txn.sender].copy()
        uint64_dynamic_array = box_value.unknown_length_uint64_array.copy()
        uint64_dynamic_array[index] = new_num
        box_value.unknown_length_uint64_array = uint64_dynamic_array.copy()
        self.test_box_map[Txn.sender] = box_value.copy()

    @abimethod
    def dynamic_array_of_structs_write_box(self, dynamic_structs: DynamicArray[SomeStruct], mbr_payment: gtxn.PaymentTransaction) -> None:
        pre_mbr = get_mbr()
        self.test_nested_struct_box_map[Txn.sender] = dynamic_structs.copy()
        post_mbr = get_mbr()

        mbr_needed = post_mbr - pre_mbr
        excess_mbr_funded = mbr_payment.amount - mbr_needed
        refund_excess_mbr(excess=excess_mbr_funded)

    @abimethod
    def dynamic_array_of_structs_get_item_by_index_in_uint64_array(self, struct_index: UInt64, index: UInt64) -> arc4.UInt64:
        box_value = self.test_nested_struct_box_map[Txn.sender].copy()
        target_struct = box_value[struct_index].copy()
        return target_struct.unknown_length_uint64_array[index]

    @abimethod
    def dynamic_array_of_structs_find_item_index_in_uint64_array(self, struct_index: UInt64, target_uint64: arc4.UInt64) -> tuple[arc4.UInt64, UInt64]:
        box_value = self.test_nested_struct_box_map[Txn.sender].copy()
        target_struct = box_value[struct_index].copy()
        uint64_dynamic_array = target_struct.unknown_length_uint64_array.copy()
        for i in urange(target_struct.unknown_length_uint64_array.length):
            if uint64_dynamic_array[i] == target_uint64:
                return uint64_dynamic_array[i], i
            
        return arc4.UInt64(0), UInt64(0)

    @abimethod
    def dynamic_array_of_structs_adjust_item_at_index(self, struct_index: UInt64, index: UInt64, new_num: arc4.UInt64) -> None:
        box_value = self.test_nested_struct_box_map[Txn.sender].copy()
        target_struct = box_value[struct_index].copy()
        uint64_dynamic_array = target_struct.unknown_length_uint64_array.copy()
        uint64_dynamic_array[index] = new_num
        box_value[struct_index].unknown_length_uint64_array = uint64_dynamic_array.copy()
        self.test_nested_struct_box_map[Txn.sender] = box_value.copy()
    


