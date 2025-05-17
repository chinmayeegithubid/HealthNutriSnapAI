<p align="center">
  <img src="https://github.com/chinmayeegithubid/HealthNutriSnapAI/blob/main/logo.png" width="200" alt="HealthNutriSnapAI Logo">
</p>


# 🥗 HealthNutriSnapAI

**AI-powered food calorie and nutrition analyzer using Gemini 1.5 & Streamlit**

HealthNutriSnapAI helps users:
- 🧠 Estimate food calories from images
- 📊 Analyze nutritional breakdown (carbs, proteins, fats, etc.)
- 🩺 Get health assessments and AI-generated diet suggestions
- 🗓️ Generate daily, weekly, monthly diet plans tailored to goals
- 🎙️ Includes voice assistant and webcam-based scanning!

---

## 🚀 Features

- 📷 Upload or capture food images using webcam
- 🔍 AI-powered calorie and nutrition estimation
- 📈 Nutrition history tracking (CSV log)
- 💡 GPT-based health Q&A assistant
- 🧑‍⚕️ Daily/weekly/monthly doctor advice plan
- 📥 Export scan reports
- 🔐 .env used for API key security

---

## 📦 Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/chinmayeegithubid/HealthNutriSnapAI.git
   cd HealthNutriSnapAI
2. Create & activate virtual environment (optional but recommended):

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On Mac/Linux
3. Install dependencies:
pip install -r requirements.txt
✅ Step 3: Run the App
4. Run the Streamlit app:

```bash
streamlit run app.py
✅ Step 4: Directory Structure
## 📁 Directory Structure

.
├── app.py
├── requirements.txt
├── nutrition_history.csv
├── .env
└── .gitignore

---

### ✅ Step 5: License (Mention only)

```markdown
## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
✅ Step 6: Acknowledgements
## 🙏 Acknowledgements

- Google Gemini 1.5 Flash API
- Streamlit team for a simple UI framework
- Inspiration from daily health struggles and personal learning journey
