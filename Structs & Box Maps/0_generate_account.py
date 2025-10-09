from algosdk.account import generate_account
from dotenv import load_dotenv, set_key

load_dotenv('Structs & Box Maps/.env')
sk, pk = generate_account()
set_key('Structs & Box Maps/.env', 'sk', sk)
set_key('Structs & Box Maps/.env', 'pk', pk)