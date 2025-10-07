from algokit_utils import AlgorandClient, SigningAccount, CommonAppCallParams, PaymentParams, AlgoAmount, ABIType
from contract_files.TestClient import (
    TestFactory, 
    TestArc4Uint64Args, 
    TestArc4Uint256Args, 
    TestBiguintArgs, 
    TestArc4Uint64WPaddingArgs, 
    TestArc4Uint256WPaddingArgs, 
    TestBigintWPaddingArgs,
    TestMathOnUnresolvedArc4Uint64Args,
    TestStorageOnResolvedArc4Uint64Args
    #TestArc4TypesArgs, 
    # TestArc4TypesWithPaddingArgs
)
from dotenv import load_dotenv
import os


load_dotenv('Bytes To Arc4 UIntNs Check/.env')
sk = os.getenv('sk')
pk = os.getenv('pk')

algorand = AlgorandClient.testnet()

test_account = SigningAccount(
    private_key=sk,
    address=pk
)

test_contract_factory =  TestFactory(
    algorand=algorand,
    default_sender=test_account.address,
    default_signer=test_account.signer,
)

print(f'Deploying Test Contract . . .')
test_contract_client, deploy_response = test_contract_factory.send.create.bare()
print(f'Deployed Test Contract, App ID: {test_contract_client.app_id}')

print(f'Funding Account MBR for Box Storage . . .')
mbr_payment = algorand.send.payment(
    PaymentParams(
        sender=test_account.address,
        signer=test_account.signer,
        receiver=test_contract_client.app_address,
        amount=AlgoAmount(micro_algo=100_000),
        validity_window=1000
    ),
)
print(f'Funding Account MBR.')


print(f'Testing Arc4 Conversions for UInt64, UInt256 & BigInt, each return should be 555 . . .')

group = test_contract_client.new_group()

group.test_arc4_uint64(
    args=TestArc4Uint64Args(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)

group.test_arc4_uint256(
    args=TestArc4Uint256Args(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)

group.test_biguint(
    args=TestBiguintArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)

group.test_arc4_uint64_w_padding(
    args=TestArc4Uint64WPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)

group.test_arc4_uint256_w_padding(
    args=TestArc4Uint256WPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)

group.test_bigint_w_padding(
    args=TestBigintWPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)
    )
)
group.test_math_on_unresolved_arc4_uint64(
    args=TestMathOnUnresolvedArc4Uint64Args(
        bytes_1=(555).to_bytes(7, 'big'),
    ),
    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=1000)

    )
)


mbr_payment = algorand.create_transaction.payment(
    PaymentParams(
        sender=test_account.address,
        signer=test_account.signer,
        receiver=test_contract_client.app_address,
        amount=AlgoAmount(micro_algo=20_000),
        validity_window=1000
    ),
)
group.test_storage_on_resolved_arc4_uint64(
    args=TestStorageOnResolvedArc4Uint64Args(
        bytes_1=(555).to_bytes(7, 'big'),
        mbr_payment=mbr_payment
    ),
    params=CommonAppCallParams(
        validity_window=1000,
        max_fee=AlgoAmount(micro_algo=2000)
    ),
)
txn_response = group.send(
    send_params={
        'populate_app_call_resources': True,
        'cover_app_call_inner_transaction_fees': True
    }
)

print(f'All returns should be 555, the last return should be 556, Returns: {[abi_return.value for abi_return in txn_response.returns]}')

try:
    box_name_abi_type = ABIType.from_string('uint64')
    box_name_raw = algorand.app.get_box_names(test_contract_client.app_id)[0].name_raw
    box_name_decoded_as_uint64 = box_name_abi_type.decode(box_name_raw)
    print(f'When storing an unresolved arc4.UInt64 the value is: {box_name_decoded_as_uint64}')
except Exception as e:
    print(e)
    print(f'arc4.UInt64 was stored as {len(box_name_raw)} bytes and cannot be decoded as uint64')

