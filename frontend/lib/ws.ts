const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

export class AgentWebSocketClient {
  private socket: WebSocket | null = null;
  private onMessageCallback: ((data: any) => void) | null = null;

  connect(onMessage: (data: any) => void) {
    this.onMessageCallback = onMessage;
    this.socket = new WebSocket(`${WS_BASE_URL}/ws/agents`);

    this.socket.onopen = () => {
      console.log('⚡ Connected to AdsIQ Agent WebSocket Stream');
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (this.onMessageCallback) {
          this.onMessageCallback(data);
        }
      } catch (err) {
        console.error('Error parsing WS message:', err);
      }
    };

    this.socket.onclose = () => {
      console.log('🔌 WebSocket Stream Closed');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  send(data: any) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
