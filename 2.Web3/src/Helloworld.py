from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
import time
import json

provider_url = "https://data-seed-prebsc-1-s1.binance.org:8545" # rpc link
web3 = Web3(HTTPProvider(provider_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

#check connect successfull
isConnected = web3.isConnected()
print(f"Successful Connection: {isConnected} ")
#check latest blocknumber
blocknumber = web3.eth.block_number
print(f"The latest blocknumber is: {blocknumber}")
data = web3.eth.get_block(blocknumber)
# print(data)
#lấy cấu trúc dữ liệu của abi
with open("../abi/duccontract.json", "r") as f:
    abi = json.loads(f.read())
#Địa chỉ của valas  
address = "0x1809a5EB1F851c5108061Ea3B26bCdb69367c83C"
# Kiểm tra xem địa chỉ có đúng không
if not web3.isAddress(address):
    address = web3.toChecksumAddress(address)
#Sử dụng web3 thiết lập đối tượng contract để sử dụng các phương thức
contract = web3.eth.contract(abi=abi, address=address)
events = contract.events.Transfer.createFilter(fromBlock=29328724, toBlock=29328724).get_all_entries()
event_list = []
for event in events:
    event_list.append(json.loads(web3.toJSON(event)))
print(event_list)

