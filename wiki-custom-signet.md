# Signet Personalizada #

Una red signet personalizada en Bitcoin es una red de prueba privada que se utiliza para desarrollar y probar nuevas funciones de Bitcoin antes de implementarlas en mainnet`. 

Las redes signet son similares a la red principal de Bitcoin, pero están separadas y no están conectadas a ella. Esto permite a los desarrolladores probar nuevos cambios sin afectar la red principal y sin riesgo de perder fondos.

**Las redes signet personalizadas se pueden crear con diferentes parámetros que mainnet, lo que permite a los desarrolladores probar cómo funcionarían los cambios en diferentes escenarios.** Por ejemplo, una red signet personalizada podría tener un límite de bloque más pequeño o una tasa de emisión de bitcoins diferente.

**Las redes signet personalizadas son una herramienta valiosa para el desarrollo de Bitcoin y se utilizan para probar una amplia gama de nuevas funciones, que incluyen:**

* **Nuevas firmas y scripts:** Las firmas personalizadas y los scripts son un tipo de código que se puede usar para crear transacciones de Bitcoin más complejas y flexibles. Las redes signet se pueden usar para probar estos nuevos tipos de firmas y scripts antes de implementarlos en la red principal.
* **Cambios en las reglas de consenso:** Las reglas de consenso son las reglas que rigen el funcionamiento de la red Bitcoin. Las redes signet se pueden usar para probar cambios en las reglas de consenso, como un nuevo algoritmo de minería o un tamaño de bloque diferente.
* **Nuevas aplicaciones:** Las redes signet se pueden usar para probar nuevas aplicaciones que se basan en Bitcoin, como mercados descentralizados o sistemas de votación.

**El uso de redes signet personalizadas ayuda a garantizar que los nuevos cambios de Bitcoin sean seguros y confiables antes de implementarlos en la red principal.** Esto ayuda a proteger la red Bitcoin y a mantenerla segura y estable.

**Aquí hay algunos beneficios adicionales de usar redes signet personalizadas:**

* **Permitir la colaboración entre desarrolladores:** Las redes signet personalizadas permiten que los desarrolladores colaboren en nuevos proyectos sin afectar la red principal.
* **Acelerar el desarrollo:** Las redes signet personalizadas permiten a los desarrolladores probar nuevos cambios más rápidamente que si tuvieran que hacerlo en la red principal.
* **Reducir el riesgo:** Las redes signet personalizadas permiten a los desarrolladores probar nuevos cambios sin riesgo de perder fondos.

**En general, las redes signet personalizadas son una herramienta valiosa para el desarrollo de Bitcoin y desempeñan un papel importante en la creación de nuevas funciones y aplicaciones seguras y confiables.**

Para crea nuestra propia signet personaliza, debemos tener en cuenta varios de pasos: 
- generar las claves utilizadas para firmar, 
- definir el script de bloque, 
- iniciar un nodo que se ejecute en la nueva signet e 
- importar la clave privada para firmar bloques.


## Generar claves utilizadas para firmar un bloque

La forma más sencilla es simplemente iniciar un nodo de prueba de regtest y para luego generar una nueva clave desde allí.

```
$ cd PATHTOBITCOIN/bitcoin/src

$ ./bitcoind -datadir=/home/ifuensan/signet_files/datadir2/ -regtest -daemon
./bitcoind -datadir=/home/ifuensan/signet_files/datadir2/ -regtest -daemon -deprecatedrpc=create_bdb

$ alias btsig = "./bitcoin-cli -datadir=/home/ifuensan/signet_files/datadir2/ -regtest"
$ btsig -named createwallet wallet_name=wallet_test descriptors=false
$ ADDR=$(btsig getnewaddress)
$ PRIVKEY=$(btsig dumpprivkey $ADDR)
$ btsig getaddressinfo $ADDR | grep pubkey
  "pubkey": "THE_REAL_PUBKEY",
```
Necesitamos anotar la clave privada (`echo $PRIVKEY`) y la clave pública (aquí `THE_REAL_PUBKEY`).

```
➜  src git:(d287a8c) ✗ btsig getaddressinfo $ADDR | grep pubkey
  "pubkey": "028c9959fecef8e837c5a8bf55ea1801436d514a4109ef581b581ad811b327a23f",
➜  src git:(d287a8c) ✗ echo $PRIVKEY
cQLdPSz8bMNncSdoWWwhDzBmninpJ6zmJf8NiEK2gU1RfGWy4a4f
```


## Definiendo el script de bloque 

El script de bloque es como cualquier script antiguo de Bitcoin, pero el tipo más común es un multifirma k-of-n. 
Aquí haremos una multisig 1-de-1 con nuestra única clave pública anterior. Nuestro script se convierte

* `51` '1' (recuento de firmas)
* `21` Push 0x21=33 bytes (la longitud de nuestra clave pública anterior)
* `THE_REAL_PUBKEY` (nuestra clave pública)
* `51` '1' (recuento de claves públicas)
* `ae` `OP_CHECKMULTISIG` opcode

Juntos, nuestro valor de `-signetchallenge` se convierte en `5121...51ae`. Donde `...` representa `THE_REAL_PUBKEY` (ver arriba).

5121028c9959fecef8e837c5a8bf55ea1801436d514a4109ef581b581ad811b327a23f51ae

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
➜  src git:(d287a8c) ✗ ../contrib/signet/miner --cli="./bitcoin-cli" calibrate --grind-cmd="./bitcoin-util grind" --seconds=50
nbits=1d3b96b6 for 50s average mining time

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

https://github.com/bitcoin/bitcoin/pull/19937


