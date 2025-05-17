# 🥗 HealthNutriSnapAI: Calories Advisory Application
# Developed by Chinmayee Nayak

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import re
import matplotlib.pyplot as plt
import datetime
import csv
import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3
import time
import threading

st.set_page_config(page_title="HealthNutriSnapAI", page_icon="🥗")

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Typing animation
def animated_title(text):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(f"<h1 style='text-align: center; color: #2E8B57;'>{full_text}</h1>", unsafe_allow_html=True)
        time.sleep(0.05)

animated_title("🥗 HealthNutriSnapAI")

# Safe speech function
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# File handling
def get_user_history_file():
    return "nutrition_history.csv"

def save_to_history(filename, image_name, calories, items, nutrients, assessment):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        csv.writer(file).writerow([now, image_name, calories, items, nutrients, assessment])

def load_history(filename):
    return list(csv.reader(open(filename, 'r', encoding='utf-8'))) if os.path.exists(filename) else []

# Image helpers
def is_blurry(image_pil):
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(image_cv, cv2.CV_64F).var() < 100

def input_image_setup(uploaded_file):
    return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]

# Gemini
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model.generate_content([input_prompt, image[0]]).text

# Nutrients parsing
def extract_nutrient_section(text):
    section, found = "", False
    for line in text.split("\n"):
        if any(word in line.lower() for word in ["carbohydrates", "protein", "fats", "fiber", "sugar"]):
            found = True
        if found:
            section += line + "\n"
    return section.strip()

def plot_nutrient_pie(nutrient_text):
    labels, sizes = [], []
    for line in nutrient_text.split("\n"):
        match = re.search(r"(\w+):\s*(\d+\.?\d*)", line)
        if match:
            labels.append(match.group(1))
            sizes.append(float(match.group(2)))
    if labels:
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, explode=[0.1 if x == max(sizes) else 0 for x in sizes])
        ax.axis("equal")
        ax.set_title("Nutrient Distribution")
        st.pyplot(fig)

def parse_and_display(response_text):
    st.subheader("📏 Calorie Breakdown:")
    items = re.findall(r"- ([\w\s]+)[–\-:]\s*(\d+)\s*calories", response_text)
    total_calories, lines = 0, []
    for i, (item, cal) in enumerate(items, 1):
        st.markdown(f"{i}. **{item.strip().title()}** – {cal} calories")
        total_calories += int(cal)
        lines.append(f"{item.strip().title()} - {cal} calories")
    st.subheader(f"🔥 Total Estimated Calories: **{total_calories}**")
    nutrient_section = extract_nutrient_section(response_text)
    st.subheader("📊 Nutrition Profile")
    st.markdown(nutrient_section if nutrient_section else "_No nutrient data available_")
    if nutrient_section:
        plot_nutrient_pie(nutrient_section)
    return total_calories, " | ".join(lines), nutrient_section.replace('\n', ' '), "Assessment complete"

# Sidebar
with st.sidebar:
    st.title("🥗 HealthNutriSnapAI")
    st.caption("Developed with ❤️💻 by Chinmayee Nayak")

    with st.expander("🎯 Set Nutrition Goals"):
        goal_calories = st.number_input("Daily Calorie Goal", 500, 5000, 2000)
        st.session_state["goal_calories"] = goal_calories

    with st.expander("🥗 Select Meal Plan"):
        meal_plan = st.selectbox("Choose your goal", ["General Health", "Weight Loss", "Muscle Gain", "Diabetic Friendly", "Heart Healthy"])
        st.session_state["meal_plan"] = meal_plan

    with st.expander("🤖 Ask AI for Health Suggestions"):
        question = st.text_input("Ask a question (e.g., What is a low-carb dinner?)")
        if question:
            st.markdown("**Thinking...**")
            reply = genai.GenerativeModel("gemini-1.5-flash").generate_content(question).text
            st.markdown(f"**Assistant:** {reply}")
            speak(reply[:200])  # Speak first 200 chars

# Image Upload
st.header("📷 Upload or Snap Your Food")
upload_option = st.radio("Choose input method:", ["Upload Image", "Use Webcam"])
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"]) if upload_option == "Upload Image" else st.camera_input("Take a photo")

if uploaded_file:
    image = Image.open(uploaded_file)
    if is_blurry(image):
        st.warning("⚠️ Image seems blurry. Try retaking a clearer photo.")
    st.image(image, caption="🍽️ Your Meal", use_container_width=True)

    if st.button("🔍 Analyze Calories"):
        with st.spinner("Analyzing your meal..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response("""
You are an expert AI nutritionist.

Please analyze the uploaded food image and generate a structured nutritional report in markdown format:

### 🍽️ Food Items & Estimated Calories:
- Rice – 180 calories
- Fish Fry – 200 calories
- Mixed Vegetables – 100 calories

### 🔥 Total Estimated Calories:
**480 calories**

### 📊 Nutritional Breakdown (percent of total calories):
- Carbohydrates: 55%
- Protein: 25%
- Fats: 15%
- Fiber: 3%
- Sugar: 2%

### 🩺 Health Assessment:
This is a well-balanced traditional Indian meal with lean protein and moderate carbohydrates.

Use this format strictly. If unsure, mention 'Unknown item – not estimated'.
""", image_data)

        st.header("🧠 AI Nutrition Analysis")
        st.text_area("📜 Raw Gemini Output (for debugging)", response, height=300)
        total_calories, final_items, final_nutrients, final_assessment = parse_and_display(response)
        report = f"Items: {final_items}\n\nNutrients: {final_nutrients}\n\nAssessment: {final_assessment}"
        st.download_button("💾 Download Report", report, file_name="nutrition_report.txt")
        save_to_history(get_user_history_file(), uploaded_file.name if hasattr(uploaded_file, 'name') else "camera_image", total_calories, final_items, final_nutrients, final_assessment)

# Meal Plan
st.subheader("🍽️ Personalized Meal Plan")
if "meal_plan" in st.session_state:
    prompt = f"Create a one-day {st.session_state['meal_plan'].lower()} meal plan with breakfast, lunch, dinner, snacks, and estimated calories."
    with st.spinner("Generating meal plan..."):
        result = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        st.markdown(result.text)

# Voice Assistant
st.subheader("🎤 Talk to Health Assistant")
if st.button("🎙️ Speak Now"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        try:
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            question = recognizer.recognize_google(audio_data)
            st.write("You asked:", question)
            answer = genai.GenerativeModel("gemini-1.5-flash").generate_content(question).text
            st.markdown(f"**Assistant:** {answer}")
            speak(answer[:200])
        except sr.WaitTimeoutError:
            st.warning("⏱️ Timeout. Please try again.")
        except Exception as e:
            st.error(f"Voice assistant error: {e}")

# AI Doctor Plan
st.subheader("🩺 AI Doctor Advice")
plan_type = st.radio("Select Plan Type:", ["Daily", "Weekly", "Monthly"])
if st.button("📋 Generate Health Plan"):
    with st.spinner(f"Generating your {plan_type.lower()} doctor plan..."):
        prompt = f"""
You are an AI Doctor. Generate a detailed {plan_type.lower()} health plan including:
- Diet advice
- Exercise guidance
- Hydration goals
- Stress & sleep tips
- Routine suggestions
- Lifestyle improvements
Format it in markdown with clear headers and bullets.
"""
        plan = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        st.markdown(plan.text)
        speak(plan.text[:200])

# History
with st.expander("🕘 View Your Scan History"):
    for row in reversed(load_history(get_user_history_file())):
        st.markdown(f"- **{row[0]}** | **{row[1]}** | {row[2]} cal")
        st.markdown(f"  - **Items:** {row[3]}")
        st.markdown(f"  - **Nutrients:** {row[4]}")
        st.markdown(f"  - **Assessment:** {row[5]}")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ by Chinmayee Nayak")
