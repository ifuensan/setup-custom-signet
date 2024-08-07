# Configurar una Signet Personalizada

Me he basado en todo lo visto en el ejercicio [Signet Wallet Project](https://github.com/chaincodelabs/signet-wallet-project) de  ChainCode Labs.

## Guía de uso de ChainCode Traducida ##

El administrador debe ejecutar el Script signet-setup.py incluido en un servidor públicamente accesible para iniciar el juego.

El script requiere una instalación local de Bitcoin Core, ya que consume el framework de tests como una biblioteca.

Utilice: `python signet-setup.py <path/to/bitcoin> <path/to/student/files> <path/for/bitcoin/datadir>`

`<path/to/bitcoin>`: (requerido) Ruta hacia la instalación local del repositorio de Bitcoin Core.

`<path/to/student/files>`: (opcional, por defecto ./config) Destino para el bitcoin.conf del estudiante y descriptores de billeteras.

`<path/for/bitcoin/datadir>`: (opcional, por defecto es `os.tmpdir()`) Directorio de datos para el nodo completo de Signet.

El script ejecuta el nodo completo de Signet, crea todas las billeteras y continúa minando bloques para siempre. Nunca debe ser matado el proceso, pero el nodo siempre se puede reiniciar usando `-datadir=<path/for/bitcoin/datadir>`


## Ampliaciones ##

`python3 signet-setup.py ~/bitcoin/ ~/signet_files/students/ ~/signet_files/datadir/`

# Lanzar el script  
```bash
python3 signet-setup.py /Work/bitcoin/ /home/ifuensan/signet_files/students/ /home/ifuensan/signet_files/datadir/
```
### Parar el nodo
/Work/bitcoin/src/bitcoin-cli -datadir=/home/ifuensan/signet_files/datadir/node0 stop

### Arrancar el nodo
```bash
/Work/bitcoin/src/bitcoind \
    -datadir=/home/ifuensan/signet_files/datadir/node0 \
    -logtimemicros \
    -debug \
    -debugexclude=libevent \
    -debugexclude=leveldb \
    -debugexclude=rand \
    -uacomment=testnode0 \
    -logthreadnames \
    -logsourcelocations \
    -loglevel=trace \
    -v2transport=0 \
    -bind=0.0.0.0 \
    -txindex

    -signetchallenge=0013f21b6165d87eb5a9355ef1561590a4691e2501b9 \

```
### Arrancar el miner
```bash
/usr/bin/python3 /Work/bitcoin/contrib/signet/miner --cli=/Work/bitcoin/src/bitcoin-cli -datadir=/home/ifuensan/signet_files/datadir/node0 -rpcwallet=miner generate --address=tb1q7gdkzewc0666jd2779tpty9ydy0z2qdeydnf08 --grind-cmd=/Work/bitcoin/src/bitcoin-util grind --min-nbits --ongoing
```
Un ejemplo de configuración:
```
signet=1
[signet]
port=13383
rpcport=18383
rpcservertimeout=99000
rpcdoccheck=1
fallbackfee=0.0002
server=1
txindex=1
rpcuser=mempool
rpcpassword=mempool
keypool=1
discover=0
dnsseed=0
fixedseeds=0
listenonion=0
peertimeout=999999999
printtoconsole=0
upnp=0
natpmp=0
shrinkdebugfile=0
deprecatedrpc=create_bdb
unsafesqlitesync=1
connect=0
bind=127.0.0.1
signetchallenge=0014f21b6165d87eb5a9355ef1561590a4691e2501b9
```
