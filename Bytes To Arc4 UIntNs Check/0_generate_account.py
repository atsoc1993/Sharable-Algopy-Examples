from algosdk.account import generate_account
from dotenv import load_dotenv, set_key

load_dotenv('Box Creation On App Creation/.env')
sk, pk = generate_account()
set_key('Box Creation On App Creation/.env', 'sk', sk)
set_key('Box Creation On App Creation/.env', 'pk', pk)