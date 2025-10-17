import React, { useEffect, useRef, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function App() {
  const [connected, setConnected] = useState(false);
  const socket = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Substitua pelo IP do ESP32 mostrado no serial monitor
    socket.current = new WebSocket('ws://192.168.1.16/ws');

    socket.current.onopen = () => {
      setConnected(true);
      console.log("Conectado ao ESP32");
    };

    socket.current.onclose = () => {
      setConnected(false);
      console.log("Desconectado do ESP32");
    };

    socket.current.onerror = (e) => {
      console.log("Erro de conexão", e.message);
    };

    return () => {
      socket.current?.close();
    };
  }, []);

  const enviarComando = (mensagem: string) => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      socket.current.send(mensagem);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.status}>Status: {connected ? "Conectado" : "Desconectado"}</Text>

      <TouchableOpacity
        style={styles.botao}
        onPress={() => enviarComando("ligar_led")}
        disabled={!connected}
      >
        <Text style={styles.textoBotao}>Botão</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#161b21',
    alignItems: 'center',
    justifyContent: 'center',
  },
  status: {
    color: '#fff',
    fontSize: 20,
    marginBottom: 20,
  },
  botao: {
    backgroundColor: '#007bff',
    padding: 15,
    borderRadius: 10,
  },
  textoBotao: {
    color: '#fff',
    fontSize: 18,
  },
});
