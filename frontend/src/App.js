import { useEffect, useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);

  const backendUrl = process.env.REACT_APP_API_URL || "http://localhost:8000";

  useEffect(() => {
    const eventSource = new EventSource(`${backendUrl}/events`);
    eventSource.onmessage = (e) => {
      setMessages((prev) => [...prev, e.data]);
    };
    return () => eventSource.close();
  }, []);

  const sendCommand = async (endpoint) => {
    await fetch(`${backendUrl}/${endpoint}`, { method: "POST" });
  };

  return (
    <div>
      <h1>Live Updates</h1>
      <button onClick={() => sendCommand("stop_pull")}>Stop Pull</button>
      <button onClick={() => sendCommand("resume_pull")}>Resume Pull</button>

      <ul>
        {messages.map((msg, i) => (
          <li key={i}>{msg}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
