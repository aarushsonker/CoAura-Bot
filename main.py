import gradio as gr
import random

# --- system state ---
phase = "start"
system_health = 100
img_state = 1
current_component = None  # Track which component is active

def reset_game():
    global phase, system_health, img_state, current_component
    phase = "start"
    system_health = 100
    img_state = 1
    current_component = None

    intro = [{
        "role": "assistant",
        "content": "Hi, I'm CoAura. One of the system components may be acting up. How would you like to start?"
    }]
    options = ["Run a system scan", "Ignore for now"]
    return intro, gr.update(choices=options, value=None)

def progress(choice, chat):
    global phase, system_health, img_state, current_component

    if not choice:
        chat.append({"role":"assistant","content":"Please choose an option so I can continue."})
        return chat, gr.update()

    chat.append({"role":"user","content":choice})

    # system failsafe
    if system_health <= 0 and phase != "end":
        chat.append({"role":"assistant","content":"The system could not recover. Restart when ready."})
        phase = "end"
        return chat, gr.update(choices=["Restart"], value="Restart")

    # --- INITIAL SCAN ---
    if phase == "start":
        if choice == "Run a system scan":
            current_component = random.choice(["O2", "Cooling", "Power"])
            
            if current_component == "O2":
                img_state = 2
                reply = "Scan complete — oxygen system is unstable. What should we do?"
                options = ["Attempt manual valve adjustment", "Reroute backup oxygen supply"]
                phase = "o2_choice1"

            elif current_component == "Cooling":
                img_state = 3
                reply = "Scan complete — cooling system temperature is abnormal. What next?"
                options = ["Increase coolant flow rate", "Switch to backup cooling loop"]
                phase = "cooling_choice1"

            else:  # Power
                img_state = 4
                reply = "Scan complete — power fluctuation detected. Choose a response:"
                options = ["Stabilize main voltage regulator", "Reroute to auxiliary power"]
                phase = "power_choice1"

        elif choice == "Ignore for now":
            system_health -= 25
            reply = "Ignoring the issue made things worse. What should we do now?"
            options = ["Run a system scan", "Reboot subsystem"]
        else:
            reply = "I didn't quite understand that."
            options = []

    # ---- OXYGEN: First Choice ----
    elif phase == "o2_choice1":
        if choice == "Attempt manual valve adjustment":
            reply = "Valve access confirmed. How should we proceed?"
            options = ["Open emergency vent slowly", "Close primary intake valve"]
            phase = "o2_choice1a"
        else:  # Reroute backup
            reply = "Backup system online. Final step:"
            options = ["Activate redundant oxygen tank", "Purge main O2 line"]
            phase = "o2_choice1b"

    # ---- OXYGEN: Sub-choices (A1 = LIVE, A2 = DIE) ----
    elif phase == "o2_choice1a":
        if choice == "Open emergency vent slowly":
            img_state = 5
            reply = "Perfect! Pressure stabilized. Oxygen levels normal."
            phase = "finish"
            options = ["Continue"]
        else:  # Close primary intake
            system_health = 0
            img_state = 7
            reply = "Fatal mistake — oxygen supply cut off completely."
            phase = "end"
            options = ["Restart"]

    # ---- OXYGEN: Sub-choices (B1 = DIE, B2 = LIVE) ----
    elif phase == "o2_choice1b":
        if choice == "Activate redundant oxygen tank":
            img_state = 5
            reply = "Excellent choice! Backup O2 flowing smoothly."
            phase = "finish"
            options = ["Continue"]
        else:  # Purge main line
            system_health = 0
            img_state = 7
            reply = "Catastrophic failure — oxygen completely vented to space."
            phase = "end"
            options = ["Restart"]

    # ---- COOLING: First Choice ----
    elif phase == "cooling_choice1":
        if choice == "Increase coolant flow rate":
            reply = "Flow rate increased. Next action:"
            options = ["Gradually raise pump pressure", "Flush coolant reservoir"]
            phase = "cooling_choice1a"
        else:  # Switch to backup
            reply = "Backup loop engaging. Final step:"
            options = ["Activate secondary radiators", "Divert heat to main radiator"]
            phase = "cooling_choice1b"

    # ---- COOLING: Sub-choices ----
    elif phase == "cooling_choice1a":
        if choice == "Gradually raise pump pressure":
            img_state = 5
            reply = "Success! Temperature dropping to safe levels."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Coolant contamination detected — system overheated."
            phase = "end"
            options = ["Restart"]

    elif phase == "cooling_choice1b":
        if choice == "Activate secondary radiators":
            img_state = 5
            reply = "Perfect! Cooling systems balanced and stable."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Thermal overload — critical systems melted."
            phase = "end"
            options = ["Restart"]

    # ---- POWER: First Choice ----
    elif phase == "power_choice1":
        if choice == "Stabilize main voltage regulator":
            reply = "Regulator access granted. What now?"
            options = ["Recalibrate voltage threshold", "Bypass surge protector"]
            phase = "power_choice1a"
        else:  # Reroute to auxiliary
            reply = "Auxiliary power available. Final decision:"
            options = ["Switch to battery backup", "Isolate faulty circuit"]
            phase = "power_choice1b"

    # ---- POWER: Sub-choices ----
    elif phase == "power_choice1a":
        if choice == "Recalibrate voltage threshold":
            img_state = 5
            reply = "Voltage stabilized! Power grid operating normally."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Massive power surge — all systems fried."
            phase = "end"
            options = ["Restart"]

    elif phase == "power_choice1b":
        if choice == "Switch to battery backup":
            img_state = 5
            reply = "Smart move! Battery power maintaining all systems."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Isolation failed — cascading power failure."
            phase = "end"
            options = ["Restart"]

    # ---- Recovery state ----
    elif phase == "finish":
        img_state = 6
        reply = "Everything looks stable now. Restart?"
        phase = "end"
        options = ["Restart"]

    # ---- Restart handler ----
    elif phase == "end":
        if "restart" in choice.lower():
            return reset_game()
        reply = "Ready to restart whenever you are."
        options = ["Restart"]

    chat.append({"role":"assistant","content":reply})
    return chat, gr.update(choices=options, value=options[0])

# ---- UI ----
with gr.Blocks() as app:
    gr.Markdown("## 🤖 CoAura — NASA SOS BOT")
    chat = gr.Chatbot(type="messages", height=350)
    picks = gr.Radio([], label="Select an option")
    btn = gr.Button("Continue")

    app.load(reset_game, [], [chat, picks])
    btn.click(progress, [picks, chat], [chat, picks])

app.launch()