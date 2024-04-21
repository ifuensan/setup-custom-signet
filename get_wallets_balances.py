import subprocess
import sys
import os

def get_wallet_balances(datadir, num_wallets):
    # Comando para obtener el saldo de una billetera
    command_template = "bitcoin-cli -datadir={} -rpcwallet={} getbalance"

    # Nombre del archivo de salida
    output_file = "wallet_balances.txt"

    # Obtener la ruta completa del archivo de salida
    output_file_path = os.path.join(os.getcwd(), output_file)

    # Intentar obtener los saldos de las billeteras y escribirlos en el archivo de salida
    try:
        # Abrir el archivo de salida en modo escritura
        with open(output_file_path, 'w') as f:
            # Ejecutar el comando para cada billetera y escribir el nombre de la billetera y su saldo en el archivo
            for i in range(num_wallets):
                wallet = f"wallet_{i:03d}"
                command = command_template.format(datadir, wallet)
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                balance = result.stdout.strip() if result.returncode == 0 else "Error"
                f.write(f"{wallet} {balance}\n")
        
        # Imprimir un mensaje de éxito si se generó el archivo de salida correctamente
        print(f"Archivo de salida '{output_file_path}' generado correctamente.")

    except Exception as e:
        # Imprimir un mensaje de error si hubo algún problema durante el proceso
        print(f"Se produjo un error al generar el archivo de salida: {str(e)}")

if __name__ == "__main__":
    # Verificar si se proporcionan los argumentos adecuados
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <num_wallets> [datadir]")
        sys.exit(1)

    # Obtener el número total de billeteras
    num_wallets = int(sys.argv[1])

    # Obtener el directorio de datos (si se proporciona, de lo contrario, usar el predeterminado)
    if len(sys.argv) == 3:
        datadir = sys.argv[2]
    else:
        datadir = "~/signet_files/config"

    # Expandir el directorio de datos
    datadir = os.path.expanduser(datadir)

    # Llamar a la función para obtener los saldos de las billeteras y escribirlos en el archivo de salida
    get_wallet_balances(datadir, num_wallets)

