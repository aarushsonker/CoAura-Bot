import gradio as gr
import random

# basic state variables
phase = "start"
system_health = 100

def reset_game():
    global phase, system_health
    phase = "start"
    system_health = 100

    first_message = [{
        "role": "assistant",
        "content": "Hello, I'm CoAura. I noticed an irregular system reading. How would you like to proceed?"
    }]
    
    options = ["Run a system check", "Ignore for now"]
    return first_message, gr.update(choices=options, value=None)

def progress(choice, history):
    global phase, system_health

    if not choice:
        history.append({"role":"assistant","content":"Please choose an option so I can continue."})
        return history, gr.update()

    history.append({"role":"user","content":choice})

    # system fail safe
    if system_health <= 0 and phase != "end":
        reply = "Something went wrong and the system couldn't recover. We can restart whenever you're ready."
        options = ["Start again"]
        phase = "end"
        history.append({"role":"assistant","content":reply})
        return history, gr.update(choices=options, value="Start again")

    # Conversation flow (not roleplaying a reactor narrative, just simple AI logic)
    if phase == "start":
        if choice == "Run a system check":
            phase = "coolant"
            reply = "Okay, I looked into it. There's a part of the system performing below expected levels. What would you like to try?"
            options = ["Attempt a fix", "Try another method"]
        elif choice == "Ignore for now":
            phase = "overheat"
            system_health -= 25
            reply = "Understood. However, leaving it unchecked has caused some issues. What should we try now?"
            options = ["Take quick action", "Contact support"]
        else:
            reply = "Hmm, I didn't understand that."
            options = []

    elif phase == "coolant":
        if choice == "Attempt a fix":
            if random.random() < 0.5:
                phase = "critical"
                system_health -= 40
                reply = "It didn’t quite work. The system is still unstable. What would you like to do next?"
                options = ["Try again", "Stop here"]
            else:
                phase = "reroute"
                reply = "Great, that helped. The system is stabilizing. Shall we continue?"
                options = ["Continue"]
        elif choice == "Try another method":
            phase = "end"
            reply = "Good thinking. That approach worked, and everything is running normally again."
            options = ["Start again"]
        else:
            reply = "I'm not sure what you meant."
            options = []

    elif phase == "overheat":
        if choice == "Take quick action":
            if random.random() < 0.3:
                system_health = 0
                reply = "The quick fix didn’t succeed and caused a failure."
            else:
                phase = "end"
                system_health -= 10
                reply = "That helped enough for now. The system is recovering."
            options = ["Start again"]
        elif choice == "Contact support":
            phase = "manual"
            system_health -= 20
            reply = "Support didn't connect. Let's try another approach."
            options = ["Manual attempt", "Shut the system down"]
        else:
            reply = "I didn’t catch that."
            options = []

    elif phase == "critical":
        if choice == "Try again":
            if random.random() < 0.6:
                phase = "reroute"
                reply = "That did the trick! Things are stabilizing."
                options = ["Continue"]
            else:
                system_health = 0
                phase = "end"
                reply = "Unfortunately, it failed again and the system shut down."
                options = ["Start again"]
        elif choice == "Stop here":
            system_health = 0
            phase = "end"
            reply = "System halted. We can restart anytime."
            options = ["Start again"]
        else:
            reply = "Can you choose one of the listed options?"
            options = []

    elif phase == "manual":
        if choice == "Manual attempt":
            if random.random() < 0.7:
                reply = "Nice — that worked. Everything is back to normal."
            else:
                system_health = 0
                reply = "The attempt didn’t succeed and caused a shutdown."
        else:
            system_health = 0
            reply = "Shutdown executed. System is offline."
        options = ["Start again"]
        phase = "end"

    elif phase == "reroute":
        reply = "Everything looks good now. Thanks for working through that with me."
        options = ["Start again"]
        phase = "end"

    elif phase == "end":
        if "start" in choice.lower():
            msgs, opts = reset_game()
            return msgs, opts

        reply = "We finished this cycle. Let me know when you're ready to begin again."
        options = ["Start again"]

    history.append({"role":"assistant","content":reply})
    return history, gr.update(choices=options, value=options[0] if options else None)


with gr.Blocks() as app:
    gr.Markdown("##  CoAura — Interactive AI Chat Companion\n### We're exploring choices together — let's begin.")
    chat = gr.Chatbot(type="messages", height=350)
    picks = gr.Radio([], label="Choose an option")
    btn = gr.Button("Continue")

    app.load(reset_game, [], [chat, picks])
    btn.click(progress, [picks, chat], [chat, picks])

app.launch()
