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
    
    intro = [{"role": "assistant", "content": "Commander, this is CoAura. I'm detecting anomalies in the station systems. We need to address this immediately. Shall I run a full diagnostic scan?"}]
    return intro, gr.update(choices=["Run a system scan", "Ignore for now"], value=None)

def progress(choice, chat):
    global phase, img_state, completed_components
    
    if not choice:
        chat.append({"role":"assistant","content":"Commander, I need your input to proceed. Please select an option."})
        return chat, gr.update()
    
    chat.append({"role":"user","content":choice})
    time.sleep(random.uniform(0.5, 1.0))
    
    if phase == "start":
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
        img_state = 6
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
            return reset_game()
        reply = "I'm standing by, Commander. Ready to assist when you need me."
        options = ["Restart"]
    
    chat.append({"role":"assistant","content":reply})
    return chat, gr.update(choices=options, value=options[0])

with gr.Blocks() as app:
    gr.Markdown("##  CoAura — NASA's SOS Response Agent")
    chat = gr.Chatbot(type="messages", height=550)
    picks = gr.Radio([], label="Select an option")
    btn = gr.Button("Continue")
    
    app.load(reset_game, [], [chat, picks])
    btn.click(progress, [picks, chat], [chat, picks])

app.launch()
