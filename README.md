# Setup My Own Signet

### From Chain Code Labs, [Signet Wallet Project](https://github.com/chaincodelabs/signet-wallet-project) ###

The included script signet-setup.py needs to be run by the administrator on a publicly reachable server to start the game.

The script requires a local installation of Bitcoin Core since it consumes the test framework as a library.

Usage: `python signet-setup.py <path/to/bitcoin> <path/to/student/files> <path/for/bitcoin/datadir>`

`<path/to/bitcoin>`: (required) Path to local installation of Bitcoin Core repository

`<path/to/student/files>`: (optional, default ./config) Destination for student bitcoin.conf and wallet descriptors

`<path/for/bitcoin/datadir>`: (optional, default is `os.tmpdir()`) Data directory for the signet full node

The script runs the signet full node, creates all the wallets and continues mining blocks forever. It should never be killed, but the node can always be restarted by using `-datadir=<path/for/bitcoin/datadir>`


## Setup Multiple RPC Users in Bictoin Core ##

In Bitcoin Core, you can set up multiple JSON-RPC users with different permissions and access levels. This feature allows you to control who can access the JSON-RPC interface and perform various actions like sending transactions, querying information about the blockchain, and more.

To set up multiple JSON-RPC users, you need to modify the bitcoin.conf configuration file, which is typically located in the Bitcoin data directory. Each JSON-RPC user is defined with a username and password, along with optional permissions.

Here's an example of how you can configure multiple JSON-RPC users in the bitcoin.conf file:

```
rpcuser=user1
rpcpassword=password1
rpcallowip=127.0.0.1
rpcport=8332

rpcuser=user2
rpcpassword=password2
rpcallowip=192.168.0.1/24
rpcport=8333
```
In this example, two JSON-RPC users are defined:

* User 1 with username user1 and password password1. This user is allowed to access the JSON-RPC interface only from the local machine (127.0.0.1) and uses the default RPC port 8332.

* User 2 with username user2 and password password2. This user is allowed to access the JSON-RPC interface from the local network (192.168.0.1/24) and uses a custom RPC port 8333.

You can add as many JSON-RPC users as needed by repeating the rpcuser, rpcpassword, rpcallowip, and rpcport lines in the bitcoin.conf file.

It's important to note that when using JSON-RPC over HTTP, you should ensure secure communication, such as using HTTPS and implementing proper authentication mechanisms, especially if exposing the JSON-RPC interface to the internet. Additionally, ensure that you choose strong passwords for each user to enhance security.

You can user that python program for generate the encoded password [rpcauth.py](https://github.com/bitcoin/bitcoin/blob/master/share/rpcauth/rpcauth.py) or that web page [Bitcoin Core RPC Auth Config Generator](https://jlopp.github.io/bitcoin-core-rpc-auth-generator/)
