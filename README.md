<<<<<<< HEAD
# 🎓 Student Project & Milestone Tracker

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS" />
</div>

## 📌 Overview
Managing capstone projects, tracking document submissions, and maintaining faculty evaluation records is traditionally a chaotic, spreadsheet-driven process. 

The **Student Project & Milestone Tracker** is a centralized platform designed to streamline academic workflows. It empowers students to submit phased project milestones, enables faculty guides to efficiently evaluate and grade submissions, and provides coordinators with real-time data exports.

## ✨ Value Proposition (Why We Built This)
* **For Students:** A clear, step-by-step portal to upload deliverables (Synopsis, Phase 1 & 2, Final Report) without the hassle of lost email threads.
* **For Faculty (Guides):** A dedicated dashboard to track assigned teams, provide structured feedback, allocate marks, and approve projects for publication.
* **For Administrators:** Instant CSV report generation for university auditing and record-keeping.

## 🚀 Core Features (MVP)
1. **Team Registration:** Register capstone projects with full team details (USNs, Names) and domain classifications (e.g., AIML, Cloud Computing).
2. **Milestone Upload Engine:** Secure file uploads with built-in validation (size limits and correct file extensions) for each project stage.
3. **Faculty Evaluation Portal:** Dedicated interface for guides to review submissions, assign marks (0-100), and rate projects (Poor to Outstanding).
4. **Glassmorphic UI Design:** A premium, modern, responsive interface prioritizing user experience and aesthetic appeal.
5. **Admin Reporting:** One-click CSV export functionality for all tracked project metrics and statuses.

## 🏗️ Technical Architecture
* **Backend:** Django (Python) - Handling ORM, routing, and server-side validation.
* **Database:** SQLite (Development) -> PostgreSQL (Planned for Production).
* **Frontend:** Django Templates combined with custom Vanilla CSS utilizing a dark "Glassmorphism" design system.

## 📂 Project Structure
```text
Student-Project-Milestone-Tracker/
├── projects/                 # Core Django App
│   ├── models.py             # Database Schema (Project, Milestone, Evaluation)
│   ├── views.py              # Business Logic & Routing
│   ├── forms.py              # Form Validation Logic
│   └── urls.py               # Endpoint Definitions
├── static/                   # Static Assets
│   └── style.css             # Glassmorphic Design System
├── templates/                # HTML Views
│   ├── base.html             # Master Layout & Navbar
│   ├── home.html             # Dashboard View
│   ├── project_list.html     # Directory & Status Badges
│   └── ...                   # Upload & Evaluation Forms
├── student_project_tracker/  # Django Project Configuration
├── manage.py                 # Django Entry Point
└── requirements.txt          # Dependencies
```

## 🛠️ Local Installation & Setup
To run this project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shivamraj502/Student-Project-Milestone-Tracker.git
   cd Student-Project-Milestone-Tracker
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000` in your web browser.

## 🗺️ Roadmap (Future Enhancements)
*   [ ] **Role-Based Authentication:** Distinct login portals for Students, Guides, and Admins.
*   [ ] **Cloud Integration:** Migrate local media uploads to AWS S3 for production durability.
*   [ ] **Automated Notifications:** Email alerts for milestone submissions and guide evaluations.
*   [ ] **Advanced Analytics:** Dynamic dashboard visualizations (Chart.js) for domain distributions and grade averages.
*   [ ] **Production Deployment:** Containerization and deployment to Render with PostgreSQL.
=======
# Django-semihack-starter
Starter template for semi-hackathon
# 🚀 Django Semi-Hackathon: [Team Name]

## 📋 Project Details
- **Theme**: [e.g., TH-03: Elective Choice System]
- **Team Members**: @student1, @student2, @student3, @student4
- **Live URL**: [To be filled after deployment]

## ✅ Submission Checklist
- [ ] Code runs with `pip install -r requirements.txt`
- [ ] `DEBUG=False` in production settings
- [ ] Working AJAX endpoint (tested live)
- [ ] CSV/PDF export functional
- [ ] CO-SDG mapping table completed below
- [ ] 150-word SDG justification included

## 🎯 CO-SDG Mapping Table
| Course Outcome | How This Project Demonstrates It | SDG Target Addressed |
|---------------|----------------------------------|---------------------|
| CO1: MVT Architecture | [Brief explanation] | SDG 4.5 |
| CO2: Models & Forms | [Brief explanation] | SDG 9.5 |
| ... | ... | ... |

## 📦 Setup Instructions
```bash
git clone [your-repo-url]
cd [repo-name]
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### ✅ Pre-Deploy Checklist
- [ ] `DEBUG = False` in `settings.py`
- [ ] `STATIC_ROOT` configured
- [ ] `ALLOWED_HOSTS` includes cloud domain
- [ ] `gunicorn` in `requirements.txt`
- [ ] Local `python manage.py collectstatic` ran successfully
## 🚀 Deployment Guide (Free Tier: Render)
*Follow these steps on Event Day to make your app publicly accessible for judging.*

1. **Sign Up & Connect**
   - Go to [render.com](https://render.com) → Sign up with GitHub
   - Authorize Render to access your repos

2. **Create Web Service**
   - Click `New +` → `Web Service` → Connect this repo
   - Fill in:
     - **Name**: `team-xyz-app`
     - **Region**: `Oregon` or `Frankfurt` (closest to India)
     - **Branch**: `main`
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn project_name.wsgi` *(replace `project_name` with your actual Django folder)*

3. **Environment Variables (Critical)**
   Click `Advanced` → `Add Environment Variable`:
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | Generate at [miniwebtool.com/django-secret-key-generator](https://miniwebtool.com/django-secret-key-generator/) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `*.onrender.com, localhost, 127.0.0.1` |

4. **Deploy & Verify**
   - Click `Create Web Service` → Wait 2–4 mins for build
   - Once live, copy the `https://...onrender.com` URL
   - ✅ Test: Open URL, check CSS/JS loads, test AJAX endpoint, download CSV/PDF
   - 📝 Update this `README.md` with your live URL

### 🚨 Troubleshooting Quick Fixes
| Issue | Fix |
|-------|-----|
| `Application Error` | Ensure `gunicorn` is in `requirements.txt` & `wsgi` path matches your project folder |
| Broken CSS/JS | Add `STATIC_ROOT = BASE_DIR / "staticfiles"` to `settings.py` |
| `DisallowedHost` | Verify `ALLOWED_HOSTS` env var or `settings.py` matches your Render domain |
| DB locked/migrations fail | Free tier uses SQLite by default. It's fine for hackathon demos. No extra config needed. |

> 💡 **Note:** After deployment, every `git push` to `main` auto-triggers a rebuild. No manual server restarts needed.
>>>>>>> 2a55c0b7423e0e5327e885164cfe16ed0f77dc77
