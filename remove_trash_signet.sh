#!/bin/bash
killall -9 bitcoind
killall -9 python3
rm -rf /tmp/bitcoin_func_test_*
rm -rf ~/signet_files/datadir
rm -rf ~/signet_files/config
