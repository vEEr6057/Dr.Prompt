const chatbox = document.getElementById('messages');

// Function to add a message to the chatbox
function addMessage(content, sender) {
    const message = document.createElement('div');
    message.classList.add('message', sender);
    message.textContent = content;
    chatbox.appendChild(message);
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Function to send a message to the Flask backend
function sendMessage() {
    const userMessage = document.getElementById('userMessage').value;
    if (userMessage === "") return;

    // Display the user's message
    addMessage(userMessage, 'user');

    // Clear the input box
    document.getElementById('userMessage').value = '';

    // Make a request to the Flask backend
    fetch('/get_doctor_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: userMessage }),  // Sending user input as doctor name to backend
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            addMessage(data.error, 'bot');
        } else {
            if (data.name=="yes schedule it "){
                const botReply = `${data.location}`;
                addMessage(botReply, 'bot');                    
            }
           else if (data.name=="show doctor available "){
                const botReply = `${data.location}`;
                addMessage(botReply, 'bot'); 
            }
            else if (data.name=="when will be my meeting then "){
                const botReply = `${data.location}`;
                addMessage(botReply, 'bot'); 
            }

            else {
            const botReply = `Doctor: ${data.name}, Specialty: ${data.specialty}, Location: ${data.location}, Hospital: ${data.hospital}, Contact: ${data.contact}`;
            addMessage(botReply, 'bot');}
        } 
        
    })
    .catch(error => {
        addMessage("Sorry, something went wrong. Please try again.", 'bot');
        console.error('Error:', error);
    });
}
