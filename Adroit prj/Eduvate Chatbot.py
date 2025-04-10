import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime, timedelta, date


class Eduvate:
    def __init__(self, master):
        self.master = master
        master.title("Eduvate Chatbot")

        self.chat_log = scrolledtext.ScrolledText(master, state=tk.DISABLED, height=20, width=80)
        self.chat_log.pack(padx=10, pady=10)

        self.input_entry = tk.Entry(master, width=80)
        self.input_entry.pack(padx=10, pady=5)
        self.input_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.memory = {}
        self.reminders = []
        self.edit_mode = False
        self.block_drawer_open = False

        self.faq_keywords = {
            ("login", "log in", "how do i log in"): "• Enter the username and password provided to you and click on the 'Login' button.",
            ("my courses", "enrolled courses", "where can i find courses"): "• Click the menu icon and then 'My Courses' to view your enrolled courses.",
            ("course content", "access course", "access course content"): "• Click on the course under 'My Courses' to go to your course page.",
            ("course page",): "Your course page includes:\n• Syllabus\n• Question Bank\n• Session Content\n• Course Roadmap\n• Agenda\n• Assignments\n• Quizzes\n• Videos",
            ("download materials", "download course", "download document"): "• Click on the activity, and you'll see a download option.",
            ("videos", "video available", "are videos available"): "• Yes, course-related videos are provided.",
            ("submit assignment", "assignment submit"): "• Go to the assignment activity and click 'Add Submission' to upload your file.",
            ("assignment formats", "file formats", "submit format"): "• Accepted formats include PDF, Word documents, etc.",
            ("edit assignment", "edit submission"): "• If allowed by your instructor, you can edit before the deadline.",
            ("assignment submitted", "check submission", "assignment status"): "• You'll see a confirmation message once uploaded.",
            ("attend quiz", "start quiz", "quiz begin"): "• Click on the quiz activity and select 'Attempt Quiz'.",
            ("after quiz", "quiz complete", "submit quiz"): "• Click 'Finish Attempt', review answers, and submit.",
            ("retake quiz", "redo quiz"): "• This depends on the instructor’s settings.",
            ("quiz results", "check score", "quiz marks"): "• You may see scores immediately or once results are released.",
            ("forgot password", "reset password"): "• Use 'Forgot Password' on the login page and follow the steps.",
            ("not see course", "course missing", "course not showing"): "• Check your credentials or contact support.",
            ("contact support", "technical issue", "help"): "• Use the Help section or contact your instructor.",
            ("mobile", "access on phone", "can i use on phone"): "• Yes, Eduvate works on mobile browsers and may have an app.",
            ("file not appearing", "upload issue"): "• Refresh and retry. If it persists, contact support.",
            ("logout", "sign out"): "• Click your profile icon and select 'Logout'.",
            ("available courses", "list courses"): "• Available courses: Course A, Course B, Course C.",
            ("hi", "hello"): "Hello! How can I assist you today?",
            ("how are you", "how r u", "how are u"): "I'm just a bot, but I'm doing great!",
            ("what is todays date", "today date", "date today"): self.get_current_date(),
            ("bye", "goodbye"): "Goodbye! Have a great day and happy learning!",
            ("ok","thanks","tqs"): "I hope u understood it!",
            ("submit","how to submit"): "Click on submit at bottom of page to submit.",
        }

        self.faq_exact = {
            "how do i log in to eduvate?": "Enter the username and password provided and click 'Login'.",
            "where can i find the courses i have enrolled in?": "Click the menu icon, then 'My Courses'.",
            "how do i access my course content?": "Click on the course under 'My Courses' to view content.",
            "what will be available on my course page?": "You'll find syllabus, question bank, session content, and more.",
            "can i download the course materials?": "Yes, just click the activity and download.",
            "are videos available in the course?": "Yes, videos are available for learning support.",
            "how do i submit an assignment?": "Click the assignment, then 'Add Submission' to upload.",
            "what file formats are accepted for assignment submission?": "PDF, Word documents, or as specified by instructor.",
            "can i edit my assignment submission?": "Yes, before the deadline, if allowed by your instructor.",
            "how do i check if my assignment is submitted successfully?": "A confirmation or status update will be shown.",
            "how do i attend a quiz?": "Click the quiz and select 'Attempt Quiz'.",
            "what should i do after completing the quiz?": "Click 'Finish Attempt' and then submit.",
            "can i retake a quiz?": "This depends on instructor settings.",
            "how do i check my quiz results?": "Results may be available immediately or after release.",
            "i forgot my password. how can i reset it?": "Click 'Forgot Password' and follow the reset process.",
            "why can’t i see my enrolled course?": "Ensure you're logged in correctly or contact support.",
            "how do i contact support for technical issues?": "Use 'Help' on Eduvate or contact your instructor.",
            "can i access eduvate on my mobile?": "Yes, it's mobile compatible.",
            "what should i do if my uploaded file is not appearing?": "Refresh, re-upload, or contact support.",
            "how do i log out of eduvate?": "Click your profile icon and choose 'Logout'.",
            "list all available courses": "Available courses: Course A, Course B, Course C.",
            "hi": "Hello! How can I assist you today?",
            "hello": "Hi there! How can I help you?",
            "how are you?": "I'm just a bot, but I'm here and ready to help!",
            "what is todays date?": self.get_current_date(),
            "bye": "Goodbye! Have a great day and happy learning!",
            "goodbye": "Take care! See you next time on Eduvate.",
        }

        self.display_message("Eduvate Chatbot: Hi, how can I help you?")
        self.check_reminders()

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("Today is %A, %B %d, %Y.")

    def get_bot_reply(self, user_input):
        user_input = user_input.lower().strip()

        if user_input in self.faq_exact:
            return self.faq_exact[user_input]

        for keywords, response in self.faq_keywords.items():
            if any(keyword in user_input for keyword in keywords):
                return response

        return "I'm still learning! Can you rephrase that?"

    def display_message(self, message, add_timestamp=False):
        timestamp = f"[{datetime.now().strftime('%H:%M')}] " if add_timestamp else ""
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.insert(tk.END, f"{timestamp}{message}\n")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(tk.END)

    def send_message(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        self.display_message("You: " + user_input)
        self.input_entry.delete(0, tk.END)

        lower_input = user_input.lower()

        if "time plan" in lower_input:
            response = self.generate_time_plan()
        elif "dark mode" in lower_input:
            self.set_dark_mode()
            response = "Dark mode activated."
        elif "light mode" in lower_input:
            self.set_light_mode()
            response = "Light mode activated."
        elif "grades" in lower_input:
            response = "For grades, please contact your instructor with your student ID."
        elif "contact" in lower_input:
            response = "For further assistance, please contact support@eduvate.com"
        elif "set reminder" in lower_input:
            self.set_reminder()
            return
        elif "feedback" in lower_input:
            self.get_feedback()
            return
        elif "edit mode on" in lower_input:
            self.edit_mode = True
            response = "Edit mode is now ON."
        elif "edit mode off" in lower_input:
            self.edit_mode = False
            response = "Edit mode is now OFF."
        elif "open block drawer" in lower_input:
            self.block_drawer_open = True
            response = "Block drawer opened."
        elif "close block drawer" in lower_input:
            self.block_drawer_open = False
            response = "Block drawer closed."
        else:
            response = self.get_bot_reply(lower_input)

        self.display_message("Eduvate Chatbot: " + response)
        self.memory[lower_input] = response

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
        if not reminder_text:
            self.display_message("Eduvate Chatbot: Reminder text was not provided.")
            return

        reminder_time = simpledialog.askstring("Set Reminder", "Enter reminder time (YYYY-MM-DD HH:MM):")
        if not reminder_time:
            self.display_message("Eduvate Chatbot: Reminder time was not provided.")
            return

        try:
            reminder_datetime = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
            self.reminders.append((reminder_datetime, reminder_text))
            self.display_message(f"Eduvate Chatbot: Reminder set for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}: {reminder_text}")
        except ValueError:
            self.display_message("Eduvate Chatbot: Invalid time format. Please use YYYY-MM-DD HH:MM.")

    def check_reminders(self):
        now = datetime.now()
        due = [rem for rem in self.reminders if rem[0] <= now]
        for rem in due:
            self.display_message(f"Reminder: {rem[1]}")
            self.reminders.remove(rem)
        self.master.after(60000, self.check_reminders)

    def get_feedback(self):
        feedback = simpledialog.askstring("Feedback", "Enter your feedback:")
        if feedback:
            self.display_message("Eduvate Chatbot: Thank you for your feedback!")


# Run the chatbot
if __name__ == "__main__":
    root = tk.Tk()
    chatbot = Eduvate(root)
    root.mainloop()
