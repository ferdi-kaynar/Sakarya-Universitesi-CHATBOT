document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Mesaj gönderme fonksiyonu
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        // Kullanıcı mesajını ekrana ekle
        addMessage(message, 'user');
        userInput.value = '';

        // Yükleniyor mesajı göster
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot');
        
        const loadingContent = document.createElement('div');
        loadingContent.classList.add('message-content', 'loading-message');
        loadingContent.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        
        loadingDiv.appendChild(loadingContent);
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // API'ye istek gönder
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Yükleniyor mesajını kaldır
            chatMessages.removeChild(loadingDiv);
            
            // Botun yanıtını ekrana ekle
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            // Yükleniyor mesajını kaldır
            chatMessages.removeChild(loadingDiv);
            
            // Hata mesajı göster
            addMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.', 'bot');
            console.error('Error:', error);
        });
    }

    // Mesaj ekleme fonksiyonu
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = text;

        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Sohbet alanını en alta kaydır
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageDiv;
    }

    // Gönder butonuna tıklama olayını ekle
    sendButton.addEventListener('click', sendMessage);

    // Enter tuşuna basma olayını ekle
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}); 