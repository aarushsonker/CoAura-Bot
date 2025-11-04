import gradio as gr
import random

# --- system state ---
phase = "start"
system_health = 100
img_state = 1  # reserved for future component indicators

# img_state reference (future visual system)
# 1 = System normal / stable
# 2 = Oxygen system issue
# 3 = Cooling system issue
# 4 = Power system issue
# 5 = System recovering / repair successful
# 7 = Critical failure / shutdown

# (State 6 removed — same meaning as 1)


def reset_game():
    global phase, system_health, img_state
    phase = "start"
    system_health = 100
    img_state = 1

    intro = [{
        "role": "assistant",
        "content": "Hi, I'm CoAura. One of the system components may be acting up. How would you like to start?"
    }]
    options = ["Run a system scan", "Ignore for now"]
    return intro, gr.update(choices=options, value=None)

def progress(choice, chat):
    global phase, system_health, img_state

    if not choice:
        chat.append({"role":"assistant","content":"Please choose an option so I can continue."})
        return chat, gr.update()

    chat.append({"role":"user","content":choice})

    # system failsafe
    if system_health <= 0 and phase != "end":
        chat.append({"role":"assistant","content":"The system could not recover. Restart when ready."})
        phase = "end"
        return chat, gr.update(choices=["Restart"], value="Restart")

    # --- flow ---
    if phase == "start":
        if choice == "Run a system scan":
            component = random.choice(["O2", "Cooling", "Power"])
            
            if component == "O2":
                img_state = 2
                reply = "Scan complete — oxygen system is unstable. What should we do?"
                options = ["Attempt repair", "Reroute backup oxygen"]
                phase = "o2"

            elif component == "Cooling":
                img_state = 3
                reply = "Scan complete — cooling system temperature is abnormal. What next?"
                options = ["Increase coolant flow", "Switch to backup cooling"]
                phase = "cooling"

            else:  # Power
                img_state = 4
                reply = "Scan complete — power fluctuation detected. Choose a response:"
                options = ["Stabilize voltage", "Reroute power"]
                phase = "power"

        elif choice == "Ignore for now":
            system_health -= 25
            reply = "Ignoring the issue made things worse. What should we do now?"
            options = ["Run a system scan", "Reboot subsystem"]
        
        else:
            reply = "I didn't quite understand that."
            options = []

    # ---- Oxygen component ----
    elif phase == "o2":
        if random.random() < 0.5:
            img_state = 5
            reply = "Good call — oxygen levels stabilizing."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Repair failed — oxygen system collapsed."
            options = ["Restart"]
            phase = "end"

    # ---- Cooling system ----
    elif phase == "cooling":
        if random.random() < 0.5:
            img_state = 5
            reply = "Cooling stabilized. Temperature returning to safe levels."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Cooling intervention failed — system overheated."
            options = ["Restart"]
            phase = "end"

    # ---- Power system ----
    elif phase == "power":
        if random.random() < 0.5:
            img_state = 5
            reply = "Power grid stabilized. System normal again."
            phase = "finish"
            options = ["Continue"]
        else:
            system_health = 0
            img_state = 7
            reply = "Voltage spike — power system crashed."
            options = ["Restart"]
            phase = "end"

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
