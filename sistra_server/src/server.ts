import { createServer, Socket } from 'net';

const PORT = 4080;

// Registro de equipos y sus estados
const equipoRegistrado: Record<string, string> = {};

const hexToDecimal = (hex: string): number => {
  return parseInt(hex, 16);
};

const MensajeCliente = (message: string, socket: Socket): void => {
  console.log(`Mensaje recibido: ${message}`);
  const match = message.match(/<\[([0-9a-fA-F]{4})([01D])\]>/);
  if (!match) {
    socket.write("Formato de mensaje inválido");
    return;
  }

  const [, codigoEquipo, status] = match;

  // Convertir el código del equipo a decimal y mostrarlo
  const decimalCode = hexToDecimal(codigoEquipo);
  let estado = ''

  if (status === 'D') {
    delete equipoRegistrado[codigoEquipo];
    estado = 'eliminado'
  } else if(status === '1') {
      estado = "conectado"
  } else {
    estado = "desconectado"
  }
  socket.write(`Equipo ${decimalCode} ${estado}`)
  // if ( status == '1') return;
  equipoRegistrado[codigoEquipo] = status;
};

const server = createServer((socket: Socket) => {
  console.log('Cliente conectado');
  let dataBuffer = "";

  socket.on('data', (data: Buffer) => {
    // Acumula los datos en un buffer hasta que el cliente se desconecte
    dataBuffer += data.toString();
    console.log('Datos recibidos: ', dataBuffer);
    MensajeCliente(dataBuffer, socket);
  });

  socket.on('end', () => {
    console.log('Cliente desconectado');
  });
});

server.listen(PORT, () => {
  console.log(`Servidor escuchando en el puerto ${PORT}`);
});