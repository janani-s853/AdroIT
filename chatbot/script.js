let chatbox = document.getElementById("chatbox-modal");
let chatboxIcon = document.querySelector(".chatbox-icon");
let closeChatboxBtn = document.getElementById("closeChatbox");
let chatboxBody = document.getElementById("chatbox-body");
let chatboxInput = document.getElementById("chatbox-input");
let sendBtn = document.getElementById("send-btn");
let reservationDetails = {};

chatboxIcon.addEventListener("click", function () {
    chatbox.style.display = "flex";
    if (!chatboxBody.innerHTML) { 
        showWelcomeMessage();
    }
});

chatboxInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {  
        event.preventDefault();  
        sendBtn.click();  
    }
});
closeChatboxBtn.addEventListener("click", function () {
    chatbox.style.display = "none";
});

function showWelcomeMessage() {
    let welcomeMessage = ` 
        <div class="chatbot-message">
            <div class="chatbot-bubble">
                <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                <div class="chat-message">
                    Hello! Welcome to XYZ. I'm xyzAI, your virtual assistant 😎
                    <br>How can I help you today?
                    <br><br>
                    <button class="option-btn" onclick="handleOptionClick('bookReservation')">Book Reservation</button>
                    <button class="option-btn" onclick="handleOptionClick('locateStore')">Locate Nearby Store</button>
                    <button class="option-btn" onclick="handleOptionClick('viewMenu')">View Menu</button>
                </div>
            </div>
        </div>
    `;
    chatboxBody.innerHTML = welcomeMessage;  
}

function handleOptionClick(option) {
    let optionBtns = document.querySelectorAll(".option-btn");
    optionBtns.forEach(btn => {
        btn.classList.add("disabled-option");
        btn.disabled = true; 
    });

    let responseMessage = "";

    if (option === "bookReservation") {
        responseMessage = "Booking a reservation! Please choose the date and time 🗓️";
        chatboxBody.innerHTML += `
            <div class="chatbot-message">
                <div class="chatbot-bubble">
                    <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                    <div class="chat-message">${responseMessage}</div>
                </div>
            </div>
        `;
        showDateAndTimePicker();

    } else if (option === "viewMenu") {
        window.open("https://a2bva.com/menu/", "_blank");
        responseMessage = "I have opened the menu for you in a new tab. Let me know if you need anything else!";
        chatboxBody.innerHTML += `
            <div class="chatbot-message">
                <div class="chatbot-bubble">
                    <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                    <div class="chat-message">${responseMessage}</div>
                </div>
            </div>
        `;
        setTimeout(function() {
            showWelcomeMessage();
            optionBtns.forEach(btn => {
                btn.classList.remove("disabled-option");
                btn.disabled = false;  
            });
        }, 4000);

    } else if (option === "locateStore") {
        window.open("https://stores.lenskart.com/", "_blank");
        responseMessage = "I have opened the nearest stores page for you in a new tab. Let me know if you need anything else!";
        chatboxBody.innerHTML += `
            <div class="chatbot-message">
                <div class="chatbot-bubble">
                    <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                    <div class="chat-message">${responseMessage}</div>
                </div>
            </div>
        `;
        setTimeout(function() {
            showWelcomeMessage();
            optionBtns.forEach(btn => {
                btn.classList.remove("disabled-option");
                btn.disabled = false;  
            });
        }, 4000);
    }
}

function showDateAndTimePicker() {
    let date = new Date();
    let tomorrow = new Date(date);
    tomorrow.setDate(date.getDate() + 1);

    let dayAfterTomorrow = new Date(date);
    dayAfterTomorrow.setDate(date.getDate() + 2);

    let tomorrowFormatted = tomorrow.toISOString().split("T")[0];
    let dayAfterTomorrowFormatted = dayAfterTomorrow.toISOString().split("T")[0];

    let dateOptions = ` 
        <label for="date">Choose a date:</label>
        <input type="date" id="date" class="date-picker" min="${tomorrowFormatted}" max="${dayAfterTomorrowFormatted}" oninput="this.setCustomValidity('')" />
        <br>
        <label for="time">Choose a time:</label>
        <select id="time" class="time-picker">
            <option value="09:00">9:00 AM</option>
            <option value="12:00">12:00 PM</option>
            <option value="15:00">3:00 PM</option>
            <option value="18:00">6:00 PM</option>
            <option value="21:00">9:00 PM</option>
        </select>
        <br>
        <div class="confirm-btn-container">
            <button onclick="handleConfirmReservation()" class="confirm-btn">Confirm</button>
        </div>
    `;

    chatboxBody.innerHTML += `
        <div class="chatbot-message">
            <div class="chatbot-bubble">
                <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                <div class="chat-message">${dateOptions}</div>
            </div>
        </div>
    `;

    let dateInput = document.getElementById("date");
    dateInput.addEventListener("keydown", function(event) {
        event.preventDefault();
    });
}

function handleConfirmReservation() {
    let selectedDate = document.getElementById("date").value;
    let selectedTime = document.getElementById("time").value;

    if (!selectedDate || !selectedTime) {
        alert("Please select both date and time.");
        return;
    }

    reservationDetails.date = selectedDate;
    reservationDetails.time = selectedTime;

    let responseMessage = `Great! You've selected ${selectedDate} at ${selectedTime}. How many people should I reserve for? 👥`;
    chatboxBody.innerHTML += `
        <div class="chatbot-message">
            <div class="chatbot-bubble">
                <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                <div class="chat-message">${responseMessage}</div>
            </div>
        </div>
    `;

    chatboxInput.disabled = false;
    chatboxInput.placeholder = "Type Something...";
    sendBtn.disabled = false;
}


sendBtn.addEventListener("click", function () {
    let userMessage = chatboxInput.value.trim().toLowerCase();
    if (userMessage) {
        chatboxBody.innerHTML += `
            <div class="user-message">
                <div class="user-bubble user-bubble-right">
                    <div class="chat-message">${userMessage}</div>
                </div>
            </div>
        `;
        chatboxInput.value = "";
        chatboxInput.disabled = true;
        sendBtn.disabled = true;
        if (!reservationDetails.people) {
            let numberPattern = /^(1|2|3|4|5|6|7|8|people|table|of|one|two|three|four|five|six|seven|eight)$/i;
            if (numberPattern.test(userMessage)) {
                if (["people", "table", "of"].includes(userMessage)) {
                    let responseMessage = "I can't understand you. Please give a valid input.";
                    chatboxBody.innerHTML += `
                        <div class="chatbot-message">
                            <div class="chatbot-bubble">
                                <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                                <div class="chat-message">${responseMessage}</div>
                            </div>
                        </div>
                    `;
                    chatboxInput.disabled = false;
                    chatboxInput.placeholder = "Type Something...";
                    sendBtn.disabled = false;
                    return;  
                } else {
                    reservationDetails.people = parseInt(userMessage, 10) || getTextualNumber(userMessage);
                    let responseMessage = `Wonderful! What name should I reserve the table under? 📝`;
                    chatboxBody.innerHTML += `
                        <div class="chatbot-message">
                            <div class="chatbot-bubble">
                                <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                                <div class="chat-message">${responseMessage}</div>
                            </div>
                        </div>
                    `;
                    chatboxInput.disabled = false;
                    chatboxInput.placeholder = "Type Something...";
                    sendBtn.disabled = false;
                }
            } else {
                let responseMessage = "I can't understand you. Please give a valid input.";
                chatboxBody.innerHTML += `
                    <div class="chatbot-message">
                        <div class="chatbot-bubble">
                            <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                            <div class="chat-message">${responseMessage}</div>
                        </div>
                    </div>
                `;
                chatboxInput.disabled = false;
                chatboxInput.placeholder = "Type Something...";
                sendBtn.disabled = false;
            }
        } else if (!reservationDetails.name) {
            reservationDetails.name = userMessage;
            let responseMessage = `Thanks, ${reservationDetails.name}! Could you share a contact number so we can confirm the reservation? ☎️`;
            chatboxBody.innerHTML += `
                <div class="chatbot-message">
                    <div class="chatbot-bubble">
                        <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                        <div class="chat-message">${responseMessage}</div>
                    </div>
                </div>
            `;
            chatboxInput.disabled = false;  
            sendBtn.disabled = false; 
        } else if (!validatePhoneNumber(userMessage)) {
            let responseMessage = "I can't understand you. Please provide a valid 10-digit phone number.";
            chatboxBody.innerHTML += `
                <div class="chatbot-message">
                    <div class="chatbot-bubble">
                        <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                        <div class="chat-message">${responseMessage}</div>
                    </div>
                </div>
            `;
            chatboxInput.disabled = false;  
            sendBtn.disabled = false; 
        } else {
            reservationDetails.contact = userMessage;
            let confirmationMessage = `Your reservation for ${reservationDetails.people} people on ${reservationDetails.date} at ${reservationDetails.time} has been confirmed! 🎉
                                      <br> Name: ${reservationDetails.name} 
                                      <br> Contact: ${reservationDetails.contact}
                                      <br> See you soon! If you need to make another reservation, just let me know.`;
            chatboxBody.innerHTML += `
                <div class="chatbot-message">
                    <div class="chatbot-bubble">
                        <img src="images/chatbot.png" class="chatbot-img" alt="FoodieAI" />
                        <div class="chat-message">${confirmationMessage}</div>
                    </div>
                </div>
            `;
            setTimeout(function() {
                showWelcomeMessage();
            }, 4000);
        }
    }
});

function validatePhoneNumber(number) {
    const phonePattern = /^\d{10}$/;
    return phonePattern.test(number);
}

function getTextualNumber(word) {
    const numberWords = {
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8
    };
    return numberWords[word.toLowerCase()] || 0;
}
