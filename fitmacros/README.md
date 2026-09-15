# 🥗 FitMacros — Smart Nutrition & BMI Calculator

FitMacros is a full-stack web app that turns your age, gender, height,
weight, activity level, and goal into a complete nutrition plan: BMI, BMR,
TDEE, daily calories, macros (protein/carbs/fat), water intake, a healthy
weight range, and a meal-by-meal breakdown.

It's built as a **learning project**, on purpose kept free of databases,
authentication, and Docker, so you can focus on the fundamentals:

- Frontend development (React + Vite + plain CSS)
- Backend API development (Python + FastAPI)
- Connecting a frontend to a backend over HTTP
- Testing an API
- Environment variables
- Git & GitHub
- Deploying a backend to **Render**
- Deploying a frontend to **Vercel**

---

## 📁 Project Structure

```text
fitmacros/
│
├── frontend/                  React + Vite app (what the user sees)
│   ├── public/
│   │   ├── favicon.svg
│   │   └── exercise-animations/    # drop your own exercise GIFs here (see its README)
│   ├── src/
│   │   ├── api/
│   │   │   ├── calculateNutrition.js   # talks to the backend
│   │   │   ├── chatApi.js
│   │   │   └── foodAnalysisApi.js
│   │   ├── utils/
│   │   │   └── imageResize.js          # resizes photos in-browser before upload
│   │   ├── components/
│   │   │   ├── Header.jsx              # gradient hero banner
│   │   │   ├── NutritionForm.jsx       # the input form
│   │   │   ├── Loader.jsx              # loading animation
│   │   │   ├── MacroRing.jsx           # macro donut chart
│   │   │   ├── ResultsDashboard.jsx    # result cards + meal plan
│   │   │   ├── WorkoutPreferencesForm.jsx
│   │   │   ├── WorkoutPrompt.jsx
│   │   │   ├── WorkoutPlanDashboard.jsx
│   │   │   ├── ChatWidget.jsx          # floating fitness coach chatbot
│   │   │   ├── FoodPhotoAnalyzer.jsx   # floating food photo analyzer
│   │   │   └── coach/                  # Workout Coach Mode
│   │   │       ├── WorkoutPlayer.jsx       # session orchestrator
│   │   │       ├── ExerciseCard.jsx        # current exercise display
│   │   │       ├── ExerciseAnimation.jsx   # GIF loader + fallback
│   │   │       ├── CountdownTimer.jsx      # reusable countdown
│   │   │       ├── RestTimer.jsx
│   │   │       ├── ProgressBar.jsx
│   │   │       ├── WorkoutControls.jsx
│   │   │       └── WorkoutSummary.jsx
│   │   ├── App.jsx             # main component, holds app state
│   │   ├── App.css             # component styles
│   │   ├── index.css           # global reset + design tokens
│   │   └── main.jsx             # React entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── backend/                   FastAPI app (does all the math)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic request/response models
│   │   ├── calculations.py     # every nutrition formula
│   │   ├── workouts.py         # rule-based workout plan generator
│   │   ├── exercise_guidance.py
│   │   ├── routes.py           # the /calculate endpoint
│   │   ├── chat_routes.py      # the /chat endpoint
│   │   ├── food_routes.py      # the /analyze-food endpoint
│   │   ├── food_vision.py      # food photo analysis logic (uses Gemini)
│   │   └── gemini_client.py    # shared Gemini API client (chat + food)
│   ├── chatbot/
│   │   ├── knowledge_base/     # JSON topic files (nutrition, workout, etc.)
│   │   ├── chatbot_service.py  # chatbot logic + personalized replies
│   │   ├── keyword_matcher.py  # keyword-based topic matching (no AI)
│   │   └── ai_fallback.py      # optional Gemini fallback for unmatched questions
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt
│   ├── runtime.txt             # pins Python version for Render
│   └── .env.example
│
├── README.md
├── .gitignore
└── LICENSE
```

The frontend and backend are two **independent** projects. They only talk
to each other over HTTP, using a URL stored in an environment variable
(`VITE_API_URL`). This is exactly how real-world apps are structured, and
it's what lets you deploy them to two different platforms (Vercel and
Render).

---

## 🧠 How the Calculations Work

All math lives in `backend/app/calculations.py`:

1. **BMI** = weight(kg) ÷ height(m)²
2. **BMR** — Mifflin-St Jeor Equation (the most widely used formula)
3. **TDEE** = BMR × activity multiplier (1.2 to 1.9 depending on activity)
4. **Goal calories** = TDEE adjusted for Cut / Maintenance / Lean Bulk / Bulk
5. **Protein** = grams per kg of bodyweight, scaled by goal
6. **Fat** = 25% of total daily calories
7. **Carbs** = whatever calories remain after protein and fat
8. **Water** = ~35 ml per kg of bodyweight + an activity bonus
9. **Healthy weight range** = weight at BMI 18.5 and BMI 24.9
10. **Meal plan** = daily totals split 25% / 30% / 30% / 15% across
    breakfast, lunch, dinner, and snacks

The **Weekly Workout Plan** is generated the same way - by rule-based logic
in `backend/app/workouts.py`, with no AI or external calls involved:

11. **Weekly split** is chosen from a fixed template based on your
    available days (3 = Full Body, 4 = Upper/Lower, 5 = Body Part Split,
    6 = Push/Pull/Legs)
12. **Exercises** are pulled from a built-in exercise library, filtered by
    your workout location and available equipment
13. **Sets** scale with fitness level; **rep ranges** reuse the same goal
    you set in the Nutrition section, so you're never asked for it twice
14. **Rest days** fill in the remaining days of the week, with the first
    one set as "Active Recovery" and the rest as full rest

The **Fitness Assistant Chatbot** (the floating 🤖 button) works the same
way - entirely rule-based, no AI APIs involved:

15. Your message is matched against a JSON knowledge base
    (`backend/chatbot/knowledge_base/`) using keyword scoring in
    `keyword_matcher.py` - no exact-sentence matching required
16. Questions like "explain my protein" are detected separately and
    answered using your own calculated numbers, if you've generated a plan
17. Anything that looks like a medical question is redirected to a
    healthcare professional rather than answered directly
18. If nothing matches, you get a friendly fallback message instead of an
    error

**Workout Coach Mode** (the "▶ Start Workout" button on any training day)
guides you through that day's exercises one at a time - animation,
instructions, common mistakes, set tracking, and rest timers - entirely
in the frontend, calling no new backend endpoint.

> **About exercise animations:** the backend only ever sends a *filename*
> (e.g. `pushup.gif`) - it doesn't generate or include any actual GIF
> files. Until you add your own to
> `frontend/public/exercise-animations/`, Coach Mode shows a clean
> animated placeholder instead. See that folder's README for exactly how
> to add real ones.

**Food Photo Analyzer** (the 📸 floating button, bottom-left) is the one
feature in FitMacros that genuinely requires AI - there's no rule-based
way to recognize food in a photo. Take or upload a photo of a meal, and
Gemini's vision model identifies each visible ingredient (e.g. bun,
patty, cheese, sauce for a burger) and estimates calories, protein,
carbs, and fat for each one.

> **This feature requires `GEMINI_API_KEY`** (see `backend/.env.example`
> for the free, no-credit-card signup link - the same key powers the
> chatbot's optional AI fallback). Without it, the analyzer shows a
> clear "not set up yet" message instead of failing unexpectedly. Photos
> are resized in the browser before upload (max 1024px, JPEG) to keep
> uploads fast.

---

## 🚀 Running the Project Locally

You'll need:

- **Node.js** 18+ ([nodejs.org](https://nodejs.org))
- **Python** 3.10+ ([python.org](https://python.org))
- **Git** ([git-scm.com](https://git-scm.com))

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fitmacros.git
cd fitmacros
```

### 2. Start the backend

```bash
cd backend

# Create a virtual environment (keeps dependencies isolated)
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your local environment file
cp .env.example .env

# Start the server
uvicorn main:app --reload
```

Your backend is now running at **http://localhost:8000**.

Open **http://localhost:8000/docs** in your browser — FastAPI
automatically generates interactive API documentation where you can test
the `/calculate` endpoint directly, without needing the frontend at all.

### 3. Start the frontend

Open a **new** terminal window (leave the backend running):

```bash
cd frontend

# Install dependencies
npm install

# Create your local environment file
cp .env.example .env

# Start the dev server
npm run dev
```

Your frontend is now running at **http://localhost:5173**. Open it in your
browser, fill in the form, and press **Calculate Nutrition**.

> If you see a "Could not reach the FitMacros server" error, double-check
> that the backend is still running in the other terminal.

---

## 🧪 Testing the API Directly

You don't need the frontend to test the backend. With the backend running,
try this in a terminal:

```bash
curl -X POST http://localhost:8000/calculate \
  -H "Content-Type: application/json" \
  -d '{
        "age": 25,
        "gender": "male",
        "height_cm": 178,
        "weight_kg": 75,
        "activity_level": "moderately_active",
        "goal": "maintenance",
        "fitness_level": "intermediate",
        "workout_location": "home",
        "available_days": 4,
        "workout_duration": 45,
        "equipment": "dumbbells"
      }'
```

> `equipment` is only required when `workout_location` is `"home"`. When
> `workout_location` is `"gym"`, omit `equipment` entirely (or send `null`)
> - a gym is assumed to have everything.

Or simply visit **http://localhost:8000/docs** and use the "Try it out"
button on the `/calculate` endpoint.

---

## 🔧 Environment Variables

Neither `.env` file is committed to Git (see `.gitignore`) — only the
`.env.example` templates are. This is standard practice: environment
variables often hold values that differ between your machine and
production (or, for real projects, secrets that should never be public).

| File | Variable | Purpose |
|---|---|---|
| `backend/.env` | `ALLOWED_ORIGINS` | Comma-separated list of frontend URLs allowed to call the API (CORS) |
| `frontend/.env` | `VITE_API_URL` | The base URL of the backend API |

---

## 🐙 Git & GitHub Workflow

If you're new to Git, here's the exact sequence to get this project onto
GitHub:

```bash
# 1. Initialize a Git repository (skip if you cloned it already)
git init

# 2. Stage all files
git add .

# 3. Commit
git commit -m "Initial commit: FitMacros app"

# 4. Create a new, empty repository on github.com (do not add a README
#    there - you already have one), then connect it:
git remote add origin https://github.com/YOUR_USERNAME/fitmacros.git

# 5. Push
git branch -M main
git push -u origin main
```

After that, your normal day-to-day workflow is:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## ☁️ Deploying the Backend to Render

1. Push your project to GitHub (see above).
2. Go to [render.com](https://render.com) and sign in with GitHub.
3. Click **New +** → **Web Service**.
4. Select your `fitmacros` repository.
5. Configure the service:
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Under **Environment Variables**, add:
   - `ALLOWED_ORIGINS` = `http://localhost:5173` for now (you'll add your
     Vercel URL here once step 2 of the frontend deployment is done).
7. Click **Create Web Service**. Render will build and deploy your API.
8. Once deployed, copy the live URL Render gives you (something like
   `https://fitmacros-api.onrender.com`) — you'll need it for the frontend.

> Render's free tier "spins down" after inactivity, so the first request
> after a period of inactivity can take up to a minute. This is normal.

---

## ▲ Deploying the Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New...** → **Project**, and import your `fitmacros` repo.
3. Configure the project:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite (Vercel usually detects this automatically)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Under **Environment Variables**, add:
   - `VITE_API_URL` = the Render URL from the backend step (e.g.
     `https://fitmacros-api.onrender.com`)
5. Click **Deploy**.
6. Once deployed, copy your live Vercel URL (e.g.
   `https://fitmacros.vercel.app`).

### Final step: connect the two

Go back to your Render backend's environment variables and update
`ALLOWED_ORIGINS` to include your live Vercel URL:

```text
ALLOWED_ORIGINS=http://localhost:5173,https://fitmacros.vercel.app
```

Redeploy the backend so the change takes effect. Your app is now fully
live and the two services can talk to each other. 🎉

---

## 🩺 Disclaimer

FitMacros is an educational project. The calculations use widely accepted,
general-purpose formulas, but they are not a substitute for advice from a
doctor, dietitian, or other qualified professional.

## 📄 License

Released under the [MIT License](LICENSE).
