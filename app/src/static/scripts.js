document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    var marker = L.marker([0, 0]).addTo(map);

    // Obtenir la localisation actuelle de l'utilisateur
    navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        map.setView([lat, lng], 8); // Zoom moins bas
        marker.setLatLng([lat, lng]);
    });

    document.getElementById('sidebar-toggle').addEventListener('click', function() {
        document.getElementById('chat').classList.toggle('show');
    });

    document.getElementById('chat-input').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            var input = event.target.value;
            var messages = document.getElementById('chat-messages');

            var userMessage = document.createElement('div');
            userMessage.className = 'message user';
            userMessage.textContent = input;
            messages.appendChild(userMessage);

            sendMessage(input);

            event.target.value = '';
            messages.scrollTop = messages.scrollHeight;
        }
    });

    async function sendMessage(message) {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        const messages = document.getElementById('chat-messages');
        if (data.reply) {
            var botMessage = document.createElement('div');
            botMessage.className = 'message bot';
            botMessage.textContent = data.reply;
            messages.appendChild(botMessage);
        } else {
            var errorMessage = document.createElement('div');
            errorMessage.className = 'message error';
            errorMessage.textContent = data.error;
            messages.appendChild(errorMessage);
        }
        messages.scrollTop = messages.scrollHeight;
    }

    // Gestion de l'enregistrement vocal
    const recordButton = document.getElementById('record-button');
    let mediaRecorder;
    let audioChunks = [];

    recordButton.addEventListener('click', async () => {
        if (!mediaRecorder || mediaRecorder.state === 'inactive') {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                const formData = new FormData();
                formData.append('file', audioBlob, 'voice-message.wav');

                const response = await fetch('/vocal', {
                    method: 'POST',
                    body: formData
                });

                const responseBlob = await response.blob();
                const responseUrl = URL.createObjectURL(responseBlob);
                const messages = document.getElementById('chat-messages');
                
                const botMessage = document.createElement('div');
                botMessage.className = 'message bot audio-message';
                
                const audioElement = document.createElement('audio');
                audioElement.controls = true;
                audioElement.src = responseUrl;
                
                botMessage.appendChild(audioElement);
                messages.appendChild(botMessage);
                
                messages.scrollTop = messages.scrollHeight;

                // play the audio
                audioElement.play();
                
                
            };

            mediaRecorder.start();
            recordButton.classList.add('recording');
        } else {
            mediaRecorder.stop();
            recordButton.classList.remove('recording');
        }
    });
});
