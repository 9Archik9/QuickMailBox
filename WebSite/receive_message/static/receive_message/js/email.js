document.addEventListener('DOMContentLoaded', function() {
    const messageContainer = document.getElementById('message-container');
    const checkInterval = 5000; // 5 секунд

    async function checkMail() {
        try {
            const response = await fetch('/receive_message/api/check_mail/');
            const data = await response.json();

            messageContainer.innerHTML = '';
            if (data.messages.length > 0) {
                data.messages.forEach(message => {
                    const messageRow = document.createElement('tr');
                    messageRow.innerHTML = `
                        <td>${message.sender}</td>
                        <td><strong>Subject:</strong> ${message.subject}<br><strong>Content:</strong> ${message.content}</td>
                        <td>${message.date}</td>
                    `;
                    messageContainer.appendChild(messageRow);
                });
            } else {
                messageContainer.innerHTML = '<tr><td colspan="3">No new emails</td></tr>';
            }
        } catch (error) {
            console.error('Error checking mail:', error);
        }
    }

    setInterval(checkMail, checkInterval);
});
