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
