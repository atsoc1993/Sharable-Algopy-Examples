from algokit_utils import AlgorandClient, SigningAccount, AlgoAmount, CommonAppCallParams
from contract_files.TestClient import TestFactory, TestArc4Uint64Args, TestArc4Uint256Args, TestBiguintArgs, TestArc4Uint64WPaddingArgs, TestArc4Uint256WPaddingArgs, TestBigintWPaddingArgs #TestArc4TypesArgs, TestArc4TypesWithPaddingArgs
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


print(f'Testing Arc4 Conversions for UInt64, UInt256 & BigInt, each return should be 555 . . .')

group = test_contract_client.new_group()


group.test_arc4_uint64(
    args=TestArc4Uint64Args(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)
group.test_arc4_uint64_w_padding(
    args=TestArc4Uint64WPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)
group.test_arc4_uint256(
    args=TestArc4Uint256Args(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)
group.test_arc4_uint256_w_padding(
    args=TestArc4Uint256WPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)
group.test_biguint(
    args=TestBiguintArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)
group.test_bigint_w_padding(
    args=TestBigintWPaddingArgs(
        bytes_1=(555).to_bytes(7, 'big'),
    ),

    params=CommonAppCallParams(
        validity_window=1000
    )
)

txn_response = group.send()

print(f'All returns should be 555, Returns: {[abi_return.value for abi_return in txn_response.returns]}')

