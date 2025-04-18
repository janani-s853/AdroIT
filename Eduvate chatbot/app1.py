from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os

app = Flask(__name__)

def get_current_date():
    return datetime.now().strftime("Today is %A, %B %d, %Y.")

faq_exact = {
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
    "what is todays date?": get_current_date(),
    "bye": "Goodbye! Have a great day and happy learning!",
    "goodbye": "Take care! See you next time on Eduvate.",
}

faq_keywords = {
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
    ("what is todays date", "today date", "date today"): get_current_date(),
    ("bye", "goodbye"): "Goodbye! Have a great day and happy learning!",
    ("ok", "thanks", "tqs"): "I hope u understood it!",
    ("submit", "how to submit"): "Click on submit at bottom of page to submit.",
}

def get_bot_reply(user_input):
    user_input = user_input.lower().strip()
    if user_input in faq_exact:
        return faq_exact[user_input]
    for keywords, response in faq_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return response
    return "I'm still learning! Can you rephrase that?"

@app.route("/")
def index():
    return send_from_directory(".", "index1.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = get_bot_reply(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(port=3000, debug=True)
