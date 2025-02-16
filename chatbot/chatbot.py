from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')

app = Flask(__name__)

reservation_details = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    user_message = request.json.get('message')
    response = process_message(user_message)
    return jsonify({'response': response})

def process_message(message):
    tokens = word_tokenize(message.lower())

    if 'book reservation' in tokens:
        return "Booking a reservation! Please choose the date and time 🗓️"
    elif 'view menu' in tokens:
        return "I have opened the menu for you in a new tab. Let me know if you need anything else!"
    elif 'locate store' in tokens:
        return "I have opened the nearest stores page for you in a new tab. Let me know if you need anything else!"
    elif 'people' in tokens or 'of' in tokens:
        return handle_reservation_people(tokens)
    elif 'confirm' in tokens:
        return confirm_reservation()
    elif validate_phone_number(message):
        return "Your contact number is confirmed. Thank you!"
    elif reservation_details.get('people') and not reservation_details.get('name'):
        return "What name should I reserve the table under? 📝"
    elif reservation_details.get('name') and not reservation_details.get('contact'):
        return "Could you share a contact number so we can confirm the reservation? ☎️"
    else:
        return "Sorry, I couldn't understand that. Please try again."

def handle_reservation_people(tokens):
    for word in tokens:
        if word.isdigit():
            reservation_details['people'] = int(word)
        elif word in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']:
            reservation_details['people'] = get_textual_number(word)
    
    return f"Wonderful! You selected {reservation_details['people']} people. What name should I reserve the table under? 📝"

def get_textual_number(word):
    number_words = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8
    }
    return number_words.get(word, 0)

def confirm_reservation():
    if reservation_details.get('people') and reservation_details.get('name') and reservation_details.get('contact'):
        confirmation_message = (
            f"Your reservation for {reservation_details['people']} people is confirmed! 🎉\n"
            f"Name: {reservation_details['name']}\n"
            f"Contact: {reservation_details['contact']}\n"
            "See you soon! If you need to make another reservation, just let me know."
        )
        reset_reservation()
        return confirmation_message
    else:
        return "Please complete all reservation details first."

def reset_reservation():
    reservation_details.clear()

def validate_phone_number(number):
    phone_pattern = re.compile(r'^\d{10}$')
    return bool(phone_pattern.match(number))

if __name__ == '__main__':
    app.run(debug=True)
