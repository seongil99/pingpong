window.onlineSocket = null;

function connect() {
  if (
    window.onlineSocket &&
    window.onlineSocket.readyState === WebSocket.OPEN
  ) {
    return;
  }
  const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const host = window.location.host;
  window.onlineSocket = new WebSocket(`${protocol}${host}/api/online-status/`);
  let retryDelay = 5000; // Start with 5 seconds
  window.onlineSocket.onopen = () => {
    console.log("Connected");

    // Send heartbeat every 5 seconds
    setInterval(() => {
      if (window.onlineSocket.readyState === WebSocket.OPEN) {
        window.onlineSocket.send(JSON.stringify({ type: "heartbeat" }));
        console.log("Heartbeat sent");
      }
    }, 5000);
  };

  window.onlineSocket.onclose = () => {
    console.log("Disconnected. Retrying...");
    setTimeout(() => {
      connect();
    }, retryDelay);
    retryDelay = Math.min(30000, retryDelay * 1.5); // Exponential backoff capped at 30 seconds
  };

  window.onlineSocket.onerror = (error) => {
    console.error("WebSocket error:", error);
    if (window.onlineSocket.readyState === WebSocket.OPEN) {
      window.onlineSocket.close();
    }
  };

  // Close the WebSocket when the tab is hidden
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      console.log("Tab hidden, closing WebSocket...");
      window.onlineSocket.close();
    } else if (window.onlineSocket.readyState === WebSocket.CLOSED) {
      console.log("Tab visible, reconnecting WebSocket...");
      connect();
    }
  });
}

connect();
