import socket

def decimal_to_hexadecimal(decimal_num: int) -> str:
    return format(decimal_num, '04X')

def main():
    # Configuración del servidor
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 4080

    # Crear un socket TCP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar al servidor
    cliente_socket.connect((SERVER_IP, SERVER_PORT))

    while True:
        try:
            # Solicitar al usuario el código del equipo en decimal
            codigo_equipo_decimal = int(input("Ingrese el código del equipo en decimal: "))

            # Verificar que el código del equipo sea un número decimal válido
            if codigo_equipo_decimal < 0:
                print("El código del equipo debe ser un número decimal positivo.")
                continue

            codigo_equipo_hexadecimal = decimal_to_hexadecimal(codigo_equipo_decimal)

            # Solicitar al usuario el estado del equipo
            status = input("¿El equipo está conectado? (1 para conectado, 0 para desconectado, D para eliminar): ")


            if status not in ('0', '1', 'D'):
                print("Entrada no válida para el estado del equipo.")
                continue

            # Crear el mensaje en el formato correcto
            message = f"<[{codigo_equipo_hexadecimal}{status}]>"
            print(f"Mensaje enviado: {message}")

            # Enviar el mensaje al servidor
            cliente_socket.sendall(message.encode())

            # Recibir respuesta del servidor
            response = cliente_socket.recv(1024).decode()
            print(f"Respuesta del servidor: {response}")

            # Cerrar la conexión
            cliente_socket.close()
            break

        except ValueError:
            print("Entrada no válida. Debe ingresar un número decimal para el código del equipo.")

if __name__ == "__main__":
    main()