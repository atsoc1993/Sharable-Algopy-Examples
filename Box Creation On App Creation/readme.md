## Summary

Creating an Application via outer transaction and Funding Account MBR & Box Storage MBR is not possible practically *(theoretically & in some testing environments, yes)*— since the payment transaction in the group will require the address of an application that has not been created and the application call will require an application ID reference & box name. The typical solution is to "two-stage" the creation of the application and subsequent box creation. This way you have a definite application ID & address to fund afterwards, but this can create tension in UX since they must sign transaction prompts twice.

**Although there is a *guessing* trick** with simulating app ID's since the resulting app ID on creation is deterministic based on TX Count, and the logic address is the hash of the constant b"appID" & the application ID bytes as a uint64 [See code at the end of this readme to see get_application_address method]— **this guessing trick is not optimal for use in outer transactions.** In mainnet environments, or any higher volumne environment, there is a good chance that the TX count between simulating and actually submitting the group will have changed; this renders the *guessed* application ID stale, and the group will fail since the **application address and App ID for the respective payment and application call transaction will not match what was predicted.**

However, with the new protocol update, **this same logic can be easily replicated via inner transactions without the *guessing* trick.** Smart contracts can contain logic to create applications from templates, and have immediate availability of the exact application ID and address without *guessing*. The box reference is also not needed with a *definite* application ID & box name bytes, an empty box reference can simply be passed and the application will resolve the box reference on its own. **This means we can create & fund an application, as well as create a box simultaneously.**

*Note: Setting box values simultaneously with the above is not available as of yet, only box names can be initially set, the box value must be empty with an initial box size of zero.*

## Replication
1. Algokit & Algokit Utils must be available globally
2. If contract changes are made, use the one-liner in compile_commands.txt
3. Although a .env is available, feel free to generate a new private & public key pair using `0_generate_account.py` & fund the account via https://bank.testnet.algorand.network/
4. Run 1_deploy.py

`deploy.py` does the following:

- Loads our .env and prepares a signing account from `sk` and `pk` env variables
- Declares the Child Template Factory & Parent Factory 
- Deploys the Child Template App from the child tempalte factory we will be creating via inner-transaction and creating a box in simultaneously at time of creation
- Deploys the Parent Factory & simultaneously assigns the application ID from the now live child template into a global state of the parent factory
- Funds the Parent Factory with Account Minimum Balance Requirement of 0.1 Algorand
- Creates a Payment Transaction to our parent factory for the upcoming application call (this is rerouted to the created child application, whose approval & clear programs are derived from the global state)
- Calls the `create_test_contract_child_and_box` method on the parent factory, which accepts the aforementioned payment and uses those funds for the MBR increases resulting from: creating the child application & funding the account MBR & Box MBR of the child application (excess is refunded to the parent factory). Then, the parent factory submits an inner abi call to the newly created child application's `create_box` method— this initializes the empty box with a box name of choice, and refunds any excess MBR, returning the amount of MBR used to the parent factory. The parent factory calculates the total MBR used, and refunds this to the initial sender of the MBR payment included in the `create_test_contract_child_and_box` method.

## Example Transaction:
https://lora.algokit.io/testnet/transaction/YIMHVBFPFNBGWMYMHC4VWZO57FNXZXVOMCXLIY7LFAJSST5QV7ZQ


## Additional Information

The code for `get_application_address` mentioned previously for the *guessing* trick.

```

# APPID_PREFIX = b"appID"

def get_application_address(appID: int) -> str:
    """
    Return the escrow address of an application.

    Args:
        appID (int): The ID of the application.

    Returns:
        str: The address corresponding to that application's escrow account.
    """
    assert isinstance(
        appID, int
    ), "(Expected an int for appID but got [{}] which has type [{}])".format(
        appID, type(appID)
    )

    to_sign = constants.APPID_PREFIX + appID.to_bytes(8, "big")
    checksum = encoding.checksum(to_sign)
    return encoding.encode_address(checksum)

def checksum(data):
    """
    Compute the checksum of arbitrary binary input.

    Args:
        data (bytes): data as bytes

    Returns:
        bytes: checksum of the data
    """
    chksum = SHA512.new(truncate="256")
    chksum.update(data)
    return chksum.digest()
```

