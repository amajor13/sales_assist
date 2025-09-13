import React, { useState } from "react";

const API_BASE = "http://127.0.0.1:8000"; // FastAPI backend

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  // Email states
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [template, setTemplate] = useState("Hi {name}, I wanted to tell you about {product} at {company}.");

  // --- Chat Functionality ---
  async function sendMessage() {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: input }]);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `${data.reply || "No response"} (Intent: ${
            data.intent || "unknown"
          }, Reason: ${data.reason || "n/a"})`,
        },
      ]);
    } catch (error) {
      console.error("Error talking to backend:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Backend not reachable." },
      ]);
    }

    setInput("");
  }

  // --- Email Functionality ---
  async function sendEmail() {
    if (!email || !subject || !template) {
      alert("Please fill all email fields!");
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/send_email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to_email: email,
          subject: subject,
          template: template,
          personalization: {
            name: "Ashutosh", // Replace later with user input or CRM data
            company: "Visa",
            product: "AI Sales Bot",
          },
        }),
      });

      const data = await res.json();
      alert(data.message || "Email sent!");
    } catch (error) {
      console.error("Error sending email:", error);
      alert("⚠️ Could not send email.");
    }
  }

  return (
    <div style={{ fontFamily: "Arial, sans-serif", maxWidth: "800px", margin: "20px auto" }}>
      <h2>💬 Sales Assistant Bot</h2>

      {/* Chatbox */}
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: "10px",
          padding: "10px",
          height: "300px",
          overflowY: "auto",
          marginBottom: "10px",
        }}
      >
        {messages.map((msg, idx) => (
          <div key={idx} style={{ textAlign: msg.sender === "user" ? "right" : "left", margin: "5px 0" }}>
            <b>{msg.sender === "user" ? "You" : "Bot"}:</b> {msg.text}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{ flex: 1, padding: "10px", borderRadius: "5px", border: "1px solid #ccc" }}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage} style={{ padding: "10px 20px" }}>
          Send
        </button>
      </div>

      {/* Email Section */}
      <h3>📧 Send Personalized Email</h3>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Recipient Email"
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <input
        type="text"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        placeholder="Email Subject"
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <textarea
        value={template}
        onChange={(e) => setTemplate(e.target.value)}
        placeholder="Email Template (use {name}, {company}, {product})"
        rows="5"
        style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
      />
      <button onClick={sendEmail} style={{ padding: "10px 20px" }}>
        Send Email
      </button>
    </div>
  );
}

export default App;
