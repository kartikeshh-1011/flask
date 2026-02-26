/* =====================================================
   Apex Learning Hub – Chatbot Frontend Logic
   Powered by Google Gemini via Flask /chatbot endpoint
   ===================================================== */

(function () {
    'use strict';

    /* ---------- DOM refs ---------- */
    const toggle = document.getElementById('chatbot-toggle');
    const window_el = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('chatbot-close');
    const messagesEl = document.getElementById('chatbot-messages');
    const inputEl = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send');
    const notifDot = document.querySelector('#chatbot-toggle .notif-dot');
    const suggestions = document.querySelectorAll('.suggestion-chip');

    if (!toggle) return; // guard if widget not in DOM

    /* ---------- State ---------- */
    let isOpen = false;
    let isWaiting = false;

    /* ---------- Open / Close ---------- */
    toggle.addEventListener('click', () => {
        isOpen = !isOpen;
        window_el.classList.toggle('open', isOpen);
        toggle.innerHTML = isOpen
            ? '<i class="fas fa-times"></i>'
            : '<i class="fas fa-robot"></i><span class="notif-dot"></span>';
        if (isOpen) {
            // hide notification dot once opened
            const dot = toggle.querySelector('.notif-dot');
            if (dot) dot.style.display = 'none';
            inputEl.focus();
            scrollToBottom();
        }
    });

    closeBtn.addEventListener('click', () => {
        isOpen = false;
        window_el.classList.remove('open');
        toggle.innerHTML = '<i class="fas fa-robot"></i>';
    });

    /* ---------- Suggested chips ---------- */
    suggestions.forEach(chip => {
        chip.addEventListener('click', () => {
            const text = chip.textContent.trim();
            sendMessage(text);
        });
    });

    /* ---------- Send via button ---------- */
    sendBtn.addEventListener('click', () => {
        const msg = inputEl.value.trim();
        if (msg && !isWaiting) sendMessage(msg);
    });

    /* ---------- Send via Enter key ---------- */
    inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !isWaiting) {
            e.preventDefault();
            const msg = inputEl.value.trim();
            if (msg) sendMessage(msg);
        }
    });

    /* ---------- Core send function ---------- */
    async function sendMessage(text) {
        if (!text || isWaiting) return;

        // Display user bubble
        appendBubble('user', text);
        inputEl.value = '';
        inputEl.disabled = true;
        sendBtn.disabled = true;
        isWaiting = true;

        // Show typing indicator
        const typingId = showTyping();

        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            removeTyping(typingId);

            if (data.success) {
                appendBubble('bot', data.reply);
            } else {
                appendBubble('bot', '⚠️ ' + (data.error || 'Something went wrong. Please try again.'));
            }

        } catch (err) {
            removeTyping(typingId);
            appendBubble('bot', '⚠️ Cannot reach the server. Please check your connection.');
        } finally {
            inputEl.disabled = false;
            sendBtn.disabled = false;
            isWaiting = false;
            inputEl.focus();
        }
    }

    /* ---------- Append a message bubble ---------- */
    function appendBubble(role, text) {
        const wrapper = document.createElement('div');
        wrapper.className = `chat-msg ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = role === 'bot' ? '🤖' : '👤';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        // Convert markdown-like **bold** and newlines
        bubble.innerHTML = formatText(text);

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);
        scrollToBottom();
    }

    /* ---------- Typing indicator ---------- */
    function showTyping() {
        const id = 'typing-' + Date.now();
        const wrapper = document.createElement('div');
        wrapper.className = 'chat-msg bot';
        wrapper.id = id;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = '🤖';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.innerHTML = `
            <div class="typing-bubble">
                <span></span><span></span><span></span>
            </div>`;

        wrapper.appendChild(avatar);
        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);
        scrollToBottom();
        return id;
    }

    function removeTyping(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    /* ---------- Helpers ---------- */
    function scrollToBottom() {
        setTimeout(() => {
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }, 50);
    }

    function formatText(text) {
        // Convert **bold**, *italic*, newlines to HTML
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

})();
