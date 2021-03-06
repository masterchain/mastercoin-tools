#######################################################
#                                                     #
#  Copyright Masterchain Grazcoin Grimentz 2013-2014  #
#  https://github.com/masterchain/masterchain-world   #
#  https://masterchain.info                           #
#  masterchain@@bitmessage.ch                         #
#  https://masterchain.info/LICENSE.txt               #
#                                                     #
#######################################################

import urlparse
import os, sys
from msc_apps import *

def validateaddr_response(response_dict):
    info(response_dict)
    try:
        response_dict['addr']
    except KeyError:
        return (None, 'No address in dictionary')
        
    if len(response_dict['addr'])!=1:
        return response(None, 'No single address')

    addr=get_response_field(response_dict, 'addr')
    
    # now verify
    l=len(addr)
    if l == 66 or l == 130: # probably pubkey
        if is_pubkey_valid(addr):
            debug='valid pubkey'
            response_status='OK'
        else:
            debug='invalid pubkey'
            response_status='invalid pubkey'
    else:   
        if not is_valid_bitcoin_address(addr):
            debug='invalid address'
            response_status='invalid address'
        else:
            addr_pubkey=get_pubkey(addr)
            if is_pubkey_valid(addr_pubkey):
                debug='valid address'
                response_status='OK'
            else:
                debug='missing pubkey'
                response_status='missing pubkey'

    if response_status != 'OK':
        info(response_status)
        return(None, response_status)

    response='{"status":"'+response_status+'", "debug":"'+debug+'"}'
    return (response, None)

def validateaddr_handler(environ, start_response):
    return general_handler(environ, start_response, validateaddr_response)
