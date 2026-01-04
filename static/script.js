let currentTab = 'chat';
let isLoading = false;

// Switch tabs
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update tab buttons
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName + 'Tab').classList.add('active');
    
    // Load data for the tab
    if (tabName === 'history') {
        loadHistory();
    } else if (tabName === 'knowledge') {
        loadKnowledge();
    }
}

// Send message
async function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    const model = document.getElementById('modelSelect').value;
    
    // Add user message to chat
    addMessageToChat('user', message);
    input.value = '';
    isLoading = true;
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, model })
        });
        
        const data = await response.json();
        
        if (data.success) {
            removeLoading();
            addMessageToChat('assistant', data.response);
            updateStats();
        } else {
            removeLoading();
            addMessageToChat('assistant', 'Error: ' + data.error, true);
        }
    } catch (error) {
        removeLoading();
        addMessageToChat('assistant', 'Connection error. Please try again.', true);
    }
    
    isLoading = false;
}

// Add message to chat
function addMessageToChat(role, content, isError = false) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remove welcome message if exists
    const welcome = chatMessages.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    if (isError) messageDiv.style.background = '#fee2e2';
    
    messageDiv.innerHTML = `
        <div class="message-header">${role === 'user' ? 'You' : 'AI Assistant'}</div>
        <div class="message-content">${content}</div>
        <div class="message-time">${new Date().toLocaleTimeString()}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show loading
function showLoading() {
    const chatMessages = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.id = 'loadingIndicator';
    loadingDiv.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading
function removeLoading() {
    const loading = document.getElementById('loadingIndicator');
    if (loading) loading.remove();
}

// Handle key press
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        const historyList = document.getElementById('historyList');
        historyList.innerHTML = '';
        
        if (data.history.length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📭</div>
                    <p>No conversation history yet</p>
                </div>
            `;
            return;
        }
        
        data.history.forEach(item => {
            const historyItem = document.createElement('div');
            historyItem.className = `history-item ${item.role}`;
            historyItem.innerHTML = `
                <div class="history-item-header">
                    ${item.role === 'user' ? 'You' : 'AI'} - ${new Date(item.timestamp).toLocaleString()}
                </div>
                <div class="history-item-content">${item.content}</div>
            `;
            historyList.appendChild(historyItem);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Load knowledge
async function loadKnowledge() {
    try {
        const response = await fetch('/api/knowledge');
        const data = await response.json();
        
        const knowledgeList = document.getElementById('knowledgeList');
        knowledgeList.innerHTML = '';
        
        if (data.knowledge.length === 0) {
            knowledgeList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📚</div>
                    <p>No knowledge stored yet. Start asking questions!</p>
                </div>
            `;
            return;
        }
        
        data.knowledge.forEach(item => {
            const card = document.createElement('div');
            card.className = 'knowledge-card';
            card.innerHTML = `
                <div class="knowledge-card-icon">💡</div>
                <div class="knowledge-card-topic">${item.topic}</div>
                <div class="knowledge-card-content">${item.content}</div>
                <div class="knowledge-card-time">Added: ${new Date(item.timestamp).toLocaleString()}</div>
            `;
            knowledgeList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading knowledge:', error);
    }
}

// Clear history
async function clearHistory() {
    if (!confirm('Are you sure you want to clear all history?')) return;
    
    try {
        await fetch('/api/clear-history', { method: 'POST' });
        loadHistory();
        document.getElementById('chatMessages').innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">🎓</div>
                <h2>Welcome to Academic AI!</h2>
                <p>Ask me anything about your studies. I'm here to help you learn.</p>
            </div>
        `;
        updateStats();
    } catch (error) {
        alert('Error clearing history');
    }
}

// Clear knowledge
async function clearKnowledge() {
    if (!confirm('Are you sure you want to clear all knowledge?')) return;
    
    try {
        await fetch('/api/clear-knowledge', { method: 'POST' });
        loadKnowledge();
        updateStats();
    } catch (error) {
        alert('Error clearing knowledge');
    }
}

// Export data
async function exportData() {
    try {
        const [historyRes, knowledgeRes] = await Promise.all([
            fetch('/api/history'),
            fetch('/api/knowledge')
        ]);
        
        const history = await historyRes.json();
        const knowledge = await knowledgeRes.json();
        
        const data = {
            history: history.history,
            knowledge: knowledge.knowledge,
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'chatbot-data-' + new Date().toISOString().split('T')[0] + '.json';
        a.click();
        URL.revokeObjectURL(url);
    } catch (error) {
        alert('Error exporting data');
    }
}

// Update stats
async function updateStats() {
    try {
        const [historyRes, knowledgeRes] = await Promise.all([
            fetch('/api/history'),
            fetch('/api/knowledge')
        ]);
        
        const history = await historyRes.json();
        const knowledge = await knowledgeRes.json();
        
        document.getElementById('statsText').textContent = 
            `Knowledge: ${knowledge.knowledge.length} | History: ${history.history.length}`;
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Initialize on load
window.addEventListener('load', () => {
    updateStats();
});