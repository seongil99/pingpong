let isReconnecting = false;

function connect() {
  if (isReconnecting) return;
  isReconnecting = true;

  const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const host = window.location.host;
  const socket = new WebSocket(`${protocol}${host}/api/online-status/`);
  let retryDelay = 5000; // Start with 5 seconds

  socket.onopen = () => {
    console.log("Connected");
    isReconnecting = false;

    // Send heartbeat every 5 seconds
    setInterval(() => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "heartbeat" }));
        console.log("Heartbeat sent");
      }
    }, 5000);
  };

  socket.onclose = () => {
    console.log("Disconnected. Retrying...");
    isReconnecting = true;
    setTimeout(() => {
      isReconnecting = false;
      connect();
    }, retryDelay);
    retryDelay = Math.min(30000, retryDelay * 1.5); // Exponential backoff capped at 30 seconds
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    if (socket.readyState === WebSocket.OPEN) {
      socket.close();
    }
  };

  // Close the WebSocket when the tab is hidden
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      console.log("Tab hidden, closing WebSocket...");
      socket.close();
    } else if (socket.readyState === WebSocket.CLOSED) {
      console.log("Tab visible, reconnecting WebSocket...");
      connect();
    }
  });
}

connect();
