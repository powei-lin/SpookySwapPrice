import random
from time import time
from web3 import Web3, HTTPProvider
import json
from tqdm import tqdm
from random import shuffle

from spooky_swap import Spookyswap
import util
import time


def main():
    ftm_rpc = 'https://rpcapi.fantom.network/'
    ftmscan_token = 'https://ftmscan.com/token/'
    ftm = Web3(Web3.HTTPProvider(ftm_rpc))

    # chech if fantom network is connected
    print(ftm.isConnected())

    # show latest block number
    block_num = ftm.eth.block_number

    top_tokens = util.load_json('top_tokens.json')
    wFTM = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
    top_tokens.pop(wFTM)

    spooky_swap = Spookyswap(ftm)
    spooky_swap_factory = spooky_swap.factory_contract()
    spooky_swap_router = spooky_swap.router_contract()

    all_pairs_length = spooky_swap_factory.functions.allPairsLength().call()
    print(all_pairs_length)

    keys = list(top_tokens.keys())
    shuffle(keys)

    prev_price = 0.0

    while (True):
        if (block_num == ftm.eth.block_number):
            time.sleep(0.1)
            continue
        block_num = ftm.eth.block_number

        token0 = keys[0]
        token0 = '0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e'
        token1 = keys[1]
        token0_name = top_tokens[token0]
        token1_name = top_tokens[token1]

        wFTM_amount_Wei = Web3.toWei(1, 'ether')
        token0_amount_Wei = spooky_swap_router.functions.getAmountsOut(
            wFTM_amount_Wei, (wFTM, token0)).call()[1]
        # token1_amount_Wei = spooky_swap_router.functions.getAmountsOut(token0_amount_Wei, (token0, token1)).call()[1]
        wFTM_back_amount_Wei = spooky_swap_router.functions.getAmountsOut(
            token0_amount_Wei, (token0, wFTM)).call()[1]
        price = Web3.fromWei(wFTM_back_amount_Wei, 'ether')
        if (prev_price != price):
            print(price)
            print("{} -> {} -> {}".format("wFTM", token0_name, "wFTM"))
            prev_price = price
            shuffle(keys)

    # for i in range(100, 200):
    #     coin_pair_address = spooky_swap_factory.functions.allPairs(i).call()
    #     pair_contract_abi = spooky_swap.pair_contract_abi()

    #     pair_contract = ftm.eth.contract(coin_pair_address, abi=pair_contract_abi)
    #     reserves = pair_contract.functions.getReserves().call()
    #     if(reserves[0] == 0):
    #         continue

    #     token0_address = pair_contract.functions.token0().call()
    #     token1_address = pair_contract.functions.token1().call()
    #     print(token0_address, token1_address)

    #     # get token name
    #     token0_name, token1_name = "", ""
    #     if(token0_address in token_dictionary):
    #         token0_name = token_dictionary[token0_address]
    #     else:
    #         token0_name = util.get_toekn_name(ftmscan_token, token0_address)
    #         token_dictionary[token0_address] = token0_name

    #     if(token1_address in token_dictionary):
    #         token1_name = token_dictionary[token1_address]
    #     else:
    #         token1_name = util.get_toekn_name(ftmscan_token, token1_address)
    #         token_dictionary[token1_address] = token1_name

    #     print("{}_{}".format(token0_name, token1_name))
    #     print(reserves)
    #     print()
    # with open("coin_pair.json", 'w') as ofile:
    #   json.dump(token_dictionary, ofile, indent=2)


if __name__ == '__main__':
    main()
