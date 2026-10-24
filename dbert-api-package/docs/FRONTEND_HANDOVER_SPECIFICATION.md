# DBERT Frontend Handover Specification
> **Document Purpose**: Pure functional, architectural, data, and content specification for an AI agent or engineering team building the DBERT frontend from scratch.  
> **Backend Package**: `dbert-api-package-v1.zip`  
> **API Version**: 1.0.0 (FastAPI + PostgreSQL 15)  
> **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI) & `http://localhost:8000/redoc` (ReDoc)  
> **Static OpenAPI 3.1 Spec**: `dbert-api-package/docs/openapi.json`  

---

## 1. System Overview & Architecture

The DBERT backend has been completely rebuilt as a high-performance, asynchronous REST API. The frontend is fully decoupled from the backend and interacts strictly via HTTP/HTTPS JSON endpoints (and `multipart/form-data` for file uploads).

```
+---------------------------------------------------------------------------------------+
|                                    FRONTEND CLIENT                                    |
|              (Next.js / React / Vue / Mobile Client - Handover Scope)                 |
+-------------------------------------------+-------------------------------------------+
                                            |
                         HTTPS Bearer JWT   |   REST JSON / Uploads
                                            v
+---------------------------------------------------------------------------------------+
|                                   NGINX REVERSE PROXY                                 |
|                               (Ports 80 / 443 -> 8000)                                |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            v
+---------------------------------------------------------------------------------------+
|                               FASTAPI ASYNC BACKEND                                   |
|                88 REST Endpoints across 18 Router Modules (/api/v1/*)                 |
+---------------------+---------------------+---------------------+---------------------+
                      |                     |                     |
                      v                     v                     v
            +-------------------+ +-------------------+ +-------------------+
            |   PostgreSQL 15   | |  Razorpay Gateway | |  Google Gemini AI |
            |    (74 Tables)    | |  (Async Checkout) | |  (Async Key-Rot)  |
            +-------------------+ +-------------------+ +-------------------+
```

### Connection Endpoints
- **Local Development Base URL**: `http://localhost:8000`
- **API Prefix**: `/api/v1`
- **Health Check**: `GET http://localhost:8000/health`
- **File Upload Assets**: `GET http://localhost:8000/uploads/{filename}`

---

## 2. User Roles & Permission Matrix

The system enforces 5 distinct authenticated user roles in addition to anonymous public guests:

| Role Code | User Type | Description | Primary Capabilities |
|---|---|---|---|
| `public` | Unauthenticated Visitor | General web visitor | Browse marketing pages, blog, public job marketplace, course catalog, view verified certificates and public CVs |
| `intern` | Student / Candidate | Enrolled or applicant student | Multi-stage signup, apply for internships, take AI interview, enroll, access course player, chat with AI tutor, submit projects, practice tasks, earn coins, request withdrawals, message mentors |
| `company` | Employer / Partner | Hiring company | Create company profile, post internship/job openings, manage applications, review candidates |
| `mentor` | Technical Mentor | Industry advisor | View student submissions, manage availability slots, conduct sessions |
| `staff` | Operations Staff | Platform operator | Review intern applications, approve project submissions, triage queue roles |
| `admin` | Super Administrator | Executive control plane | Platform metrics, manage all accounts, export data to CSV, view abuse logs, trigger maintenance cron jobs |

---

## 3. Site Map & Complete View Inventory

The frontend must provide views for the following functional routes:

### 3.1 Public Marketing & Educational Pages
1. **Home / Landing**: Value proposition, ecosystem statistics (`GET /api/v1/public/stats/openings`), featured companies, course highlights, partner logos.
2. **About Us**: Company mission, leadership, ecosystem partners (DBERT, Gayatri AI, Digital Blaize).
3. **AI Consultant**: Enterprise AI consulting services, inquiry trigger.
4. **AI Solutions**: Production AI case studies and tech stack overview.
5. **Labs**: Applied AI research, open-source projects, and repository links.
6. **Learners / Internships**: Career tracks, student journey overview, testimonials.
7. **Pricing / Fee Structure**: Transparent breakdown of free tracks, scholarship tracks, and certified direct tracks (₹1,599).
8. **Startups / Employers**: Hiring partner onboarding, talent sourcing overview.
9. **Course Catalog** (`/courses`): Public course listings (`GET /api/v1/public/courses`).
10. **Single Course Overview** (`/courses/:id`): Curriculum breakdown, syllabus, modules, projects.
11. **Job Marketplace** (`/marketplace` or `/jobs`):
    - All job/internship listings with filters for domain, work mode (Remote/On-site), and stipend (`GET /api/v1/marketplace/internships`).
    - Lead Detail View (`/marketplace/:slug` or `/marketplace/lead/:id`): Job description, responsibilities, skills, click tracking (`POST /api/v1/marketplace/lead/:id/click`), and community comments (`GET/POST /api/v1/marketplace/lead/:id/comment`).
12. **Blog & Knowledge Hub** (`/blog`):
    - Article list (`GET /api/v1/public/blog-posts`).
    - Article reader (`GET /api/v1/public/blog-posts/:slug`): Markdown rendering, author, domain tags.
13. **Public Certificate Verification** (`/verify/:cert_id`):
    - Public credential verification (`GET /api/v1/certificate/:cert_id`). Displays student name, domain, issue date, verification badge.
14. **Public Intern CV View** (`/cv/:slug`):
    - Public portfolio/CV rendered from structured JSON (`GET /api/v1/cv/public/:slug`).
15. **Legal & Compliance**:
    - Privacy Policy (`/privacy`)
    - Terms of Service (`/terms`)
    - Refund Policy (`/refund`)

---

### 3.2 Authentication & Onboarding Views
1. **Login Hub**: Role switcher or unified login supporting Intern, Company, Mentor, Staff, Admin credentials (`POST /api/v1/auth/{role}/login`).
2. **Multi-Stage Intern Application & Registration**:
   - **Stage 1 (Identity)**: Full Name, Email Address (`POST /api/v1/auth/intern/signup/stage1`).
   - **Stage 2 (Domain & Phone)**: Selected Internship Track, WhatsApp Phone Number (`POST /api/v1/auth/intern/signup/stage2`).
   - **Stage 3 (Academic & Availability Details)**:
     - College Name
     - Course / Degree
     - Current Semester (1st to 8th)
     - Year of Passing
     - 3-Month Availability Confirmation (Yes/No)
     - Laptop & Internet Connection Confirmation (Yes/No)
     - Job Placement Assistance Required (Yes/No)
     - Referral Source (Unstop, LinkedIn, Campus, Friend, etc.)
     - Resume / CV Upload (`POST /api/v1/uploads/resume`)
     - Calls `POST /api/v1/auth/intern/signup/stage3` and `POST /api/v1/applications/apply`.
3. **Company Registration**: Company Name, Website, Contact Email, Password, Industry, Location (`POST /api/v1/auth/company/signup`).
4. **Forgot & Reset Password**:
   - Email submission (`POST /api/v1/auth/forgot-password`).
   - Reset token validation & new password input (`POST /api/v1/auth/reset-password`).
5. **Phone OTP Verification**: Request OTP (`POST /api/v1/auth/send-otp`), Verify OTP (`POST /api/v1/auth/verify-otp`).

---

### 3.3 Intern Workspace / LMS Portal
1. **Intern Dashboard & Wizard**:
   - Onboarding step progress tracker (`GET /api/v1/intern/wizard-status`).
   - Step saving (`POST /api/v1/intern/save-wizard-step`).
   - Latest posts and announcement feed (`GET /api/v1/intern/latest-posts`).
2. **AI Technical Interview Interface**:
   - Status checker (`GET /api/v1/intern/interview/status`). Checks if already taken, score, or 24h cooling off.
   - Start Interview (`POST /api/v1/intern/interview/start`). Generates domain questions (or pulls from domain bank).
   - Question player: Displays 5 technical questions sequentially. Accepts text or speech answers.
   - Submit answers & trigger evaluation (`POST /api/v1/intern/interview/submit`).
   - Score & Detailed Feedback Report View.
3. **Applications Tracker**:
   - List intern applications (`GET /api/v1/intern/my-applications`).
   - State Machine visual indicator: `Apply Pending` -> `Under Review` -> `Selected` -> `Enrollment Pending` -> `Enrolled`.
4. **Enrollment & Razorpay Payment Checkout**:
   - Offer acceptance & deposit payment (`POST /api/v1/enrollments/submit`).
   - Payment order generation (`POST /api/v1/payments/create-order`).
   - Razorpay Checkout modal launch.
   - Payment verification & enrollment activation (`POST /api/v1/payments/verify`).
5. **Course Player / LMS**:
   - Enrolled courses listing (`GET /api/v1/courses/enrolled`).
   - Course structure viewer (`GET /api/v1/courses/:id`): Chapters, subtopics, lessons.
   - Day Quiz Interface (`GET /api/v1/courses/:course_id/quiz/:day_number`):
     - Multiple-choice questions with tab-switch detection and timer.
     - Submission & instant scoring (`POST /api/v1/courses/quiz/submit`).
   - Capstone Project Submission (`POST /api/v1/courses/projects/submit`): GitHub repository URL, title, description.
6. **Guided Learning & Socratic AI Tutor**:
   - Concept tree browser (`GET /api/v1/learning/v2/concept-tree/:course_id`).
   - AI Tutor interactive chat (`POST /api/v1/learning/v2/chat`): Socratic interactive dialog assessing understanding.
   - Spaced Repetition Due Reviews (`GET /api/v1/learning/v2/reviews-due`).
7. **Direct Messaging**:
   - Inbox & conversation threads (`GET /api/v1/messages`).
   - Chat thread view (`GET /api/v1/messages/:conv_id`).
   - Send message (`POST /api/v1/messages/:conv_id/send`).
   - Mark as read (`POST /api/v1/messages/:conv_id/read`).
8. **Notification Center**:
   - List notifications (`GET /api/v1/notifications`).
   - Mark single / all read (`POST /api/v1/notifications/:id/read`).
9. **Practice Tasks Hub**:
   - Task list (`GET /api/v1/tasks`).
   - Task detail & instructions (`GET /api/v1/tasks/:id`).
   - Task submission (`POST /api/v1/tasks/:id/submit`): Link or file upload, coin reward credit.
10. **Coin Wallet & Ambassador Dashboard**:
    - Coin balance & ledger history (`GET /api/v1/account/coins`).
    - Referral links & conversion statistics (`GET /api/v1/ambassador`).
    - Cash withdrawal request form (`POST /api/v1/ambassador/withdraw`): UPI ID, amount in INR.
11. **CV Builder**:
    - Intern CV view / editor (`GET/POST /api/v1/cv`).
    - Education, skills, work experience, projects, custom slug, public visibility toggle.

---

### 3.4 Company / Employer Portal
1. **Company Dashboard**: Active job postings, view count, application count (`GET /api/v1/company/me`).
2. **Post Job / Internship**:
   - Job creation form (`POST /api/v1/company/posts`): Title, domain, type (internship/job), description, responsibilities, skills, stipend range, pay period, work mode (Remote/Hybrid/On-site), duration, openings.
3. **Manage Postings**: List active/draft posts (`GET /api/v1/company/posts`).
4. **Applicant Review Queue**:
   - View applications for company posts (`GET /api/v1/company/applications`).
   - Candidate details, resume download, contact candidate.

---

### 3.5 Admin Control Plane
1. **Executive Dashboard**: System metrics (`GET /api/v1/admin/stats`): Total intern accounts, total applications, enrolled count, verified payments count.
2. **Application Manager**:
   - Paginated application list with filters (`GET /api/v1/admin/applications`).
   - Update application status (`POST /api/v1/admin/applications/:id/status`): Transitions `Under Review` -> `Selected` -> `Rejected`.
3. **Enrollment Manager**:
   - Paginated enrollment list (`GET /api/v1/admin/enrollments`).
   - Confirm enrollment / fee verification (`POST /api/v1/admin/enrollments/:id/verify`).
4. **User Account Directory**: Paginated user search, block/unblock, reset password (`GET /api/v1/admin/users`, `POST /api/v1/admin/users/:id/block`).
5. **Data Exports**: One-click CSV downloads for Applications, Enrollments, Interns, and Payments (`GET /api/v1/admin/export/:entity`).
6. **Telemetry & Abuse Monitoring**: Suspicious activity logs, rate limit infractions (`GET /api/v1/admin/abuse-logs`).

---

### 3.6 Mentor & Staff Operations
1. **Mentor Availability Calendar**:
   - Add availability slots (`POST /api/v1/mentor/slots`).
   - View booked student sessions (`GET /api/v1/mentor/bookings`).
2. **Staff Project Review Queue**:
   - View pending student project submissions (`GET /api/v1/staff/submissions`).
   - Approve / Reject project with feedback (`POST /api/v1/staff/submissions/:id/review`).

---

## 4. Comprehensive API Contract & Route Specification

Every protected route requires the HTTP header:
```http
Authorization: Bearer <jwt_access_token>
```

### 4.1 Authentication (`/api/v1/auth`)

#### Intern Login
- **Endpoint**: `POST /api/v1/auth/intern/login`
- **Request Body**:
  ```json
  {
    "email": "student@example.com",
    "password": "SecretPassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "role": "intern",
    "user_id": 1,
    "email": "student@example.com",
    "name": "Alex Smith"
  }
  ```

#### Company Login
- **Endpoint**: `POST /api/v1/auth/company/login`
- **Request Body**: `{ "email": "hr@acme.com", "password": "password" }`
- **Response**: Same token structure with `"role": "company"`.

#### Admin Login
- **Endpoint**: `POST /api/v1/auth/admin/login`
- **Request Body**: `{ "email": "admin@dbert.com", "password": "password" }`
- **Response**: Same token structure with `"role": "admin"`.

#### Token Refresh
- **Endpoint**: `POST /api/v1/auth/refresh`
- **Request Body**: `{ "refresh_token": "eyJhbGciOi..." }`
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "role": "intern"
  }
  ```

#### Current User Status
- **Endpoint**: `GET /api/v1/auth/status` (Auth Required)
- **Response (200 OK)**:
  ```json
  {
    "authenticated": true,
    "user_id": 1,
    "email": "student@example.com",
    "role": "intern"
  }
  ```

---

### 4.2 Multi-Stage Intern Registration & Application

#### Signup Stage 1: Identity
- **Endpoint**: `POST /api/v1/auth/intern/signup/stage1`
- **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "SecurePassword123"
  }
  ```
- **Response (200 OK)**: `{ "status": "success", "message": "Stage 1 saved", "stage": 1 }`

#### Signup Stage 2: Track & Phone
- **Endpoint**: `POST /api/v1/auth/intern/signup/stage2`
- **Request Body**:
  ```json
  {
    "email": "jane@example.com",
    "phone": "9876543210",
    "domain": "Machine Learning (ML)"
  }
  ```
- **Response (200 OK)**: `{ "status": "success", "message": "Stage 2 saved", "stage": 2 }`

#### Signup Stage 3: Academic & Profile
- **Endpoint**: `POST /api/v1/auth/intern/signup/stage3`
- **Request Body**:
  ```json
  {
    "email": "jane@example.com",
    "college": "National Institute of Technology",
    "course": "B.Tech Computer Science",
    "semester": "6th Semester",
    "year_of_passing": "2026",
    "city": "Bengaluru"
  }
  ```
- **Response (200 OK)**: `{ "status": "success", "message": "Account created successfully", "stage": 3 }`

#### Submit Formal Application
- **Endpoint**: `POST /api/v1/applications/apply` (Auth: Optional / Intern)
- **Request Body**:
  ```json
  {
    "domain": "Machine Learning (ML)",
    "phone": "9876543210",
    "college": "Dayananda Sagar College of Engineering",
    "course": "B.Tech",
    "semester": "5th Semester",
    "year_of_passing": "2026",
    "city": "Bengaluru",
    "resume_url": "https://dbert.in/uploads/resumes/jane_cv.pdf",
    "github_url": "https://github.com/janedoe",
    "linkedin_url": "https://linkedin.com/in/janedoe",
    "source": "Unstop",
    "answers_json": {
      "available_next_3_months": true,
      "has_laptop_and_internet": true,
      "requires_job_placement": true,
      "hear_about_us": "Unstop"
    }
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "status": "success",
    "application_id": 4594,
    "application_status": "Apply Pending",
    "message": "Application submitted successfully"
  }
  ```

---

### 4.3 AI Technical Interview (`/api/v1/intern/interview`)

#### Interview Status & Eligibility
- **Endpoint**: `GET /api/v1/intern/interview/status` (Auth: Intern)
- **Response (200 OK)**:
  ```json
  {
    "can_start": true,
    "last_interview_at": null,
    "cooling_off_hours_remaining": 0,
    "previous_score": null,
    "status": "not_started"
  }
  ```

#### Start AI Interview
- **Endpoint**: `POST /api/v1/intern/interview/start` (Auth: Intern)
- **Request Body**: `{ "domain": "Full Stack Development" }`
- **Response (200 OK)**:
  ```json
  {
    "interview_id": 577,
    "domain": "Full Stack Development",
    "total_questions": 5,
    "questions": [
      {
        "id": 1,
        "question": "Explain how event delegation works in modern JavaScript and why it improves DOM memory efficiency.",
        "concept": "JavaScript Event Loop & DOM"
      },
      {
        "id": 2,
        "question": "What is the difference between SQL indexing with B-Trees vs Hash indexes, and when would you use each?",
        "concept": "Database Indexing"
      }
    ]
  }
  ```

#### Submit Interview Answers & Get Evaluation
- **Endpoint**: `POST /api/v1/intern/interview/submit` (Auth: Intern)
- **Request Body**:
  ```json
  {
    "interview_id": 577,
    "answers": [
      {
        "question_id": 1,
        "answer_text": "Event delegation binds a single listener to a parent node rather than every child..."
      },
      {
        "question_id": 2,
        "answer_text": "B-Tree indexes support range queries (<, >), while Hash indexes only allow O(1) equality lookups..."
      }
    ]
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "interview_id": 577,
    "status": "completed",
    "score": 8.5,
    "max_score": 10.0,
    "verdict": "RECOMMENDED_FOR_SELECTION",
    "feedback": "Strong conceptual understanding of DOM architecture and relational database structures."
  }
  ```

---

### 4.4 Course Catalog, LMS & Socratic AI Tutor

#### Course Listing
- **Endpoint**: `GET /api/v1/courses`
- **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "title": "Machine Learning Foundations",
      "slug": "machine-learning-foundations",
      "domain": "Machine Learning (ML)",
      "duration_days": 15,
      "total_chapters": 6,
      "is_active": true
    }
  ]
  ```

#### Day Quiz Player
- **Endpoint**: `GET /api/v1/courses/{course_id}/quiz/{day_number}` (Auth: Intern)
- **Response (200 OK)**:
  ```json
  {
    "day_number": 3,
    "course_id": 1,
    "questions": [
      {
        "id": 1,
        "question": "What mathematical function is primarily used in logistic regression to map outputs between 0 and 1?",
        "options": ["Sigmoid", "ReLU", "Softmax", "Tanh"]
      }
    ]
  }
  ```

#### Submit Quiz Attempt
- **Endpoint**: `POST /api/v1/courses/quiz/submit` (Auth: Intern)
- **Request Body**:
  ```json
  {
    "course_id": 1,
    "day_number": 3,
    "answers": { "1": 0 },
    "tab_switches": 0,
    "time_taken_sec": 45
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "score": 10,
    "max_score": 10,
    "passed": true,
    "correct_answers": 1,
    "total_questions": 1
  }
  ```

#### Socratic AI Tutor Chat (Guided Learning)
- **Endpoint**: `POST /api/v1/learning/v2/chat` (Auth: Intern)
- **Request Body**:
  ```json
  {
    "course_id": 1,
    "concept_id": "gradient_descent",
    "message": "Why does setting learning rate too high cause divergence?"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "reply": "Think about taking a step so large across a valley that you overshoot the lowest point and land higher on the opposite slope. What happens if you take an even larger step on the next iteration?",
    "mastery_score": 0.45,
    "concept_id": "gradient_descent"
  }
  ```

---

### 4.5 Payments & Checkout (`/api/v1/payments`)

#### Create Razorpay Order
- **Endpoint**: `POST /api/v1/payments/create-order` (Auth: Intern)
- **Request Body**:
  ```json
  {
    "purpose": "security_deposit",
    "enrollment_id": 412,
    "amount_inr": 1599
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "order_id": "order_Nz1kL9...",
    "amount": 159900,
    "currency": "INR",
    "key_id": "rzp_live_..."
  }
  ```

#### Verify Payment Signature
- **Endpoint**: `POST /api/v1/payments/verify` (Auth: Intern)
- **Request Body**:
  ```json
  {
    "razorpay_order_id": "order_Nz1kL9...",
    "razorpay_payment_id": "pay_Nz2mX8...",
    "razorpay_signature": "9a5b3c...",
    "enrollment_id": 412
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Payment verified and enrollment activated.",
    "enrollment_status": "Enrolled"
  }
  ```

---

### 4.6 File Upload API (`/api/v1/uploads`)

- **Resume Upload**: `POST /api/v1/uploads/resume`
- **Avatar Upload**: `POST /api/v1/uploads/avatar`
- **Task Submission File Upload**: `POST /api/v1/uploads/document`
- **Content-Type**: `multipart/form-data`
- **Validation**:
  - File formats allowed: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.docx`.
  - Binary magic byte validation rejects disguised executables (`.php`, `.exe`, `.sh`).
  - Size limit: 10 MB.
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "filename": "e9a2b1c4_resume.pdf",
    "url": "http://localhost:8000/uploads/e9a2b1c4_resume.pdf"
  }
  ```

---

## 5. Domain Content & Preloaded Tracks

The backend contains production curriculum and internship tracks across 4 primary technical domains:

### 1. Machine Learning (ML)
- **Course**: Machine Learning Foundations & Vector Architecture
- **Curriculum**: NumPy/Pandas EDA, Supervised Regression/Classification, Model Validation, Feature Engineering, Scikit-Learn pipelines.
- **Capstone**: Predictive tabular modeling and production ML API packaging.

### 2. Data Analyst
- **Course**: Data Analysis & Modern Business Intelligence
- **Curriculum**: Advanced Excel tabular modeling, PostgreSQL relational queries, Window functions, CTEs, Python data wrangling, Matplotlib / Seaborn dashboards.
- **Capstone**: End-to-end analytics report with executive presentation.

### 3. Generative AI & Agent Development
- **Course**: Generative AI & Autonomous Agent Architecture
- **Curriculum**: LLM prompt engineering, Temperature & Tokenization, RAG (Retrieval-Augmented Generation), Vector Databases (ChromaDB / pgvector), LangChain, Multi-agent orchestration.
- **Capstone**: Production RAG pipeline with custom knowledge base.

### 4. Full Stack Development
- **Course**: Full Stack Web Development (FastAPI + React/Next.js)
- **Curriculum**: REST API design, JWT auth, Database modeling, Component lifecycle, State management, Tailwind styling, Deployment pipelines.
- **Capstone**: Production multi-tenant web application.

---

## 6. Frontend Handover & Setup Checklist

To set up and run against the real backend locally:

### Step 1: Start Backend
```bash
# Extract dbert-api-package-v1.zip
unzip dbert-api-package-v1.zip
cd dbert-api-package

# Launch container stack
docker-compose up -d --build
```

### Step 2: Configure Frontend Environment (`.env.local`)
```ini
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_UPLOADS_URL=http://localhost:8000/uploads
NEXT_PUBLIC_RAZORPAY_KEY_ID=rzp_test_placeholder
NEXT_PUBLIC_ONESIGNAL_APP_ID=onesignal_placeholder_app_id
```

### Step 3: Reference Content & Visual Assets
- All original icons, logos, illustrations, and blog posts are available in:
  `dbert-api-package/website-content/public/`
- Original Next.js components and MDX blog posts are available in:
  `dbert-api-package/website-content/src/`
- Full API documentation is live at `http://localhost:8000/docs`.
