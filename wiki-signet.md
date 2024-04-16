# Signet #

Signet ([BIP 0325](https://en.bitcoin.it/wiki/BIP_0325)) es una nueva red de prueba para Bitcoin que agrega un requisito de firma adicional para bloquear la validación.
Signet es de naturaleza similar a testnet, pero más confiable y controlado centralmente.
Existe una red Signet predeterminada ('Signet Global Test Net VI' al momento de escribir este artículo), pero cualquiera puede ejecutar su propia red Signet a su antojo.

Ejecute bitcoind con el indicador `-signet` para usar la signet por defecto (o coloque signet=1 en el archivo bitcoin.conf).
Si desea utilizar una signet personalizada, debe proporcionar el desafío de bloque (también conocido como script de bloque) usando `-signetchallenge=<hex>`.
y preferiblemente también al menos un nodo semilla usando `-signetseednode=<host>[:<port>]`.


## Diferencias ##
* El puerto de escucha predeterminado del protocolo de red Bitcoin es 38333 (en lugar de 8333)
* El puerto de conexión RPC predeterminado es 38332 (en lugar de 8332)
* Un valor diferente del campo ADDRESSVERSION garantiza que ninguna dirección Signet de Bitcoin funcionará en la red de producción. (`0x6F` en lugar de `0x00`)
* Los bytes del encabezado del mensaje de protocolo se *generan dinámicamente* según el desafío del bloque, es decir, cada sello es diferente; el encabezado del sello predeterminado actual es `0x0A03CF40` (que se invierte, por ejemplo, en las variables de Rust) (en lugar de `0xF9BEB4D9`), pero consulte #Genesis_Block_and_Message_Header
* El bloque Génesis tiene marca de tiempo 1598918400, nonce 52613770 y dificultad 0x1e0377ae.
* Segwit siempre está habilitado
* Requisito de consenso adicional de que el compromiso testigo de coinbase contenga un compromiso de signet extendido, que es un script que satisface el script de bloque (generalmente un multifirma k-of-n)

## ¿Por qué ejecutar Signet? ## 
* Usted es un instructor y desea ejecutar un entorno de red Bitcoin controlado con fines de enseñanza.
* Eres un desarrollador de software y quieres probar tu software.
* Quiere probar cambios experimentales que desea implementar en Bitcoin.
* Quiere probar software en ejecución a largo plazo y no quiere lidiar con decenas de miles de reorganizaciones de bloques, o días sin que se extraigan bloques, como es el caso de Testnet.
* Quiere una manera fácil de probar el doble gastos (Signet planea incluir soporte para el doble gasto automatizado, donde usted proporciona dos transacciones en conflicto y se extraen en orden, con una reorganización entre ellas).


## Bloque Génesis y encabezado de mensaje ##
Todas las redes Signet comparten el mismo bloque génesis, pero tienen un encabezado de mensaje diferente. El encabezado del mensaje son los 4 primeros bytes del sha256d-hash del desafío del bloque (challenge), como una única operación de inserción de script. Es decir, si el desafío del bloque es de 37 bytes, el inicio del mensaje sería `sha256d(0x25 || challenge)[0..3]`.

## Empezando ##
NOTA: signet (VI) se fusionó con la rama maestra de Bitcoin Core a partir de [BIP-325: Signet [consensus] #18267](https://github.com/bitcoin/bitcoin/pull/18267)

### Obtener y compilar signet ###
```
$ git clone https://github.com/bitcoin/bitcoin
$ cd bitcoin
$ ./autogen.sh
$ ./configure
$ make -j5
```

### Cree el archivo bitcoin.conf e inicie el demonio ###
```
$ cd src
$ mkdir signet
$ echo "signet=1
daemon=1" > signet/bitcoin.conf
$ ./bitcoind -datadir=signet
```

### Verifica que estás conectado ###
```
$ ./bitcoin-cli -datadir=signet getconnectioncount
***SHOULD BE MORE THAN ZERO***
$ ./bitcoin-cli -datadir=signet getblockcount
***SHOULD BE MORE THAN ZERO***
```

### Consigue algunas monedas ###
Existe una herramienta de línea de comandos que puede utilizar para enviar monedas directamente a su instancia de Signet, suponiendo que se encuentre en la red predeterminada. También puedes usar el faucet en línea con una dirección tuya.

#### Usando faucet en línea ####
Primero necesitas una dirección
```
$ ./bitcoin-cli -datadir=signet getnewaddress
```
Luego ve a un grifo (faucet), p. https://signet.bc-2.jp e introduce tú dirección.

#### Usando la herramienta de línea de comando ####
La herramienta está en `contrib/signet` y se llama `getcoins.sh`. Opcionalmente, puede proporcionar una ruta a bitcoin-cli usando `--cmd=[ruta]` y un grifo compatible usando `--faucet=[url]` seguido de cualquier número de argumentos para `bitcoin-cli`. El script intenta detectarlos automáticamente si se omiten.
```
$ cd ../contrib/signet
$ ./getcoins.sh -datadir=../../src/signet
Payment of 10.00000000 BTC sent with txid c0bfa...
```

#### Comprueba que recibiste las monedas ####
Verifique la transacción de su faucet confirmando, por ej. https://explorer.bc-2.jp y luego envíe monedas a personas y/o use signet para probar su billetera, etc.

Puede ver inmediatamente la cantidad usando `getunconfirmedbalance`, es decir.
```
$ cd ../../src # if you were in contrib/signet
$ ./bitcoin-cli -datadir=signet getunconfirmedbalance
```

También puedes ver información sobre la transacción que te dio el faucet.
```
$ ./bitcoin-cli -datadir=signet gettransaction THETXID
```

Una vez que se haya confirmado, deberías verlo en getbalance.
```
$ ./bitcoin-cli -datadir=signet getbalance
```

## Links Externos ##
[BIP 0325](https://en.bitcoin.it/wiki/BIP_0325)

### Grifos ###
* https://signetfaucet.com/
* ~https://alt.signetfaucet.com (the same here)~

Faucet source code, if you want your own:
* https://github.com/stepansnigirev/tinyfaucet.git (python)
* https://github.com/jsarenik/bitcoin-faucet-shell (POSIX shell)

### Exploradores de bloques ###
* https://explorer.bc-2.jp/
* https://mempool.space/signet
* ~https://ex.signet.bublina.eu.org~


----
Traducción de https://en.bitcoin.it/wiki/Signet por @ifuensan

