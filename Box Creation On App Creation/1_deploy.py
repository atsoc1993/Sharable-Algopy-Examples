from algokit_utils import AlgorandClient, SigningAccount, PaymentParams, BoxIdentifier, AlgoAmount, CommonAppCallParams, OnUpdate, OnSchemaBreak, BoxReference
from contract_files.TestFactoryClient import (
    TestFactoryFactory, 
    SetTestContractChildArgs, 
    CreateTestContractChildAndBoxArgs, 
    CreateTestContractChildCallDoSomethingElseArgs, 
    TestFactoryMethodCallCreateParams,
)
from contract_files.TestChildClient import TestChildFactory
from dotenv import load_dotenv
import os


load_dotenv('Box Creation On App Creation/.env')
sk = os.getenv('sk')
pk = os.getenv('pk')

algorand = AlgorandClient.testnet()

test_account = SigningAccount(
    private_key=sk,
    address=pk
)


test_contract_child_factory =  TestChildFactory(
    algorand=algorand,
    default_sender=test_account.address,
    default_signer=test_account.signer,
)

print(f'Deploying Child Contract Template . . .')
test_contract_template_client, deploy_response = test_contract_child_factory.send.create.bare()
print(f'Deployed Child Contract Template, App ID: {test_contract_template_client.app_id}')

test_contract_factory_factory = TestFactoryFactory(
    algorand=algorand,
    default_sender=test_account.address,
    default_signer=test_account.signer,
)

# Not recommended to use Deploy if global states change on creation when testing but the approval program and schema of the contract does not
print(f'Deploying Factory and setting child app ID to global state . . .')
factory_client, factory_deploy_resonse = test_contract_factory_factory.deploy(
    on_update=OnUpdate.AppendApp,
    on_schema_break=OnSchemaBreak.AppendApp,
    create_params=TestFactoryMethodCallCreateParams(
        args=SetTestContractChildArgs(
            test_contract_child_app=test_contract_template_client.app_id

        ),
        validity_window=1000,
    ),
)
print(f'Deployed and Global State set, App ID: {factory_client.app_id}')


# print(f'Creating Factory App without Deploy Method, removed `require` on set test contract child method')
# factory_client, factory_deploy_response = test_contract_factory_factory.send.create.bare()

# factory_client.send.set_test_contract_child(
#     args=SetTestContractChildArgs(
#         test_contract_child_app=test_contract_template_client.app_id,
#     ),
#     params=CommonAppCallParams(
#         validity_window=1000
#     )
# )
# print(f'Deployed and Global State set, App ID: {factory_client.app_id}')


print(f'Funding Account MBR for Factory . . .')
algorand.send.payment(
    params=PaymentParams(
        receiver=factory_client.app_address,
        sender=test_account.address,
        signer=test_account.signer,
        amount=AlgoAmount(micro_algo=100_000),
        validity_window=1000
    )
)
print(f'Funded Account MBR for Factory')

print(f'Testing Child Contract Creation where a box is set at creation . . .')
mbr_payment = algorand.create_transaction.payment(
    PaymentParams(
        sender=test_account.address,
        signer=test_account.signer,
        amount=AlgoAmount(algo=3),
        receiver=factory_client.app_address,
        validity_window=1000

    )
)

txn_response= factory_client.send.create_test_contract_child_and_box(
    args=CreateTestContractChildAndBoxArgs(
        mbr_payment=mbr_payment,
    ),
    params=CommonAppCallParams(
        app_references=[0, test_contract_template_client.app_id],
        box_references=[
            BoxReference(app_id=0 name=b''), #also tried with a app id 0 & actual box name
        ],
        extra_fee=AlgoAmount(micro_algo=10_000),
        validity_window=1000
    )

)

#Successful test for arbitrary inner app call
# txn_response = factory_client.send.create_test_contract_child_call_do_something_else(
#     args=CreateTestContractChildCallDoSomethingElseArgs(
#         mbr_payment=mbr_payment
#     ),
#     params=CommonAppCallParams(
#         extra_fee=AlgoAmount(micro_algo=4000)
#     ),
#     send_params={
#         'suppress_log': False,
#     }
# )
print(f'Child contract created successfully with box, Tx ID: {txn_response.tx_id[0]}')
