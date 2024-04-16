# Signet Personalizada #

Crear su propia signet implica un par de pasos: generar las claves utilizadas para firmar, definir el script de bloque, iniciar un nodo que se ejecute en la nueva signet e importar la clave privada para firmar bloques.

## Generar claves utilizadas para firmar un bloque ##
La forma más sencilla es simplemente iniciar un nodo de prueba de regtest y para luego generar una nueva clave desde allí.

```
$ cd PATHTOBITCOIN/bitcoin/src
$ ./bitcoind -regtest -daemon -wallet="test"
$ ADDR=$(./bitcoin-cli -regtest getnewaddress)
$ PRIVKEY=$(./bitcoin-cli -regtest dumpprivkey $ADDR)
$ ./bitcoin-cli -regtest getaddressinfo $ADDR | grep pubkey
  "pubkey": "THE_REAL_PUBKEY",
```
Necesitamos anotar la clave privada (`echo $PRIVKEY`) y la clave pública (aquí `THE_REAL_PUBKEY`).

## Definiendo el script de bloque ##
El script de bloque es como cualquier script antiguo de Bitcoin, pero el tipo más común es un multifirma k-of-n. 
Aquí haremos una multisig 1-de-1 con nuestra única clave pública anterior. Nuestro script se convierte

* `51` '1' (recuento de firmas)
* `21` Push 0x21=33 bytes (la longitud de nuestra clave pública anterior)
* `THE_REAL_PUBKEY` (nuestra clave pública)
* `51` '1' (recuento de claves públicas)
* `ae` `OP_CHECKMULTISIG` opcode

Juntos, nuestro valor de `-signetchallenge` se convierte en `5121...51ae`. Donde `...` representa `THE_REAL_PUBKEY` (ver arriba).

## Iniciar un nodo (emisor) ##
Para que la red sea útil, debe generar bloques a intervalos decentes, así que iniciemos un nodo que haga eso (puede ser útil usar ese nodo también como nodo semilla para otros pares).

Tenga en cuenta que estamos importando `$PRIVKEY` al final; cualquier nodo que necesite emitir bloques debe importar la clave privada que generamos anteriormente, o no podrá firmar bloques.

```
$ ./bitcoin-cli -regtest stop
$ datadir=$HOME/signet-custom
$ mkdir $datadir
$ echo "signet=1
[signet]
daemon=1
signetchallenge=5121...51ae # fill in THE_REAL_PUBKEY" > $datadir/bitcoin.conf
$ ./bitcoind -datadir=$datadir -wallet="test"
$ ./bitcoin-cli -datadir=$datadir importprivkey $PRIVKEY
```

Nota: si se encuentra con los errores anteriores, es posible que tenga un sello diferente ejecutándose, lo que está bloqueando los puertos. Detenga esto o configure el puerto y rpcport en el archivo `$datadir/bitcoin.conf` en la sección `[signet]` e intente nuevamente desde la parte `bitcoind` anterior.

## Ejecutar el emisor ##
Por último, vamos a poner en funcionamiento un emisor para extraer bloques.

Necesitaremos proporcionar un valor para nbits que sea el objetivo de minería y que sea inversamente proporcional a la dificultad. Esto nos permitirá establecer el tiempo promedio entre bloques minados.

Podemos usar el comando `calibrate` para que nos dé los nbits para un tiempo promedio de minado de 10 min (600 s):
```
$ ../contrib/signet/miner --cli="./bitcoin-cli" calibrate --grind-cmd="./bitcoin-util grind" --seconds=600
```

Haciendo referencia a nuestro valor de nbits con la variable $NBITS, debemos especificar --set-block-time al extraer el primer bloque en un nuevo sello:
```
$ ADDR=$(./bitcoin-cli -datadir=$datadir getnewaddress); ../contrib/signet/miner --cli="./bitcoin-cli -datadir=$datadir" generate --address $ADDR --grind-cmd="./bitcoin-util grind" --nbits=$NBITS --set-block-time=$(date +%s)
```

Esto creará una dirección y luego extraerá el primer bloque a esa dirección. (Tenga en cuenta que es posible que primero deba crear una billetera).
Para mantener la minería en curso desde allí, con el objetivo de que los bloques lleguen cada 10 minutos en promedio, podemos ejecutar:
```
$ ../contrib/signet/miner --cli="./bitcoin-cli -datadir=$datadir" generate --address $ADDR --grind-cmd="./bitcoin-util grind" --nbits=$NBITS --ongoing
```
Lo siguiente es hacer que sus amigos/colegas/etc. se unan a la red configurando el desafío signet igual que el anterior y conectándose a su nodo.

## Script de ejemplo ##
Puede encontrar un script de ejemplo completo en https://en.bitcoin.it/wiki/Signet:Custom:Script




