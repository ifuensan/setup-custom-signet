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
