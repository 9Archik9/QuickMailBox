document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    const loadingIcon = document.getElementById('loading-icon');
    const checkInterval = 5000; // 5 секунд

    async function checkMail() {
        try {
            const response = await fetch('/receive_message/api/check_mail/');
            const data = await response.json();

            if (data.messages.length > 0) {
                messageContainer.innerHTML = '';
                data.messages.forEach(message => {
                    const messageElement = document.createElement('p');
                    messageElement.textContent = `From: ${message.sender}, Subject: ${message.subject}, Content: ${message.content}`;
                    messageContainer.appendChild(messageElement);
                });
            } else {
                messageContainer.textContent = 'Checking for emails every 5 seconds';
            }
        } catch (error) {
            console.error('Error checking mail:', error);
        } finally {
            loadingIcon.style.display = 'none';
        }
    }

    setInterval(checkMail, checkInterval);
});
