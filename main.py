import gradio as gr
import random
import time

phase = "start"
img_state = 1
completed_components = []

def reset_game():
    global phase, img_state, completed_components
    phase = "start"
    img_state = 1
    completed_components = []
    
    intro = [{"role": "assistant", "content": "Hi, I'm CoAura, NASA's SOS Response Agent. A system component may be acting up. How would you like to start?"}]
    return intro, gr.update(choices=["Run a system scan", "Ignore for now"], value=None)

def progress(choice, chat):
    global phase, img_state, completed_components
    
    if not choice:
        chat.append({"role":"assistant","content":"Please choose an option so I can continue."})
        return chat, gr.update()
    
    chat.append({"role":"user","content":choice})
    time.sleep(random.uniform(0.5, 1.0))
    
    if phase == "start":
        if choice == "Run a system scan":
            available = [c for c in ["O2", "Cooling", "Power"] if c not in completed_components]
            if not available:
                reply = "All systems operational! Mission complete. Restart to play again."
                options, phase = ["Restart"], "end"
            else:
                component = random.choice(available)
                if component == "O2":
                    img_state = 2
                    reply = "Scan complete — oxygen system is unstable. What should we do?"
                    options = ["Attempt manual valve adjustment", "Reroute backup oxygen supply"]
                    phase = "o2_choice1"
                elif component == "Cooling":
                    img_state = 3
                    reply = "Scan complete — cooling system temperature is abnormal. What next?"
                    options = ["Increase coolant flow rate", "Switch to backup cooling loop"]
                    phase = "cooling_choice1"
                else:
                    img_state = 4
                    reply = "Scan complete — power fluctuation detected. Choose a response:"
                    options = ["Stabilize main voltage regulator", "Reroute to auxiliary power"]
                    phase = "power_choice1"
        elif choice == "Ignore for now":
            reply = "Ignoring the issue made things worse. What should we do now?"
            options = ["Run a system scan", "Reboot subsystem"]
        elif choice == "Reboot subsystem":
            reply = "Reboot failed to resolve the issue. Try scanning the system."
            options = ["Run a system scan"]
        else:
            reply = "I didn't quite understand that."
            options = ["Run a system scan", "Ignore for now"]
    
    elif phase == "o2_choice1":
        reply = "How should we proceed?"
        phase = "o2_choice2"
        options = ["Open emergency vent slowly", "Close primary intake valve"] if choice == "Attempt manual valve adjustment" else ["Activate redundant oxygen tank", "Purge main O2 line"]
    
    elif phase == "o2_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"'{choice}' worked! Oxygen system stabilized."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("O2")
        else:
            img_state = 7
            reply = f"'{choice}' failed — catastrophic oxygen failure."
            phase = "end"
            options = ["Restart"]
    
    elif phase == "cooling_choice1":
        reply = "Next action:"
        phase = "cooling_choice2"
        options = ["Gradually raise pump pressure", "Flush coolant reservoir"] if choice == "Increase coolant flow rate" else ["Activate secondary radiators", "Divert heat to main radiator"]
    
    elif phase == "cooling_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"'{choice}' succeeded! Temperature normalized."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Cooling")
        else:
            img_state = 7
            reply = f"'{choice}' caused thermal overload — system failure."
            phase = "end"
            options = ["Restart"]
    
    elif phase == "power_choice1":
        reply = "What now?"
        phase = "power_choice2"
        options = ["Recalibrate voltage threshold", "Bypass surge protector"] if choice == "Stabilize main voltage regulator" else ["Switch to battery backup", "Isolate faulty circuit"]
    
    elif phase == "power_choice2":
        if random.random() < 0.5:
            img_state = 5
            reply = f"'{choice}' worked! Power systems stable."
            phase = "finish"
            options = ["Continue"]
            completed_components.append("Power")
        else:
            img_state = 7
            reply = f"'{choice}' triggered cascading power failure."
            phase = "end"
            options = ["Restart"]
    
    elif phase == "finish":
        img_state = 6
        remaining = len([c for c in ["O2", "Cooling", "Power"] if c not in completed_components])
        if remaining > 0:
            reply = "System stable! But wait... detecting another issue. Scanning now..."
            phase = "start"
            options = ["Run a system scan"]
        else:
            reply = "All systems operational! Mission complete. Restart to play again."
            phase = "end"
            options = ["Restart"]
    
    elif phase == "end":
        if "restart" in choice.lower():
            return reset_game()
        reply = "Ready to restart whenever you are."
        options = ["Restart"]
    
    chat.append({"role":"assistant","content":reply})
    return chat, gr.update(choices=options, value=options[0])

with gr.Blocks() as app:
    gr.Markdown("##  CoAura — NASA's SOS Response Agent")
    chat = gr.Chatbot(type="messages", height=350)
    picks = gr.Radio([], label="Select an option")
    btn = gr.Button("Continue")
    
    app.load(reset_game, [], [chat, picks])
    btn.click(progress, [picks, chat], [chat, picks])

app.launch()
