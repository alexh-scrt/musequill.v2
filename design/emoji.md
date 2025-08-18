👍 Thumbs up

🏗️ Loading...

### ✅ Success States

* **Initialized / Ready** → 🚀 (launch), ✅ (check mark), 🟢 (green circle), ✨ (sparkles)
* **Created / Connected** → 🔗 (link), 🆕 (new), 🟦 (blue square), 🤝 (handshake)

### ⚙️ In-Progress / Loading States

* **Loading / Starting** → ⏳ (hourglass), 🔄 (arrows circle), ⚙️ (gear), 🌀 (spinner), 🟡 (yellow circle)
* **Waiting / Pending** → 💤 (sleep), 🕒 (clock), 🟠 (orange circle)

### ❌ Failure / Error States

* **Failure** → ❌ (cross mark), 🔴 (red circle), 💥 (collision), 🛑 (stop sign)
* **Exception / Crash** → 💀 (skull), ⚡ (zap), 🪲 (bug), 🔥 (fire)

### 📊 Informational / Debug States

* **Info** → ℹ️ (info), 📘 (blue book), 📝 (memo), 🟦 (blue square)
* **Debug / Verbose** → 🐛 (bug), 🔍 (magnifying glass), 🧪 (test tube)
* **Config / Parameters** → 🛠️ (tools), 📦 (package), ⚙️ (gear)

### 🔒 Security / Auth States

* **Authentication Success** → 🔐 (closed lock with key), 🟢 (green circle)
* **Authentication Failure** → 🔓 (open lock), 🚫 (prohibited), 🟥 (red square)

---

### Example Log Lines

```text
2025-08-16 12:00:01 [INFO] 🚀 LLMService successfully initialized with model=llama3.3:70b
2025-08-16 12:00:05 [INFO] 🔄 Creating temporary LLM instance for custom parameters...
2025-08-16 12:00:06 [SUCCESS] ✅ Request completed in 0.42s
2025-08-16 12:00:08 [ERROR] ❌ Failed to initialize LLM: Connection refused
2025-08-16 12:00:09 [DEBUG] 🧪 Parameters used: temperature=0.3, top_p=1.0
```

---

👉 Pro tip:

* Use **circles (🟢 🟡 🔴)** for **status** (good for dashboards).
* Use **action icons (🚀 🔄 ❌)** for **events**.
* Keep it consistent so the eye can “pattern-match” quickly when scanning logs.

Do you want me to suggest a **fixed mapping dictionary** (like `LOG_EMOJIS = {"success": "✅", "error": "❌", ...}`) so you can easily integrate into your logging formatter?
