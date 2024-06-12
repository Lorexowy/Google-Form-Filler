import tkinter as tk
from tkinter import simpledialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import webbrowser
import logging

# Logging configuration function
def setup_logging(enable_logging):
    if enable_logging:
        logging.basicConfig(filename='form_filler.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to fill the form
def fill_form(driver, form_url, text_inputs):
    driver.get(form_url)
    time.sleep(5)  # Wait

    filled_first_text_input = False

    while True:
        try:
            if not filled_first_text_input:
                # Text input - only the first field
                text_input_element = driver.find_element(By.XPATH, '//input[@type="text"]')
                if text_inputs:
                    input_text = random.choice(text_inputs)
                    text_input_element.send_keys(input_text)
                    logging.info(f"Entered text: {input_text}")
                filled_first_text_input = True
                time.sleep(0.1)  # Delay

            # Radiobuttons
            radio_groups = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]')
            for radio_group in radio_groups:
                options = radio_group.find_elements(By.XPATH, './/div[@role="radio"]')
                if options:
                    random.choice(options).click()
                    time.sleep(0.1)  # Delay

            # Checkboxes
            checkbox_groups = driver.find_elements(By.XPATH, '//div[contains(@class, "eBFwI") and not(contains(@class, "RVLOe"))]')
            for checkbox_group in checkbox_groups:
                checkboxes = checkbox_group.find_elements(By.XPATH, './/div[@role="checkbox"]')
                for checkbox in checkboxes:
                    label_element = checkbox.find_element(By.XPATH, '..')
                    label = label_element.text.strip()
                    if label and random.choice([True, False]):  # Random
                        checkbox.click()
                        time.sleep(0.1)  # Delay
                        logging.info(f"Clicked checkbox: {label}")

            # Scale
            scale_questions = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]//div[@data-value]')
            for scale_question in scale_questions:
                options = scale_question.find_elements(By.XPATH, './/div[@role="radio"]')
                if options:
                    random.choice(options).click()
                    time.sleep(0.1)  # Delay
                    logging.info(f"Clicked scale option: {options[random.randint(0, len(options) - 1)].get_attribute('aria-label')}")

            # Dropdown
            dropdowns = driver.find_elements(By.XPATH, '//div[@role="listbox"]')
            for dropdown in dropdowns:
                dropdown.click()
                time.sleep(0.1)  # Delay
                options = dropdown.find_elements(By.XPATH, './/div[@role="option"]')
                if options:
                    random.choice(options).click()
                    time.sleep(0.1)  # Delay
                    logging.info(f"Selected dropdown option: {options[random.randint(0, len(options) - 1)].text}")

            # Next
            next_button = driver.find_elements(By.XPATH, '//span[contains(text(), "Next")]')
            if next_button:
                next_button[0].click()
                time.sleep(0.5)  # Wait
            else:
                break  # End

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break

    try:
        # Submit
        submit_button = driver.find_element(By.XPATH, '//span[contains(text(), "Submit")]')
        submit_button.click()
        time.sleep(0.5)  # Wait
    except Exception as e:
        logging.error(f"An error occurred while submitting the form: {e}")

# Main function
def main(form_url, repetitions, text_inputs, enable_logging):
    setup_logging(enable_logging)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        for _ in range(repetitions):  # Repetitions
            fill_form(driver, form_url, text_inputs)
            time.sleep(0.5)  # Wait
    finally:
        driver.quit()

    # Show completion message
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Completion", f"Surveys have been filled {repetitions} times. Thank you! :-)")

# GUI start function
def start_gui():
    def on_submit(url_entry, repetitions_entry, text_inputs_entry, log_var):
        form_url = url_entry.get()
        try:
            repetitions = int(repetitions_entry.get())
            if repetitions < 1 or repetitions > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of repetitions (1-100).")
            return

        text_inputs = text_inputs_entry.get().split(',')
        text_inputs = [text.strip() for text in text_inputs]

        enable_logging = log_var.get()

        disclaimer_text = ("Disclaimer: I understand that using this program does not provide real scientific results. "
                           "Using this program for scientific surveys is not recommended. For "
                           "educational purposes only.\n\nCreated and coded by www.mateuszmichel.com")
        messagebox.showinfo("Disclaimer", disclaimer_text)
        main(form_url, repetitions, text_inputs, enable_logging)

    def open_url(event):
        webbrowser.open_new("https://mateuszmichel.com/")

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root = tk.Tk()
    root.title("Google Random Form Filler")
    root.configure(bg='#ADD8E6')  # Blue background

    # Title
    title_label = tk.Label(root, text="Google Random Form Filler", font=("Helvetica", 16), bg='#ADD8E6')
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Label and entry for URL
    tk.Label(root, text="Google Form URL:", bg='#ADD8E6').grid(row=1, column=0, padx=10, pady=10, sticky='e')
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=1, column=1, padx=10, pady=10)

    # Label and entry for number of repetitions
    tk.Label(root, text="Number of repetitions:", bg='#ADD8E6').grid(row=2, column=0, padx=10, pady=10, sticky='e')
    repetitions_entry = tk.Entry(root, width=10)
    repetitions_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Label and entry for text inputs with example
    tk.Label(root, text="Text inputs (comma separated):", bg='#ADD8E6').grid(row=3, column=0, padx=10, pady=10, sticky='e')
    text_inputs_entry = tk.Entry(root, width=50)
    text_inputs_entry.grid(row=3, column=1, padx=10, pady=10)
    tk.Label(root, text="Example: Poland, Ireland, Germany", bg='#ADD8E6').grid(row=4, column=1, padx=10, pady=10, sticky='w')

    # Logging option
    log_var = tk.IntVar()
    log_check = tk.Checkbutton(root, text="Enable logging", variable=log_var, bg='#ADD8E6')
    log_check.grid(row=5, column=0, columnspan=2)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: on_submit(url_entry, repetitions_entry, text_inputs_entry, log_var), bg='#87CEEB')
    submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Footer text
    footer = tk.Label(root, text="created and coded by www.mateuszmichel.com", fg="blue", cursor="hand2", bg='#ADD8E6')
    footer.grid(row=7, column=0, columnspan=2, pady=10)
    footer.bind("<Button-1>", open_url)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
