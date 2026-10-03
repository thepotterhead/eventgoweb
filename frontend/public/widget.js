(function () {
  class FunobotzTutorWidget extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      this.sessionId = 'widget_sess_' + Math.random().toString(36).substring(2, 9);
      this.apiUrl = this.getAttribute('data-api-url') || 'http://127.0.0.1:8000/api';
      this.customerId = this.getAttribute('data-customer-id') || 'FZ-HACK-001';
      this.character = this.getAttribute('data-character') || 'quacky';
      this.age = parseInt(this.getAttribute('data-learner-age') || '10');
      this.isOpen = false;
      this.messages = [];
    }

    connectedCallback() {
      this.render();
      this.initSession();
    }

    async initSession() {
      try {
        const res = await fetch(`${this.apiUrl}/session`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            learner_id: 'L-WIDGET',
            name: 'Store Visitor',
            age: this.age,
            customer_id: this.customerId,
            active_character: this.character
          })
        });
        const data = await res.json();
        this.addBotMessage(`Hi! I'm your Funobotz STEM Companion (${this.character.toUpperCase()}). Ask me anything about paper robotics!`);
      } catch (e) {
        this.addBotMessage("Hi! I'm your Funobotz STEM companion. Ask me a STEM question!");
      }
    }

    addBotMessage(text) {
      this.messages.push({ sender: 'bot', text });
      this.updateMessages();
    }

    addUserMessage(text) {
      this.messages.push({ sender: 'user', text });
      this.updateMessages();
      this.sendChat(text);
    }

    async sendChat(msg) {
      try {
        const res = await fetch(`${this.apiUrl}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: this.sessionId,
            message: msg,
            customer_id: this.customerId,
            requested_character: this.character
          })
        });
        const data = await res.json();
        this.addBotMessage(data.answer);
      } catch (e) {
        this.addBotMessage("Sorry, I had trouble reaching the Funobotz backend server.");
      }
    }

    updateMessages() {
      const container = this.shadowRoot.querySelector('.chat-body');
      if (!container) return;
      container.innerHTML = this.messages.map(m => `
        <div style="margin-bottom:8px; padding:8px 12px; border-radius:12px; max-width:85%; font-size:13px; line-height:1.4; ${m.sender === 'user' ? 'background:#6366f1; color:#fff; margin-left:auto;' : 'background:#334155; color:#f8fafc; margin-right:auto;'}">
          ${m.text}
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }

    render() {
      this.shadowRoot.innerHTML = `
        <style>
          :host {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            font-family: system-ui, -apple-system, sans-serif;
          }
          .trigger-btn {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            color: white;
            border: none;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.5);
            cursor: pointer;
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
          }
          .trigger-btn:hover { transform: scale(1.08); }
          .widget-box {
            display: ${this.isOpen ? 'flex' : 'none'};
            flex-direction: column;
            width: 320px;
            height: 420px;
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            overflow: hidden;
            position: absolute;
            bottom: 70px;
            right: 0;
          }
          .header {
            background: #1e293b;
            padding: 12px 16px;
            color: #fff;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }
          .chat-body {
            flex: 1;
            padding: 12px;
            overflow-y: auto;
            background: #0f172a;
          }
          .input-row {
            padding: 8px;
            background: #1e293b;
            display: flex;
            gap: 6px;
          }
          .input-row input {
            flex: 1;
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            padding: 8px;
            color: #fff;
            font-size: 12px;
          }
          .input-row button {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0 12px;
            cursor: pointer;
            font-weight: 600;
          }
        </style>
        <div class="widget-box">
          <div class="header">
            <span>🤖 Funobotz STEM Companion</span>
            <span style="font-size:10px; background:#10b981; padding:2px 6px; border-radius:10px;">Acc: ${this.customerId}</span>
          </div>
          <div class="chat-body"></div>
          <form class="input-row" id="chat-form">
            <input type="text" placeholder="Ask a question..." id="msg-input" />
            <button type="submit">Send</button>
          </form>
        </div>
        <button class="trigger-btn" id="toggle-btn">🤖</button>
      `;

      this.shadowRoot.getElementById('toggle-btn').onclick = () => {
        this.isOpen = !this.isOpen;
        this.shadowRoot.querySelector('.widget-box').style.display = this.isOpen ? 'flex' : 'none';
      };

      this.shadowRoot.getElementById('chat-form').onsubmit = (e) => {
        e.preventDefault();
        const input = this.shadowRoot.getElementById('msg-input');
        if (input.value.trim()) {
          this.addUserMessage(input.value.trim());
          input.value = '';
        }
      };
    }
  }

  customElements.define('funobotz-tutor', FunobotzTutorWidget);
})();
