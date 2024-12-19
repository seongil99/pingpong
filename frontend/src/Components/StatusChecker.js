function connect() {
  const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const host = window.location.host;
  const socket = new WebSocket(`${protocol}${host}/api/online-status/`);
  let retryDelay = 5 * 1000;

  socket.onopen = () => {
    console.log("Connected");
    setInterval(() => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "heartbeat" }));
        console.log("Heartbeat sent");
      }
    }, 30000); // Send heartbeat every 5 seconds
  };

  socket.onclose = () => {
    console.log("Disconnected. Retrying...");
    setTimeout(connect, retryDelay);
    retryDelay = Math.min(30000, retryDelay * 2);
  };

  socket.onerror = (error) => {
    console.error("WS error:", error);
    socket.close();
  };
}
connect();
