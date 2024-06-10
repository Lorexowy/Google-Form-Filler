import tkinter as tk
from tkinter import simpledialog, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def fill_form(driver, form_url):
    driver.get(form_url)
    time.sleep(5)  # Czekaj

    filled_first_text_input = False

    while True:
        try:
            # Tekst
            text_inputs = driver.find_elements(By.XPATH, '//input[@type="text"]')
            for input_box in text_inputs:
                if not filled_first_text_input:
                    input_box.send_keys("Polska")
                    filled_first_text_input = True
                time.sleep(0.1)  # Opóźnienie

            # Radiobuttons
            radio_groups = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]')
            for radio_group in radio_groups:
                options = radio_group.find_elements(By.XPATH, './/div[@role="radio"]')
                if options:
                    random.choice(options).click()
                    time.sleep(0.1)  # Opóźnienie

            # Checkboxy
            checkbox_groups = driver.find_elements(By.XPATH, '//div[contains(@class, "eBFwI") and not(contains(@class, "RVLOe"))]')
            for checkbox_group in checkbox_groups:
                checkboxes = checkbox_group.find_elements(By.XPATH, './/div[@role="checkbox"]')
                for checkbox in checkboxes:
                    label_element = checkbox.find_element(By.XPATH, '..')
                    label = label_element.text.strip()
                    if label and random.choice([True, False]):  # Losowy
                        checkbox.click()
                        time.sleep(0.1)  # Opóźnienie
                        print(f"Clicked checkbox: {label}")

            # Skala
            scale_questions = driver.find_elements(By.XPATH, '//div[@role="radiogroup"]//div[@data-value]')
            for scale_question in scale_questions:
                options = scale_question.find_elements(By.XPATH, './/div[@role="radio"]')
                if options:
                    random.choice(options).click()
                    time.sleep(0.1)  # Opóźnienie
                    print(f"Clicked scale option: {options[random.randint(0, len(options) - 1)].get_attribute('aria-label')}")

            # Dalej
            next_button = driver.find_elements(By.XPATH, '//span[contains(text(), "Dalej") or contains(text(), "Next")]')
            if next_button:
                next_button[0].click()
                time.sleep(0.5)  # Czekaj
            else:
                break  # Koniec

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    try:
        # Prześlij
        submit_button = driver.find_element(By.XPATH, '//span[contains(text(), "Prześlij") or contains(text(), "Submit")]')
        submit_button.click()
        time.sleep(0.5)  # Czekaj
    except Exception as e:
        print(f"An error occurred while submitting the form: {e}")

def main(form_url, repetitions):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        for _ in range(repetitions):  # Powtórzenia
            fill_form(driver, form_url)
            time.sleep(0.5)  # Czekaj
    finally:
        driver.quit()

    # Wyświetl okno dialogowe z informacją o zakończeniu pracy
    root = tk.Tk()
    root.withdraw()  # Ukryj główne okno
    messagebox.showinfo("Completion", f"Surveys have been filled {repetitions} times. Thank you! :-)")

def start_gui():
    root = tk.Tk()
    root.withdraw()  # Ukryj główne okno

    form_url = simpledialog.askstring("Input", "Please enter the Google Form URL:", parent=root)
    repetitions = simpledialog.askinteger("Input", "Please enter the number of repetitions:\n\n1-100", parent=root, minvalue=1, maxvalue=100)

    if form_url and repetitions:
        disclaimer_text = ("Disclaimer: I understand that using this program does not provide real scientific results. "
                           "Using this program for scientific surveys is not recommended. For "
                           "educational purposes only.\n\nCreated and coded by www.mateuszmichel.com")
        messagebox.showinfo("Disclaimer", disclaimer_text)
        main(form_url, repetitions)

if __name__ == "__main__":
    start_gui()
