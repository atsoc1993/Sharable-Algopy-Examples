from algokit_utils import AlgorandClient, SigningAccount, PaymentParams, AlgoAmount, CommonAppCallParams, ABIType
from contract_files.TestClient import (
    TestFactory, 
    SomeStruct,
    WriteBoxArgs, 
    GetItemByIndexInUint64ArrayArgs, 
    FindItemIndexInUint64ArrayArgs, 
    AdjustItemAtIndexArgs,
    DynamicArrayOfStructsWriteBoxArgs,
    DynamicArrayOfStructsGetItemByIndexInUint64ArrayArgs,
    DynamicArrayOfStructsFindItemIndexInUint64ArrayArgs,
    DynamicArrayOfStructsAdjustItemAtIndexArgs
)
from dotenv import load_dotenv
import os


load_dotenv('Structs & Box Maps/.env')
sk = os.getenv('sk')
pk = os.getenv('pk')

algorand = AlgorandClient.testnet()

test_account = SigningAccount(
    private_key=sk,
    address=pk
)



test_contract_factory = TestFactory(
    algorand=algorand,
    default_sender=test_account.address,
    default_signer=test_account.signer
)
print(f'Deploying Contract . . .')
test_contract_client, deploy_response = test_contract_factory.send.create.bare()
print(f'Deployed Contract, App ID: {test_contract_client.app_id}')


print(f'\nFunding Account MBR for app address . . .')
algorand.send.payment(
    params=PaymentParams(
        receiver=test_contract_client.app_address,
        sender=test_account.address,
        signer=test_account.signer,
        amount=AlgoAmount(micro_algo=100_000),
        validity_window=1000
    )
)
print(f'Funded Account MBR for app address.')

print(f'\nCalling Write Box . . .')
mbr_payment = algorand.create_transaction.payment(
    PaymentParams(
        sender=test_account.address,
        signer=test_account.signer,
        amount=AlgoAmount(algo=3),
        receiver=test_contract_client.app_address,
        validity_window=1000

    )
)

txn_response_1 = test_contract_client.send.write_box(
    args=WriteBoxArgs(
        uint64_1=7,
        uint64_2=25,
        uint256_1=64312346235,
        unknown_length_byte_array=b'Some Random Bytes',
        unknown_length_uint64_array=[3, 6, 9, 12, 15, 17, 21], #17 will later be changed to 18
        mbr_payment=mbr_payment,
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True,
        'cover_app_call_inner_transaction_fees': True
    }
)
print(f'Wrote to Box, Tx ID: {txn_response_1.tx_id}')

address_coder = ABIType.from_string('address')
box_name = b't1' + address_coder.encode(test_account.address)
box_value_coder = ABIType.from_string('(uint64,uint256,byte[],uint64[],uint64)')
box_value = algorand.app.get_box_value_from_abi_type( 
    app_id=test_contract_client.app_id,
    box_name=box_name,
    abi_type=box_value_coder
)
print(f'Box Bytes: {box_value_coder.encode(box_value)}')
print(f'Box Decoded: {box_value}')



target_index = 5
print(f'\nGetting item at index {target_index} . . .')
txn_response_2 = test_contract_client.send.get_item_by_index_in_uint64_array(
    args=GetItemByIndexInUint64ArrayArgs(index=5),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Got Item at index {target_index}: {txn_response_2.returns[0].value}, Tx ID: {txn_response_2.tx_id}')

target_item = txn_response_2.returns[0].value
print(f'\nFinding index for item: {target_item} . . .')
txn_response_3 = test_contract_client.send.find_item_index_in_uint64_array(
    args=FindItemIndexInUint64ArrayArgs(target_uint64=target_item),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Found index for {target_item}, Index: {txn_response_3.returns[0].value}, Tx ID: {txn_response_3.tx_id}')

new_num = 18
print(f'\nAdjusting uint64 {target_item} at index {target_index} to {new_num} . . .')
txn_response_4 = test_contract_client.send.adjust_item_at_index(
    args=AdjustItemAtIndexArgs(index=target_index, new_num=new_num),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Adjusted, Tx ID: {txn_response_4.tx_id}.')

box_value = algorand.app.get_box_value_from_abi_type(
    app_id=test_contract_client.app_id,
    box_name=box_name,
    abi_type=box_value_coder
)

print(f'Box Bytes: {box_value_coder.encode(box_value)}')
print(f'Box Decoded: {box_value}')

'''

DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW
DYNAMIC STRUCT SECTION BELOW


'''
print(f'\nCalling Struct Write Box . . .')
mbr_payment_2 = algorand.create_transaction.payment(
    PaymentParams(
        sender=test_account.address,
        signer=test_account.signer,
        amount=AlgoAmount(algo=3),
        receiver=test_contract_client.app_address,
        validity_window=1000

    )
)

struct_1 = SomeStruct(
    uint64_1=7,
    uint64_2=25,
    uint256_1=64312346235,
    unknown_length_byte_array=b'Some Random Bytes',
    unknown_length_uint64_array=[3, 6, 9, 12, 15, 18, 21]
)

struct_2 = SomeStruct(
    uint64_1=88,
    uint64_2=99,
    uint256_1=999999999,
    unknown_length_byte_array=b'Some Other Random Bytes',
    unknown_length_uint64_array=[4, 8, 12, 16, 19, 24] #19 will later be changed to 20
)

txn_response_5 = test_contract_client.send.dynamic_array_of_structs_write_box(
    args=DynamicArrayOfStructsWriteBoxArgs(
        dynamic_structs=[struct_1, struct_2],
        mbr_payment=mbr_payment_2,
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True,
        'cover_app_call_inner_transaction_fees': True
    }
)
print(f'Wrote to Box w/ Dynamic Structs, Tx ID: {txn_response_5.tx_id}')

box_name = b't2' + address_coder.encode(test_account.address)
box_value_coder_2 = ABIType.from_string('(uint64,uint256,byte[],uint64[],uint64)[]')
box_value = algorand.app.get_box_value_from_abi_type(
    app_id=test_contract_client.app_id,
    box_name=box_name,
    abi_type=box_value_coder_2
)
print(f'Box Bytes: {box_value_coder_2.encode(box_value)}')
print(f'Box Decoded: {box_value}')



struct_index = 1 # The 2nd struct in our box with structs, [struct_1, struct_2]
target_index = 4 # The third integer in our dynamic uint64 array within the 2nd struct
print(f'\nGetting uint64 at index {target_index} of struct at index {struct_index} . . .')
txn_response_6 = test_contract_client.send.dynamic_array_of_structs_get_item_by_index_in_uint64_array(
    args=DynamicArrayOfStructsGetItemByIndexInUint64ArrayArgs(
        struct_index=struct_index,
        index=target_index
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Item at index {target_index} in struct at index {struct_index}: {txn_response_6.returns[0].value}, Tx ID: {txn_response_6.tx_id}')

target_item = txn_response_6.returns[0].value
print(f'\nFinding index for item: {target_item} . . .')
txn_response_7 = test_contract_client.send.dynamic_array_of_structs_find_item_index_in_uint64_array(
    args=DynamicArrayOfStructsFindItemIndexInUint64ArrayArgs(struct_index=struct_index, target_uint64=target_item),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Found index for {target_item} in struct at index {struct_index}, Index: {txn_response_7.returns[0].value}, Tx ID: {txn_response_7.tx_id}')

print(f'\nAdjusting uint64 {target_item} at index {target_index} to {new_num} . . .')
new_num = 20
txn_response_8 = test_contract_client.send.dynamic_array_of_structs_adjust_item_at_index(
    args=DynamicArrayOfStructsAdjustItemAtIndexArgs(struct_index=struct_index, index=target_index, new_num=new_num),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2_000),
        validity_window=1000
    ),
    send_params={
        'populate_app_call_resources': True
    }
)

print(f'Adjusted, Tx ID: {txn_response_8.tx_id}')

box_value = algorand.app.get_box_value_from_abi_type(
    app_id=test_contract_client.app_id,
    box_name=box_name,
    abi_type=box_value_coder_2
)
print(f'Box Bytes: {box_value_coder_2.encode(box_value)}')
print(f'Box Decoded: {box_value}')
