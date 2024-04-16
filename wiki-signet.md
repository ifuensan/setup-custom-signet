# Signet #
Signet (BIP 0325) es una nueva red de prueba para Bitcoin que agrega un requisito de firma adicional para bloquear la validación.
Signet es de naturaleza similar a testnet, pero más confiable y controlado centralmente.
Existe una red Signet predeterminada ('Signet Global Test Net VI' al momento de escribir este artículo), pero cualquiera puede ejecutar su propia red Signet a su antojo.

Ejecute bitcoind con el indicador ~-signet~ para usar la signet por defecto (o coloque signet=1 en el archivo bitcoin.conf).
Si desea utilizar una signet personalizada, debe proporcionar el desafío de bloque (también conocido como script de bloque) usando -signetchallenge=<hex>.
y preferiblemente también al menos un nodo semilla usando -signetseednode=<host>[:<port>].
