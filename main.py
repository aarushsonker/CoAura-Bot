import gradio as gr
import random
import time
import os

# --- Game State ---
phase = "mode_select"
img_state = 1
completed_components = []
mode = None  # Track which mode the user selected
trivia_score = 0
trivia_questions_asked = 0
trivia_category = None

# --- Trivia Questions Database ---
TRIVIA_QUESTIONS = {
    "Space": [
        {
            "question": "What is the largest planet in our solar system?",
            "options": ["Mars", "Jupiter", "Saturn", "Neptune"],
            "correct": 1
        },
        {
            "question": "How long does it take for light from the Sun to reach Earth?",
            "options": ["8 seconds", "8 minutes", "8 hours", "8 days"],
            "correct": 1
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Venus", "Mars", "Mercury", "Jupiter"],
            "correct": 1
        },
        {
            "question": "What is the name of Earth's only natural satellite?",
            "options": ["Phobos", "Titan", "The Moon", "Europa"],
            "correct": 2
        },
        {
            "question": "How many planets are in our solar system?",
            "options": ["7", "8", "9", "10"],
            "correct": 1
        }
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H2O", "CO2", "O2", "HO"],
            "correct": 0
        },
        {
            "question": "What is the speed of light in vacuum?",
            "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "200,000 km/s"],
            "correct": 0
        },
        {
            "question": "What is the smallest unit of matter?",
            "options": ["Molecule", "Cell", "Atom", "Electron"],
            "correct": 2
        },
        {
            "question": "Which gas do plants absorb from the atmosphere?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
            "correct": 2
        },
        {
            "question": "What is the hardest natural substance on Earth?",
            "options": ["Gold", "Iron", "Diamond", "Titanium"],
            "correct": 2
        }
    ],
    "NASA History": [
        {
            "question": "In what year did NASA land the first humans on the Moon?",
            "options": ["1965", "1967", "1969", "1971"],
            "correct": 2
        },
        {
            "question": "What was the name of the first space shuttle?",
            "options": ["Discovery", "Challenger", "Enterprise", "Columbia"],
            "correct": 2
        },
        {
            "question": "Who was the first American in space?",
            "options": ["Neil Armstrong", "Buzz Aldrin", "Alan Shepard", "John Glenn"],
            "correct": 2
        },
        {
            "question": "What does ISS stand for?",
            "options": ["International Space Station", "Interstellar Space Ship", "International Satellite System", "Inner Solar System"],
            "correct": 0
        },
        {
            "question": "Which Apollo mission was the first to land on the Moon?",
            "options": ["Apollo 8", "Apollo 10", "Apollo 11", "Apollo 13"],
            "correct": 2
        }
    ]
}

# --- Image Helper ---
def get_image_path(state):
    return os.path.join("images", f"{state}.png")

# --- Game Logic ---
def reset_game():
    """Resets the game to its initial state."""
    global phase, img_state, completed_components, mode, trivia_score, trivia_questions_asked, trivia_category
    phase = "mode_select"
    img_state = 1
    completed_components = []
    mode = None
    trivia_score = 0
    trivia_questions_asked = 0
    trivia_category = None
    intro = [{"role": "assistant", "content": "Hello, Commander. I'm CoAura, your AI assistant. How can I help you today?"}]
    return intro, gr.update(choices=["Emergency Simulation Mode", "Trivia Game Mode"], value=None), get_image_path(img_state)

def progress(choice, chat):
    """Main function to handle game progress and UI updates."""
    global phase, img_state, completed_components, mode, trivia_score, trivia_questions_asked, trivia_category

    if not choice:
        chat.append({"role": "assistant", "content": "Commander, I need your input to proceed. Please select an option."})
        # CRITICAL CHANGE: The function must always return a value for the image component
        return chat, gr.update(), get_image_path(img_state)

    chat.append({"role": "user", "content": choice})
    time.sleep(random.uniform(0.5, 1.0))

    # --- MODE SELECTION ---
    if phase == "mode_select":
        if choice == "Emergency Simulation Mode":
            mode = "emergency"
            phase = "start"
            reply = "Emergency mode activated. Commander, I'm detecting anomalies in the station systems. We need to address this immediately. Shall I run a full diagnostic scan?"
            options = ["Run a system scan", "Ignore for now"]
        elif choice == "Trivia Game Mode":
            mode = "trivia"
            phase = "trivia_select_category"
            img_state = 6
            reply = f"🎮 Welcome to Space Trivia, Commander! Test your knowledge across different categories. Choose a category to begin:"
            options = ["Space", "Science", "NASA History"]
        else:
            reply = "Please select a mode to continue."
            options = ["Emergency Simulation Mode", "Trivia Game Mode"]
    
    # --- TRIVIA GAME MODE ---
    elif phase == "trivia_select_category":
        if choice in ["Space", "Science", "NASA History"]:
            trivia_category = choice
            trivia_score = 0
            trivia_questions_asked = 0
            phase = "trivia_playing"
            # Get first question
            question_data = random.choice(TRIVIA_QUESTIONS[trivia_category])
            reply = f"📚 Category: {trivia_category}\n\nQuestion 1:\n{question_data['question']}"
            options = question_data['options']
        else:
            reply = "Please select a valid category."
            options = ["Space", "Science", "NASA History"]
    
    elif phase == "trivia_playing":
        # Find the question that was just asked (last assistant message)
        last_question = None
        for msg in reversed(chat):
            if msg["role"] == "assistant" and "Question" in msg["content"]:
                # Extract question text
                question_text = msg["content"].split("\n")[-1]
                # Find matching question
                for q in TRIVIA_QUESTIONS[trivia_category]:
                    if q["question"] in question_text:
                        last_question = q
                        break
                break
        
        if last_question:
            # Check if answer is correct
            correct_answer = last_question['options'][last_question['correct']]
            if choice == correct_answer:
                trivia_score += 1
                reply = f"✅ Correct! The answer is {correct_answer}.\n\n"
            else:
                reply = f"❌ Incorrect. The correct answer was {correct_answer}.\n\n"
            
            trivia_questions_asked += 1
            
            # Check if game should continue
            if trivia_questions_asked >= 5:
                img_state = 5 if trivia_score >= 3 else 1
                reply += f"🎮 Game Over!\n\nFinal Score: {trivia_score}/5\n\n"
                if trivia_score == 5:
                    reply += "Perfect score, Commander! Outstanding knowledge! 🌟"
                elif trivia_score >= 3:
                    reply += "Great job, Commander! You know your stuff! 🚀"
                else:
                    reply += "Keep learning, Commander! Try again to improve your score! 📚"
                options = ["Play Again", "Change Category", "Back to Main Menu"]
                phase = "trivia_end"
            else:
                # Get next question
                question_data = random.choice(TRIVIA_QUESTIONS[trivia_category])
                reply += f"Score: {trivia_score}/{trivia_questions_asked}\n\nQuestion {trivia_questions_asked + 1}:\n{question_data['question']}"
                options = question_data['options']
        else:
            reply = "Error processing your answer. Let's continue."
            options = ["Back to Main Menu"]
    
    elif phase == "trivia_end":
        if choice == "Play Again":
            trivia_score = 0
            trivia_questions_asked = 0
            phase = "trivia_playing"
            img_state = 6
            # Get first question
            question_data = random.choice(TRIVIA_QUESTIONS[trivia_category])
            reply = f"📚 Category: {trivia_category}\n\nQuestion 1:\n{question_data['question']}"
            options = question_data['options']
        elif choice == "Change Category":
            phase = "trivia_select_category"
            img_state = 6
            reply = "Choose a new category:"
            options = ["Space", "Science", "NASA History"]
        elif choice == "Back to Main Menu":
            phase = "mode_select"
            img_state = 1
            reply = "Returning to main menu. What would you like to do next, Commander?"
            options = ["Emergency Simulation Mode", "Trivia Game Mode"]
        else:
            reply = "What would you like to do?"
            options = ["Play Again", "Change Category", "Back to Main Menu"]
    elif phase == "start":
        if choice == "Run a system scan":
            available = [c for c in ["O2", "Cooling", "Power"] if c not in completed_components]
            if not available:
                reply = "Excellent work, Commander! All critical systems are now functioning normally. The station is secure. Would you like to run another simulation?"
                options, phase = ["Restart"], "end"
            else:
                component = random.choice(available)
                if component == "O2":
                    img_state = 2
                    reply = "Commander, I've identified a critical oxygen system failure. Life support is compromised. I'm showing you two repair protocols — which approach do you want me to guide you through?"
                    options = ["Attempt manual valve adjustment", "Reroute backup oxygen supply"]
                    phase = "o2_choice1"
                elif component == "Cooling":
                    img_state = 3
                    reply = "Commander, the thermal management system is overheating. We're approaching dangerous temperature levels. I have two stabilization procedures available — which one should we try?"
                    options = ["Increase coolant flow rate", "Switch to backup cooling loop"]
                    phase = "cooling_choice1"
                else:
                    img_state = 4
                    reply = "Commander, we have a power grid instability. Multiple systems are at risk. I can guide you through two emergency protocols — which would you prefer?"
                    options = ["Stabilize main voltage regulator", "Reroute to auxiliary power"]
                    phase = "power_choice1"
        elif choice == "Ignore for now":
            reply = "Commander, I must advise against ignoring this. The situation is deteriorating rapidly. We need to take action now. What's your decision?"
            options = ["Run a system scan", "Reboot subsystem"]
        elif choice == "Reboot subsystem":
            reply = "The reboot attempt didn't resolve the issue, Commander. The problem is more serious than anticipated. I recommend running a full diagnostic immediately."
            options = ["Run a system scan"]
        else:
            reply = "I didn't catch that, Commander. Could you clarify your instructions?"
            options = ["Run a system scan", "Ignore for now"]

    elif phase == "o2_choice1":
        reply = "Good choice, Commander. Now, I'm walking you through the procedure. Which specific action should I help you execute?"
        phase = "o2_choice2"
        options = ["Open emergency vent slowly", "Close primary intake valve"] if choice == "Attempt manual valve adjustment" else ["Activate redundant oxygen tank", "Purge main O2 line"]

    elif phase == "o2_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Perfect execution, Commander! Your '{choice}' maneuver worked. Oxygen levels are returning to normal. Life support is stable."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("O2")
        else:
            img_state = 7
            reply = f"Commander, no! The '{choice}' procedure caused a cascade failure. I'm detecting rapid decompression. We've lost life support. I'm sorry, Commander..."
            phase = "end"
            options = ["Restart"]

    elif phase == "cooling_choice1":
        reply = "Understood, Commander. I'm configuring that now. What's your next step?"
        phase = "cooling_choice2"
        options = ["Gradually raise pump pressure", "Flush coolant reservoir"] if choice == "Increase coolant flow rate" else ["Activate secondary radiators", "Divert heat to main radiator"]

    elif phase == "cooling_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Excellent work, Commander! Your '{choice}' procedure was successful. Temperature readings are normalizing. The cooling system is back online."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Cooling")
        else:
            img_state = 7
            reply = f"Commander, we have a problem! The '{choice}' caused a thermal runaway. Critical systems are overheating. I'm losing control..."
            phase = "end"
            options = ["Restart"]

    elif phase == "power_choice1":
        reply = "On it, Commander. I'm preparing the power systems. Which final step should I execute?"
        phase = "power_choice2"
        options = ["Recalibrate voltage threshold", "Bypass surge protector"] if choice == "Stabilize main voltage regulator" else ["Switch to battery backup", "Isolate faulty circuit"]

    elif phase == "power_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"Outstanding, Commander! Your '{choice}' decision restored power stability. All systems are drawing clean energy. Grid is secure."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Power")
        else:
            img_state = 7
            reply = f"Commander, abort! The '{choice}' triggered a massive surge. I'm losing power to all— [CONNECTION LOST]"
            phase = "end"
            options = ["Restart"]

    elif phase == "finish":
        remaining = len([c for c in ["O2", "Cooling", "Power"] if c not in completed_components])
        if remaining > 0:
            reply = "Great work, Commander! That system is stable now. But... hold on, I'm detecting another critical alert. We need to move fast. Running diagnostics..."
            phase = "start"
            options = ["Run a system scan"]
        else:
            reply = "Excellent work, Commander! All critical systems are now functioning normally. The station is secure. Would you like to run another simulation?"
            phase = "end"
            options = ["Restart"]

    elif phase == "end":
        if "restart" in choice.lower():
            # CRITICAL CHANGE: The reset function now returns 3 values
            return reset_game()
        reply = "I'm standing by, Commander. Ready to assist when you need me."
        options = ["Restart"]

    chat.append({"role": "assistant", "content": reply})
    # CRITICAL CHANGE: Notice it now returns the image path at the end
    return chat, gr.update(choices=options, value=options[0] if options else None), get_image_path(img_state)


# --- UI Layout ---
# Custom CSS for space theme
custom_css = """
body {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0f0f1e 100%);
}
.gradio-container {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0f0f1e 100%) !important;
    background-attachment: fixed !important;
}
.contain {
    background: rgba(10, 14, 39, 0.8) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(100, 150, 255, 0.3);
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
h2, h1 {
    color: #00d9ff !important;
    text-shadow: 0 0 10px rgba(0, 217, 255, 0.5), 0 0 20px rgba(0, 217, 255, 0.3);
    font-family: 'Courier New', monospace;
    text-align: center;
}
.message-row {
    background: rgba(15, 15, 30, 0.6) !important;
    border: 1px solid rgba(100, 150, 255, 0.2);
}
button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: 2px solid #00d9ff !important;
    color: white !important;
    font-weight: bold !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px 0 rgba(102, 126, 234, 0.4);
}
button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px 0 rgba(0, 217, 255, 0.6);
    border-color: #00ffff !important;
}
.radio-item {
    background: rgba(15, 15, 30, 0.8) !important;
    border: 2px solid rgba(100, 150, 255, 0.3) !important;
    color: #00d9ff !important;
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
    transition: all 0.3s ease;
}
.radio-item:hover {
    border-color: #00ffff !important;
    background: rgba(0, 217, 255, 0.1) !important;
    transform: translateX(5px);
}
label {
    color: #00d9ff !important;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9em;
}
.image-container {
    border: 2px solid #00d9ff;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
}
.chatbot {
    background: rgba(10, 14, 39, 0.8) !important;
    border: 2px solid rgba(100, 150, 255, 0.3);
    border-radius: 15px;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:
    gr.Markdown("""
    # 🚀 CoAura — NASA's SOS Response Agent
    ### *Your AI Companion for Space Missions*
    """)
    
    # THIS IS THE NEW LAYOUT CODE
    with gr.Row():
        with gr.Column(scale=1):
            # This is the new Image component on the left
            img = gr.Image(value=get_image_path(img_state), label="🛸 Spaceship Status", show_label=True, interactive=False, elem_classes="image-container")
        with gr.Column(scale=2):
            # This is your chat interface on the right
            chat = gr.Chatbot(type="messages", height=550, elem_classes="chatbot")
            picks = gr.Radio([], label="⚡ Select an option")
            btn = gr.Button("🚀 Continue")

    # --- Event Handling ---
    # CRITICAL CHANGE: The 'outputs' list for the functions now includes the 'img' component
    app.load(reset_game, [], [chat, picks, img])
    btn.click(progress, [picks, chat], [chat, picks, img])

app.launch()
