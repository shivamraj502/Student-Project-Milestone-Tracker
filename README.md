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
