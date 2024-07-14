import tkinter as tk
from tkinter import messagebox, ttk
import string
import secrets
import pyperclip

def check_password_strength(password):
    strength = 0
    remarks = ''
    lower_count = upper_count = num_count = wspace_count = special_count = 0

    for char in list(password):
        if char in string.ascii_lowercase:
            lower_count += 1
        elif char in string.ascii_uppercase:
            upper_count += 1
        elif char in string.digits:
            num_count += 1
        elif char == ' ':
            wspace_count += 1
        else:
            special_count += 1

    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 2

    # Determine remarks based on password strength
    if strength == 1:
        remarks = 'That\'s a very bad password. Change it as soon as possible.'
    elif strength == 2:
        remarks = 'That\'s a weak password. You should consider using a tougher password.'
    elif strength == 3:
        remarks = 'Your password is okay, but it can be improved.'
    elif strength == 4:
        remarks = 'Your password is hard to guess. But you could make it even more secure.'
    elif strength == 5:
        remarks = 'Now that\'s one hell of a strong password!!! Hackers don\'t have a chance guessing that password!'

    result = f'Password Score: {strength}/5\nRemarks: {remarks}'
    return result, strength

def check_password():
    password = password_entry.get()
    result, strength = check_password_strength(password)

    # Update output text
    output_text.config(state='normal')
    output_text.delete('1.0', 'end')
    output_text.insert('end', result)
    output_text.config(state='disabled')

    # Define custom styles for each strength level
    style_low = ttk.Style()
    style_low.configure("low.Horizontal.TProgressbar", foreground='#ff4d4d')  # Red

    style_medium = ttk.Style()
    style_medium.configure("medium.Horizontal.TProgressbar", foreground='#ffd700')  # Yellow

    style_strong = ttk.Style()
    style_strong.configure("strong.Horizontal.TProgressbar", foreground='#32cd32')  # Green

    style_very_strong = ttk.Style()
    style_very_strong.configure("very-strong.Horizontal.TProgressbar", foreground='#1e90ff')  # Blue

    # Update progress bar style based on password strength
    if strength == 1:
        strength_meter["style"] = "low.Horizontal.TProgressbar"
    elif strength == 2:
        strength_meter["style"] = "medium.Horizontal.TProgressbar"
    elif strength in [3, 4]:
        strength_meter["style"] = "strong.Horizontal.TProgressbar"
    elif strength == 5:
        strength_meter["style"] = "very-strong.Horizontal.TProgressbar"

    # Update progress bar value based on password strength
    animate_progress_bar(strength_meter, strength * 20, 0)

def animate_progress_bar(progress_bar, target_value, current_value):
    if current_value < target_value:
        current_value += 1
        progress_bar["value"] = current_value
        progress_bar.after(10, animate_progress_bar, progress_bar, target_value, current_value)

def generate_password():
    password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
    password_entry.delete(0, 'end')
    password_entry.insert('end', password)

def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Password Copied", "Password copied to clipboard successfully!")
    else:
        messagebox.showwarning("No Password", "No password to copy!")

def clear_input():
    password_entry.delete(0, 'end')

def toggle_password_visibility():
    current_state = password_entry.cget("show")
    if current_state == "*":
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = tk.Tk()
root.title("Kami Password Checker")
root.geometry("650x400")

frame = tk.Frame(root, bg="#0a0a23")  # Dark blue background
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label = tk.Label(frame, text="Enter the password:", bg="#0a0a23", fg="white", font=("Arial", 14))
label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

check_button = tk.Button(frame, text="Check", command=check_password, bg="#1f8fff", fg="white", font=("Arial", 12))
check_button.grid(row=1, column=0, pady=10, padx=5, sticky="we")

generate_button = tk.Button(frame, text="Generate Password", command=generate_password, bg="#17b978", fg="white",
                            font=("Arial", 12))
generate_button.grid(row=1, column=1, pady=10, padx=5, sticky="we")

view_button = tk.Button(frame, text="View Password", command=toggle_password_visibility, bg="#8a2be2", fg="white",
                        font=("Arial", 12))
view_button.grid(row=1, column=2, pady=10, padx=5, sticky="we")

clear_button = tk.Button(frame, text="Clear", command=clear_input, bg="#ff6347", fg="white", font=("Arial", 12))
clear_button.grid(row=1, column=3, pady=10, padx=5, sticky="we")

output_text = tk.Text(frame, height=10, width=60, state='disabled', font=("Arial", 10))
output_text.grid(row=2, column=0, columnspan=4, pady=10)

# Initialize progress bar with a style
strength_meter = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=450, mode='determinate', value=0,
                                style="low.Horizontal.TProgressbar")
strength_meter.grid(row=3, column=0, columnspan=4, pady=12)

password_entry.bind("<KeyRelease>", lambda event: check_password())

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
