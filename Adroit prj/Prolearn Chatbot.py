import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime, timedelta, date

class ProLearnChatbot:
    def __init__(self, master):
        self.master = master
        master.title("ProLearn Chatbot")

        self.chat_log = scrolledtext.ScrolledText(master, state=tk.DISABLED, height=20, width=80)
        self.chat_log.pack(padx=10, pady=10)

        self.input_entry = tk.Entry(master, width=80)
        self.input_entry.pack(padx=10, pady=5)
        self.input_entry.bind("<Return>", self.send_message)
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.memory = {}

        self.faq = {
            "how do i login to prolearn?": "Enter the username and password provided to you and click on the 'Login' button.",
            "where can i find the courses i have enrolled in?": "If you are using a PC or mobile, you will see an icon on the top left corner. Click on it, then select 'My Courses' to view your enrolled courses.",
            "how do i access my course content?": "Click on the course under 'My Courses,' and you will be redirected to your course page.",
            "what will be available on my course page?": "Your course page includes: Syllabus, Question Bank, Session Content, Course Roadmap, Agenda, Assignments, Quizzes, Videos.",
            "can i download the course materials?": "Yes, click on the respective activity, and you will find an option to download the document.",
            "are videos available in the course?": "Yes, course-related videos are provided for better understanding and learning.",
            "how do i submit an assignment?": "Click on the assignment activity. You will be directed to the submission page. Click 'Add Submission' and upload your file.",
            "what file formats are accepted for assignment submission?": "Accepted file formats may include PDF, Word documents, and other specified formats by the instructor.",
            "can i edit my assignment submission?": "Yes, if your instructor allows it, you will see an 'Edit Submission' option before the deadline.",
            "how do i check if my assignment is submitted successfully?": "Once you upload the file, you will see a confirmation message or a status update on the assignment page.",
            "how do i attend a quiz?": "Click on the quiz activity and then select 'Attempt Quiz' to begin.",
            "what should i do after completing the quiz?": "Click 'Finish Attempt' to review your answers, then submit your attempt.",
            "can i retake a quiz?": "This depends on the instructor’s settings. Some quizzes allow multiple attempts, while others do not.",
            "how do i check my quiz results?": "After submission, you can see your score immediately (if auto-graded) or check under the quiz activity once the instructor releases results.",
            "i forgot my password. how can i reset it?": "Click on 'Forgot Password' on the login page and follow the instructions to reset it via email.",
            "why can’t i see my enrolled course?": "Ensure that you are logged in with the correct credentials. If the issue persists, contact your administrator.",
            "how do i contact support for technical issues?": "Use the 'Help' or 'Support' section on prolearn or contact your instructor for assistance.",
            "can i access prolearn on my mobile?": "Yes, prolearn is accessible via mobile browsers, and in some cases, a mobile app might be available.",
            "what should i do if my uploaded file is not appearing?": "Refresh the page and check again. If the issue continues, try re-uploading the file or contacting support.",
            "how do i log out of prolearn?": "Click on your profile icon in the top right corner and select 'Logout'.",
            "list all available courses": "Available courses: Course A, Course B, Course C. Please specify which course you want information about.",

            # Basic conversational questions
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! How can I help you?",
            "how are you?": "I'm just a bot, but I'm here and ready to help!",
            "what is todays date?": "__get_date__",
            "bye": "Goodbye! Have a great day and happy learning!",
            "goodbye": "Take care! See you next time on prolearn.",
        }

        self.reminders = []
        self.edit_mode = False
        self.block_drawer_open = False

        self.display_message("Prolearn Chatbot: Hi, how can I help you?")

    def get_bot_response(self, user_input):
        user_input = user_input.lower().strip()
        if any(phrase in user_input for phrase in ["how are you", "how are u", "how r u"]):
            return "I'm just a bot, but I'm doing great! How can I assist you today?"
    
        elif any(phrase in user_input for phrase in ["bye", "ok bye", "okay bye", "ok goodbye", "goodbye"]):
            return "Goodbye! Have a great day and happy learning!"

        response = self.faq.get(user_input)
        if response == "__get_date__":
            return datetime.now().strftime("Today is %A, %B %d, %Y.")
        elif response:
            return response
        else:
            return None


    def display_message(self, message):
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def send_message(self,event=None):
        user_input = self.input_entry.get().lower()
        self.display_message("You: " + user_input)
        self.input_entry.delete(0, tk.END)

        response = self.get_bot_response(user_input)
        if response:
            self.display_message("Prolearn Chatbot: " + response)
            self.memory[user_input] = response
        elif "time plan" in user_input:
            response = self.generate_time_plan()
            self.display_message("Prolearn Chatbot: " + response)
        elif "dark mode" in user_input or "switch to dark mode" in user_input:
            self.set_dark_mode()
            self.display_message("Prolearn Chatbot: Dark mode activated")
        elif "light mode" in user_input or "switch to light mode" in user_input:
            self.set_light_mode()
            self.display_message("Prolearn Chatbot: Light mode activated")
        elif "grades" in user_input:
            response = "For grades, please contact your instructor with your student ID."
            self.display_message("Prolearn Chatbot: " + response)
        elif "contact" in user_input:
            response = "For further assistance, please contact support@prolearn.com"
            self.display_message("Prolearn Chatbot: " + response)
        elif "set reminder" in user_input:
            self.set_reminder()
        elif "feedback" in user_input:
            self.get_feedback()
        elif "edit mode on" in user_input:
            self.edit_mode = True
            self.display_message("Prolearn Chatbot: Edit mode is on.")
        elif "edit mode off" in user_input:
            self.edit_mode = False
            self.display_message("Prolearn Chatbot: Edit mode is off.")
        elif "open block drawer" in user_input:
            self.block_drawer_open = True
            self.display_message("Prolearn Chatbot: Block drawer opened.")
        elif "close block drawer" in user_input:
            self.block_drawer_open = False
            self.display_message("Prolearn Chatbot: Block drawer closed.")
        else:
            self.display_message("Prolearn Chatbot: Can you provide more information on what you need?")
            self.memory[user_input] = "Needs clarification"

    def generate_time_plan(self):
        today = date.today()
        plan = "Here is a sample time plan:\n"
        for i in range(7):
            day = today + timedelta(days=i)
            plan += f"{day.strftime('%A')}: Study for 2 hours\n"
        return plan

    def set_dark_mode(self):
        self.master.config(bg="gray20")
        self.chat_log.config(bg="gray15", fg="white")
        self.input_entry.config(bg="gray15", fg="white", insertbackground="white")

    def set_light_mode(self):
        self.master.config(bg="SystemButtonFace")
        self.chat_log.config(bg="white", fg="black")
        self.input_entry.config(bg="white", fg="black", insertbackground="black")

    def set_reminder(self):
        reminder_text = simpledialog.askstring("Set Reminder", "Enter reminder text:")
        if reminder_text:
            reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder time (YYYY-MM-DD HH:MM):")
            if reminder_time:
                try:
                    reminder_datetime = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
                    self.reminders.append((reminder_datetime, reminder_text))
                    self.display_message(f"Prolearn Chatbot: Reminder set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}: {reminder_text}")
                except ValueError:
                    self.display_message("Prolearn Chatbot: Invalid time format. Please use YYYY-MM-DD HH:MM.")

    def get_feedback(self):
        feedback = simpledialog.askstring("Feedback", "Enter your feedback:")
        if feedback:
            self.display_message("Prolearn Chatbot: Thank you for your feedback!")

# Run the chatbot
root = tk.Tk()
chatbot = ProLearnChatbot(root)
root.mainloop()
