from algopy import subroutine, UInt64, Global, ARC4Contract, arc4, BoxMap, gtxn, itxn, Txn, Application, OnCompleteAction, Bytes, BoxRef
from algopy.arc4 import abimethod, abi_call


@subroutine
def get_mbr() -> UInt64:
    return Global.current_application_address.min_balance

'''
The below is not possible, as there is no way to no the receiver address available for funding the minimum balance requirement payment transaction (aside from simulating during low-traffic to obtain an app ID & therefore a logic address)

class TestContract(ARC4Contract):
    def __init__(self) -> None:
        self.test_box = BoxMap(arc4.UInt64, arc4.UInt64, key_prefix='')

    @abimethod(create='require')
    def create_box(self, mbr_payment: gtxn.PaymentTransaction) -> None:
        pre_mbr = get_mbr()

        self.test_box[arc4.UInt64(0)] = arc4.UInt64(0)

        post_mbr = get_mbr()
        
        excess_mbr = mbr_payment.amount - (post_mbr - pre_mbr)
        itxn.Payment(
            receiver=Txn.sender,
            amount=excess_mbr
        ).submit()
'''

class TestFactory(ARC4Contract):
    def __init__(self) -> None:
        self.test_contract_child = Application()

    @abimethod(allow_actions=['UpdateApplication', 'DeleteApplication'])
    def update_or_delete(self) -> None:
        pass

    @abimethod(create='require') 
    def set_test_contract_child(self, test_contract_child_app: Application) -> None:
        self.test_contract_child = test_contract_child_app
    
    @abimethod
    def create_test_contract_child_and_box(self, mbr_payment: gtxn.PaymentTransaction) -> None:
        assert mbr_payment.amount >= 1_000_000

        pre_mbr = get_mbr()

        create_child_tx = itxn.ApplicationCall(
            approval_program=self.test_contract_child.approval_program,
            clear_state_program=self.test_contract_child.clear_state_program,
            global_num_bytes=5,
            global_num_uint=5,
        ).submit()


        fund_account_mbr_before_method_is_called = itxn.Payment(
            receiver=create_child_tx.created_app.address,
            amount=100_000
        ).submit()

        inner_mbr_payment = itxn.Payment(
            receiver=create_child_tx.created_app.address,
            amount=100_000
        )

        excess_mbr_returned, txn = abi_call(
            TestChild.create_box,
            inner_mbr_payment,
            app_id=create_child_tx.created_app.id
        )

        post_mbr = get_mbr()
        mbr_diff = excess_mbr_returned + (post_mbr - pre_mbr)
        itxn.Payment(
            receiver=Txn.sender,
            amount=mbr_diff
        ).submit()
        
    @abimethod
    def create_test_contract_child_call_do_something_else(self, mbr_payment: gtxn.PaymentTransaction) -> None:
        pre_mbr = get_mbr()

        create_child_tx = itxn.ApplicationCall(
            approval_program=self.test_contract_child.approval_program,
            clear_state_program=self.test_contract_child.clear_state_program,
            global_num_bytes=5,
            global_num_uint=5,
        ).submit()


        abi_call(
            TestChild.do_something_else_without_boxes,
            app_id=create_child_tx.created_app.id
        )

        post_mbr = get_mbr()
        mbr_diff = mbr_payment.amount - (post_mbr - pre_mbr)
        itxn.Payment(
            receiver=Txn.sender,
            amount=mbr_diff
        ).submit()

class TestChild(ARC4Contract):
    def __init__(self) -> None:
        # Cannot use box maps as the initial value must be empty, the box can only be created
        # self.test_box = BoxMap(arc4.UInt64, arc4.UInt64, key_prefix='')
        pass
    @abimethod(allow_actions=['UpdateApplication', 'DeleteApplication'])
    def update_or_delete(self) -> None:
        pass

    @abimethod
    def create_box(self, mbr_payment: gtxn.PaymentTransaction) -> UInt64:
        pre_mbr = get_mbr()
        if Global.current_application_address.balance == 0:
            pre_mbr = UInt64(0)

        test_box = BoxRef(key=arc4.UInt64(0).bytes)
        test_box.create(size=0)

        # self.test_box[arc4.UInt64(0)] = arc4.UInt64(0)

        post_mbr = get_mbr()
        

        excess_mbr = mbr_payment.amount - (post_mbr - pre_mbr)

        itxn.Payment(
            receiver=Txn.sender,
            amount=excess_mbr
        ).submit()

        return excess_mbr

    @abimethod
    def do_something_else_without_boxes(self) -> None:
        pass

