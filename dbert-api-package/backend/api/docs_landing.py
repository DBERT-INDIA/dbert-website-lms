"""
DBERT REST API - Developer Platform & Instructions Hub
Generates rich HTML developer portal and machine-readable JSON API manifests.
"""

from typing import Dict, Any

def get_api_manifest_json(version: str = "1.0.0", environment: str = "production") -> Dict[str, Any]:
    """Returns structured JSON API manifest for machine discovery."""
    return {
        "name": "DBERT Ecosystem REST API",
        "version": version,
        "environment": environment,
        "status": "operational",
        "description": "High-performance REST API powering DBERT digital credentials, internship tracking, courses, AI tutor, and job marketplace.",
        "sovereign_domain": "https://api.dbert.in",
        "base_url": "https://api.dbert.in/api/v1",
        "documentation": {
            "developer_portal": "https://api.dbert.in/",
            "interactive_swagger": "https://api.dbert.in/docs",
            "technical_redoc": "https://api.dbert.in/redoc",
            "openapi_specification": "https://api.dbert.in/openapi.json"
        },
        "health_probes": {
            "liveness": "https://api.dbert.in/health",
            "readiness": "https://api.dbert.in/ready",
            "system_status": "https://api.dbert.in/status"
        },
        "authentication": {
            "type": "Bearer JWT",
            "header": "Authorization: Bearer <jwt_access_token>",
            "token_ttl_seconds": 3600,
            "endpoints": {
                "intern_login": "POST /api/v1/auth/intern/login",
                "company_login": "POST /api/v1/auth/company/login",
                "mentor_login": "POST /api/v1/auth/mentor/login",
                "staff_login": "POST /api/v1/auth/staff/login",
                "refresh_token": "POST /api/v1/auth/refresh",
                "logout": "POST /api/v1/auth/logout"
            }
        },
        "core_modules": [
            {
                "name": "Auth & Security",
                "prefix": "/api/v1/auth",
                "description": "Role-based authentication, JWT issuance, session refresh, and password management."
            },
            {
                "name": "Credentials & Verification",
                "prefix": "/api/v1/certificate, /api/v1/cv",
                "description": "Instant cryptographic validation of DBERT completion certificates and dynamic student CVs."
            },
            {
                "name": "Job & Internship Marketplace",
                "prefix": "/api/v1/marketplace",
                "description": "Programmatic querying of 6,600+ vetted tech internships, full-time jobs, and curated leads."
            },
            {
                "name": "Application State Machine",
                "prefix": "/api/v1/applications",
                "description": "Idempotent applicant lifecycle management (applied -> screening -> interview -> enrolled)."
            },
            {
                "name": "Courses & Guided Learning",
                "prefix": "/api/v1/courses, /api/v1/learning",
                "description": "Curriculum delivery, chapter quizzes, and pedagogical AI tutor dialog sessions."
            },
            {
                "name": "Intern Workspace",
                "prefix": "/api/v1/intern",
                "description": "Personalized intern profiles, milestone submissions, and 1-on-1 mentorship bookings."
            },
            {
                "name": "College Ambassador & Referrals",
                "prefix": "/api/v1/ambassador",
                "description": "Referral click tracking, 10% cash commission calculation, and Fernet-encrypted UPI payouts."
            },
            {
                "name": "Payments & Orders",
                "prefix": "/api/v1/payments",
                "description": "Razorpay order generation, HMAC SHA256 payment signature validation, and webhooks."
            },
            {
                "name": "Company & Hiring Partner",
                "prefix": "/api/v1/company",
                "description": "Employer registration, opportunity authoring, candidate screening, and hiring."
            }
        ],
        "quickstart_curl": "curl -X GET 'https://api.dbert.in/api/v1/marketplace/internships?page=1' -H 'Accept: application/json'"
    }


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT API Developer Platform & Instructions | Build on api.dbert.in</title>
  <meta name="description" content="Official DBERT Developer Hub. Complete API instructions, quickstart tutorials, authentication guides, and interactive endpoints to create on api.dbert.in.">
  <link rel="canonical" href="https://api.dbert.in/">
  <link rel="icon" type="image/x-icon" href="https://dbert.in/favicon.ico">
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <style>
    :root {
      --bg-dark: #070B14;
      --bg-surface: #0E1526;
      --bg-card: #141E34;
      --bg-card-hover: #1A2846;
      --border: #1E2E4E;
      --border-bright: #2C4270;
      --text: #F1F5F9;
      --text-muted: #94A3B8;
      --text-dim: #64748B;
      --gold: #F59E0B;
      --gold-bright: #FBBF24;
      --gold-glow: rgba(245, 158, 11, 0.15);
      --cyan: #38BDF8;
      --cyan-glow: rgba(56, 189, 248, 0.15);
      --emerald: #10B981;
      --purple: #A855F7;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      background-color: var(--bg-dark);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* Global Nav */
    .nav {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(7, 11, 20, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
    }
    .nav-container {
      max-width: 1240px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text);
    }
    .brand-logo {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #F59E0B, #D97706);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #070B14;
      font-size: 18px;
      box-shadow: 0 0 16px rgba(245, 158, 11, 0.4);
    }
    .brand-text {
      display: flex;
      flex-direction: column;
    }
    .brand-title {
      font-weight: 800;
      font-size: 18px;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .badge-api {
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 6px;
      background: var(--gold-glow);
      color: var(--gold);
      border: 1px solid rgba(245, 158, 11, 0.3);
      font-weight: 700;
      letter-spacing: 0.05em;
    }
    .brand-sub {
      font-size: 11px;
      color: var(--text-dim);
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    .nav-link {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      transition: color 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .nav-link:hover {
      color: var(--text);
    }
    .nav-cta {
      background: linear-gradient(135deg, #F59E0B, #D97706);
      color: #070B14;
      padding: 7px 16px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 13px;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .nav-cta:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4);
    }

    /* Main Container */
    .container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 40px 24px 80px;
    }

    /* Hero Section */
    .hero {
      text-align: center;
      padding: 50px 0 40px;
      position: relative;
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 5px 14px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--emerald);
      font-size: 12.5px;
      font-weight: 700;
      margin-bottom: 20px;
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 10px var(--emerald);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.9); }
      100% { opacity: 1; transform: scale(1); }
    }
    .hero h1 {
      font-size: clamp(32px, 5vw, 54px);
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 18px;
      background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .hero p {
      font-size: clamp(16px, 2vw, 19px);
      color: var(--text-muted);
      max-width: 780px;
      margin: 0 auto 32px;
      line-height: 1.6;
    }
    .hero-actions {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 24px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 14.5px;
      text-decoration: none;
      transition: all 0.2s;
      cursor: pointer;
    }
    .btn-gold {
      background: linear-gradient(135deg, #F59E0B, #D97706);
      color: #070B14;
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    }
    .btn-gold:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(245, 158, 11, 0.5);
    }
    .btn-outline {
      background: var(--bg-card);
      color: var(--text);
      border: 1px solid var(--border-bright);
    }
    .btn-outline:hover {
      background: var(--bg-card-hover);
      border-color: var(--cyan);
      color: var(--cyan);
    }

    /* Base URL Strip */
    .base-url-strip {
      margin: 40px auto 50px;
      max-width: 860px;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .base-url-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--gold);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .base-url-code {
      font-family: var(--font-mono);
      font-size: 14.5px;
      color: var(--cyan);
      background: rgba(56, 189, 248, 0.08);
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .copy-btn {
      background: transparent;
      border: 1px solid var(--border-bright);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .copy-btn:hover {
      color: var(--text);
      border-color: var(--text);
    }

    /* Section Headers */
    .section-title {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .section-title i {
      color: var(--gold);
    }
    .section-subtitle {
      color: var(--text-muted);
      font-size: 15px;
      margin-bottom: 28px;
    }

    /* 4-Step Instructions Workflow */
    .steps-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin-bottom: 50px;
    }
    .step-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      position: relative;
      transition: border-color 0.2s, transform 0.2s;
    }
    .step-card:hover {
      border-color: var(--border-bright);
      transform: translateY(-2px);
    }
    .step-num {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: var(--gold-glow);
      color: var(--gold);
      border: 1px solid rgba(245, 158, 11, 0.3);
      font-weight: 800;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 16px;
    }
    .step-card h3 {
      font-size: 17px;
      font-weight: 700;
      margin-bottom: 8px;
    }
    .step-card p {
      font-size: 13.5px;
      color: var(--text-muted);
      line-height: 1.5;
    }
    .step-code {
      margin-top: 12px;
      background: var(--bg-dark);
      padding: 8px 10px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--cyan);
      border: 1px solid var(--border);
      word-break: break-all;
    }

    /* Code Playground Box */
    .code-box {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 50px;
    }
    .code-header {
      background: var(--bg-card);
      border-bottom: 1px solid var(--border);
      padding: 10px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .code-tabs {
      display: flex;
      gap: 8px;
    }
    .code-tab {
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }
    .code-tab.active {
      background: rgba(245, 158, 11, 0.15);
      color: var(--gold);
    }
    .code-content {
      padding: 22px;
      background: #090E1A;
      overflow-x: auto;
    }
    .code-content pre {
      font-family: var(--font-mono);
      font-size: 13.5px;
      line-height: 1.6;
      color: #E2E8F0;
    }

    /* Modules Grid */
    .modules-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 50px;
    }
    .module-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      transition: all 0.2s;
    }
    .module-card:hover {
      border-color: var(--border-bright);
      background: var(--bg-card);
    }
    .module-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    .module-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }
    .module-card h4 {
      font-size: 17px;
      font-weight: 700;
    }
    .module-card p {
      font-size: 13.5px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
    .endpoint-chip-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .endpoint-chip {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(14, 21, 38, 0.8);
      border: 1px solid var(--border);
      padding: 6px 10px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 12px;
    }
    .method {
      font-weight: 700;
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .method-get { background: rgba(56, 189, 248, 0.15); color: var(--cyan); }
    .method-post { background: rgba(16, 185, 129, 0.15); color: var(--emerald); }
    .method-put { background: rgba(245, 158, 11, 0.15); color: var(--gold); }
    .method-delete { background: rgba(239, 68, 68, 0.15); color: #EF4444; }

    /* Quick Filter Catalog Table */
    .catalog-box {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      margin-bottom: 50px;
    }
    .catalog-toolbar {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .search-input {
      background: var(--bg-dark);
      border: 1px solid var(--border-bright);
      padding: 9px 14px;
      border-radius: 8px;
      color: var(--text);
      font-size: 13.5px;
      font-family: var(--font-sans);
      width: 280px;
      outline: none;
    }
    .search-input:focus {
      border-color: var(--gold);
    }
    .table-responsive {
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13.5px;
    }
    th {
      background: var(--bg-card);
      color: var(--text-dim);
      font-weight: 700;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 12px 18px;
      border-bottom: 1px solid var(--border);
    }
    td {
      padding: 12px 18px;
      border-bottom: 1px solid var(--border);
      color: var(--text-muted);
    }
    tr:hover td {
      background: rgba(20, 30, 52, 0.5);
      color: var(--text);
    }
    .endpoint-path {
      font-family: var(--font-mono);
      color: var(--text);
      font-weight: 600;
    }
    .auth-badge {
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(148, 163, 184, 0.1);
      color: var(--text-muted);
    }
    .auth-badge.public {
      background: rgba(16, 185, 129, 0.15);
      color: var(--emerald);
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border);
      padding: 40px 24px;
      text-align: center;
      color: var(--text-dim);
      font-size: 13px;
    }
    .footer-links {
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }
    .footer-links a {
      color: var(--text-muted);
      text-decoration: none;
      font-weight: 600;
      transition: color 0.2s;
    }
    .footer-links a:hover {
      color: var(--gold);
    }

    /* Responsive */
    @media (max-width: 768px) {
      .hero h1 { font-size: 32px; }
      .base-url-strip { flex-direction: column; align-items: flex-start; }
      .search-input { width: 100%; }
      .modules-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="nav">
    <div class="nav-container">
      <a href="/" class="brand">
        <div class="brand-logo">D</div>
        <div class="brand-text">
          <div class="brand-title">DBERT API <span class="badge-api">v__VERSION__</span></div>
          <div class="brand-sub">Sovereign Developer Platform</div>
        </div>
      </a>
      <div class="nav-links">
        <a href="/docs" class="nav-link"><i class="fas fa-bolt"></i> Swagger UI</a>
        <a href="/redoc" class="nav-link"><i class="fas fa-book"></i> ReDoc</a>
        <a href="/openapi.json" class="nav-link"><i class="fas fa-code"></i> OpenAPI JSON</a>
        <a href="https://dbert.in" target="_blank" class="nav-link"><i class="fas fa-external-link-alt"></i> dbert.in</a>
        <a href="/docs" class="nav-cta">Try In Browser</a>
      </div>
    </div>
  </nav>

  <div class="container">

    <!-- Hero -->
    <div class="hero">
      <div class="status-pill">
        <div class="status-dot"></div>
        <span>DBERT API System Operational — __ENVIRONMENT__</span>
      </div>
      <h1>Build Next-Generation Career &amp; AI Ecosystems</h1>
      <p>
        Official developer documentation and instructions for <strong>api.dbert.in</strong>. Programmatically access verified student credentials, 6,600+ vetted tech openings, applicant state machine workflows, guided AI tutoring, and payments.
      </p>
      <div class="hero-actions">
        <a href="/docs" class="btn btn-gold"><i class="fas fa-play"></i> Interactive Swagger UI (/docs)</a>
        <a href="/redoc" class="btn btn-outline"><i class="fas fa-book-open"></i> Technical ReDoc (/redoc)</a>
        <a href="/openapi.json" class="btn btn-outline" target="_blank"><i class="fas fa-download"></i> OpenAPI 3.1 Spec</a>
      </div>
    </div>

    <!-- Base URL Strip -->
    <div class="base-url-strip">
      <div class="base-url-label"><i class="fas fa-globe"></i> Production Base URL</div>
      <div class="base-url-code" id="baseUrlText">https://api.dbert.in/api/v1</div>
      <button class="copy-btn" onclick="copyText('baseUrlText')"><i class="fas fa-copy"></i> Copy Base URL</button>
    </div>

    <!-- Quickstart Instructions: How to Create on DBERT API -->
    <div style="margin-top: 30px;">
      <h2 class="section-title"><i class="fas fa-graduation-cap"></i> Quickstart Instructions: How to Create on DBERT</h2>
      <p class="section-subtitle">Follow these 4 standard steps to authenticate, make requests, and integrate your applications with DBERT APIs.</p>

      <div class="steps-grid">
        <div class="step-card">
          <div class="step-num">1</div>
          <h3>Base URL &amp; Endpoints</h3>
          <p>All REST calls route through <code>https://api.dbert.in</code> over HTTPS with TLS 1.3. Standard API version prefix is <code>/api/v1</code>.</p>
          <div class="step-code">https://api.dbert.in/api/v1/...</div>
        </div>

        <div class="step-card">
          <div class="step-num">2</div>
          <h3>Acquire Access Token</h3>
          <p>Authenticate with your registered email and password to receive a signed JWT Bearer token valid for 1 hour.</p>
          <div class="step-code">POST /api/v1/auth/intern/login</div>
        </div>

        <div class="step-card">
          <div class="step-num">3</div>
          <h3>Include Bearer Header</h3>
          <p>Pass your token in the <code>Authorization</code> HTTP header for protected resources. Public discovery requires no token.</p>
          <div class="step-code">Authorization: Bearer &lt;token&gt;</div>
        </div>

        <div class="step-card">
          <div class="step-num">4</div>
          <h3>Standard JSON Responses</h3>
          <p>All endpoints return idempotent JSON. Use <code>idempotency_key</code> for critical state mutations like submissions and payouts.</p>
          <div class="step-code">Content-Type: application/json</div>
        </div>
      </div>
    </div>

    <!-- Interactive Code Playground -->
    <div class="code-box">
      <div class="code-header">
        <div class="code-tabs">
          <button class="code-tab active" onclick="switchTab('curl')">cURL</button>
          <button class="code-tab" onclick="switchTab('python')">Python (Requests)</button>
          <button class="code-tab" onclick="switchTab('js')">JavaScript (Fetch)</button>
          <button class="code-tab" onclick="switchTab('node')">Node.js (Axios)</button>
        </div>
        <button class="copy-btn" onclick="copyCurrentCode()"><i class="fas fa-copy"></i> Copy Code</button>
      </div>

      <div class="code-content">
        <!-- cURL -->
        <pre id="code-curl"><code># 1. Authenticate to get JWT token
curl -X POST "https://api.dbert.in/api/v1/auth/intern/login" \\
  -H "Content-Type: application/json" \\
  -d '{"email": "candidate@example.com", "password": "your_password"}'

# 2. Query 6,600+ vetted tech internships (Public or Auth)
curl -X GET "https://api.dbert.in/api/v1/marketplace/internships?page=1" \\
  -H "Accept: application/json"

# 3. Verify an official DBERT digital certificate
curl -X GET "https://api.dbert.in/api/v1/certificate/CERT-DBERT-2026-DA-001" \\
  -H "Accept: application/json"</code></pre>

        <!-- Python -->
        <pre id="code-python" style="display:none;"><code>import requests

BASE_URL = "https://api.dbert.in/api/v1"

# 1. Login to obtain access token
login_res = requests.post(
    f"{BASE_URL}/auth/intern/login",
    json={"email": "candidate@example.com", "password": "your_password"}
)
tokens = login_res.json()
token = tokens.get("access_token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 2. Fetch authenticated candidate profile
me_res = requests.get(f"{BASE_URL}/intern/me", headers=headers)
print("Intern Profile:", me_res.json())

# 3. Query active job & internship marketplace
jobs_res = requests.get(f"{BASE_URL}/marketplace/internships?page=1")
print(f"Total Internships: {len(jobs_res.json().get('items', []))}")</code></pre>

        <!-- JavaScript -->
        <pre id="code-js" style="display:none;"><code>const BASE_URL = 'https://api.dbert.in/api/v1';

// 1. Authenticate
async function main() {
  const loginRes = await fetch(`${BASE_URL}/auth/intern/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'candidate@example.com', password: 'your_password' })
  });
  const { access_token } = await loginRes.json();

  // 2. Fetch Verified Credentials
  const certRes = await fetch(`${BASE_URL}/certificate/CERT-DBERT-2026-DA-001`);
  const certData = await certRes.json();
  console.log('Certificate Dossier:', certData);

  // 3. Browse Marketplace
  const marketRes = await fetch(`${BASE_URL}/marketplace/internships?page=1`);
  const opportunities = await marketRes.json();
  console.log('Opportunities:', opportunities);
}

main();</code></pre>

        <!-- Node.js -->
        <pre id="code-node" style="display:none;"><code>const axios = require('axios');

const client = axios.create({
  baseURL: 'https://api.dbert.in/api/v1',
  headers: { 'Content-Type': 'application/json' }
});

async function run() {
  // 1. Health Probe
  const health = await client.get('/health');
  console.log('DBERT API Health:', health.data);

  // 2. Public Openings
  const openings = await client.get('/public/stats/openings');
  console.log('Live Active Openings:', openings.data);
}

run().catch(console.error);</code></pre>
      </div>
    </div>

    <!-- Core API Modules Grid -->
    <div>
      <h2 class="section-title"><i class="fas fa-cubes"></i> Core Architectural Modules</h2>
      <p class="section-subtitle">Explore DBERT's 15 distinct API domains and high-volume microservices.</p>

      <div class="modules-grid">

        <!-- Module 1: Credentials & Verification -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(245, 158, 11, 0.15); color: var(--gold);">
              <i class="fas fa-certificate"></i>
            </div>
            <div>
              <h4>Credentials &amp; Verification</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/certificate, /api/v1/cv</span>
            </div>
          </div>
          <p>Instant verification of official DBERT credentials, 3-document packets (Certificate, Evaluation, LOR), and dynamic intern CV profiles.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>GET /certificate/{cert_id}</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>GET /cv/{slug}</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /cv</span>
              <span class="method method-post">POST</span>
            </div>
          </div>
        </div>

        <!-- Module 2: Job Marketplace -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(56, 189, 248, 0.15); color: var(--cyan);">
              <i class="fas fa-briefcase"></i>
            </div>
            <div>
              <h4>Job &amp; Internship Marketplace</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/marketplace</span>
            </div>
          </div>
          <p>Query over 6,600+ live tech internships and jobs. Filter by technical track (AI/ML, Data Analyst, FSD), work mode, and stipend.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>GET /marketplace/internships</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>GET /marketplace/jobs</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>GET /marketplace/leads</span>
              <span class="method method-get">GET</span>
            </div>
          </div>
        </div>

        <!-- Module 3: Courses & AI Tutor -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(168, 85, 247, 0.15); color: var(--purple);">
              <i class="fas fa-robot"></i>
            </div>
            <div>
              <h4>Courses &amp; AI Guided Tutor</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/courses, /api/v1/learning</span>
            </div>
          </div>
          <p>Structured curriculum delivery, algorithmic day quizzes, pedagogical AI tutor dialog sessions, and student mastery metrics.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>GET /courses</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /courses/{id}/enroll</span>
              <span class="method method-post">POST</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /learning/chat</span>
              <span class="method method-post">POST</span>
            </div>
          </div>
        </div>

        <!-- Module 4: Application State Machine -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald);">
              <i class="fas fa-diagram-project"></i>
            </div>
            <div>
              <h4>Application State Machine</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/applications</span>
            </div>
          </div>
          <p>Idempotent candidate application lifecycles with strict transition rules: <code>applied</code> -> <code>screening</code> -> <code>interview</code> -> <code>enrolled</code>.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>POST /applications/apply</span>
              <span class="method method-post">POST</span>
            </div>
            <div class="endpoint-chip">
              <span>GET /applications/{id}/status</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /applications/{id}/transition</span>
              <span class="method method-post">POST</span>
            </div>
          </div>
        </div>

        <!-- Module 5: College Ambassador -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(245, 158, 11, 0.15); color: var(--gold);">
              <i class="fas fa-bullhorn"></i>
            </div>
            <div>
              <h4>Ambassador &amp; Referral Program</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/ambassador</span>
            </div>
          </div>
          <p>10% cash commission calculation, referral click attribution, wallet balance checks, and Fernet-encrypted UPI withdrawal requests.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>GET /ambassador/stats</span>
              <span class="method method-get">GET</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /ambassador/upi</span>
              <span class="method method-post">POST</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /ambassador/withdraw</span>
              <span class="method method-post">POST</span>
            </div>
          </div>
        </div>

        <!-- Module 6: Payments & Checkout -->
        <div class="module-card">
          <div class="module-header">
            <div class="module-icon" style="background: rgba(16, 185, 129, 0.15); color: var(--emerald);">
              <i class="fas fa-credit-card"></i>
            </div>
            <div>
              <h4>Payments &amp; Ledger Engine</h4>
              <span style="font-size:11px; color:var(--text-dim);">/api/v1/payments</span>
            </div>
          </div>
          <p>Razorpay order generation, HMAC SHA256 payment signature verification, webhook processing, and automatic balance crediting.</p>
          <div class="endpoint-chip-list">
            <div class="endpoint-chip">
              <span>POST /payments/razorpay/create-order</span>
              <span class="method method-post">POST</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /payments/razorpay/verify-payment</span>
              <span class="method method-post">POST</span>
            </div>
            <div class="endpoint-chip">
              <span>POST /payments/razorpay/webhook</span>
              <span class="method method-post">POST</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Live Endpoints Reference Table -->
    <div class="catalog-box">
      <div class="catalog-toolbar">
        <div>
          <h3 style="font-size:17px; font-weight:700;"><i class="fas fa-list-check" style="color:var(--gold); margin-right:8px;"></i> Primary Production Endpoints</h3>
          <span style="font-size:12.5px; color:var(--text-dim);">89 Endpoints available across 15 architectural domains</span>
        </div>
        <input type="text" id="endpointSearch" class="search-input" placeholder="Filter endpoint (e.g., auth, cert, course)..." onkeyup="filterEndpoints()">
      </div>

      <div class="table-responsive">
        <table id="endpointTable">
          <thead>
            <tr>
              <th>Method</th>
              <th>Endpoint Path</th>
              <th>Auth Required</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/health</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Liveness health check probe for load balancers</td>
              <td><a href="/health" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-arrow-up-right-from-square"></i> Test</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/status</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>System metadata, version, and AI service health</td>
              <td><a href="/status" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-arrow-up-right-from-square"></i> Test</a></td>
            </tr>
            <tr>
              <td><span class="method method-post">POST</span></td>
              <td class="endpoint-path">/api/v1/auth/intern/login</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Authenticate intern candidate &amp; receive signed JWT token</td>
              <td><a href="/docs#/Auth%20%26%20Security/intern_login_api_v1_auth_intern_login_post" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-post">POST</span></td>
              <td class="endpoint-path">/api/v1/auth/company/login</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Authenticate hiring company employer &amp; get JWT</td>
              <td><a href="/docs#/Auth%20%26%20Security/company_login_api_v1_auth_company_login_post" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/certificate/{cert_id}</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Instant public digital certificate validation dossier</td>
              <td><a href="/docs#/CV%20%26%20Credentials/verify_certificate_api_v1_certificate__cert_id__get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/cv/{slug}</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Public verified intern CV &amp; portfolio showcase</td>
              <td><a href="/docs#/CV%20%26%20Credentials/get_public_cv_api_v1_cv__slug__get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/marketplace/internships</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Browse 6,600+ curated tech internships with filters</td>
              <td><a href="/docs#/Job%20Marketplace/browse_internships_api_v1_marketplace_internships_get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/courses</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>List active industry sprint courses &amp; syllabi</td>
              <td><a href="/docs#/Courses%20%26%20Guided%20Learning/list_courses_api_v1_courses_get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/intern/me</td>
              <td><span class="auth-badge">Bearer JWT</span></td>
              <td>Retrieve authenticated intern profile &amp; verified track</td>
              <td><a href="/docs#/Intern%20Workspace/get_me_api_v1_intern_me_get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-post">POST</span></td>
              <td class="endpoint-path">/api/v1/applications/apply</td>
              <td><span class="auth-badge">Bearer JWT</span></td>
              <td>Submit internship application with cover letter &amp; CV</td>
              <td><a href="/docs#/Applications/submit_application_api_v1_applications_apply_post" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-post">POST</span></td>
              <td class="endpoint-path">/api/v1/payments/razorpay/create-order</td>
              <td><span class="auth-badge">Bearer JWT</span></td>
              <td>Initialize Razorpay order for enrollment caution fee</td>
              <td><a href="/docs#/Payments/create_razorpay_order_api_v1_payments_razorpay_create_order_post" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
            <tr>
              <td><span class="method method-get">GET</span></td>
              <td class="endpoint-path">/api/v1/public/stats/openings</td>
              <td><span class="auth-badge public">Public</span></td>
              <td>Real-time verified company and opportunity totals</td>
              <td><a href="/docs#/Public%20Discovery/get_live_openings_api_v1_public_stats_openings_get" target="_blank" style="color:var(--cyan); text-decoration:none;"><i class="fas fa-book"></i> Docs</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Error Codes & Architecture -->
    <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:14px; padding:28px; margin-bottom:50px;">
      <h3 style="font-size:18px; font-weight:700; margin-bottom:12px;"><i class="fas fa-shield-halved" style="color:var(--gold); margin-right:8px;"></i> Standard Response &amp; Error Envelopes</h3>
      <p style="color:var(--text-muted); font-size:14px; margin-bottom:16px;">
        All API error responses adhere to the standard JSON envelope structure:
      </p>
      <div style="background:#090E1A; border:1px solid var(--border); border-radius:8px; padding:16px; font-family:var(--font-mono); font-size:13px; color:#E2E8F0; overflow-x:auto;">
{
  "detail": "Descriptive human-readable error explanation",
  "status_code": 401,
  "error_code": "INVALID_CREDENTIALS",
  "request_id": "req-9b81f4a2-11c9-45d2"
}
      </div>
    </div>

  </div>

  <!-- Footer -->
  <footer>
    <div class="footer-links">
      <a href="/docs">Swagger UI</a>
      <a href="/redoc">ReDoc Docs</a>
      <a href="/openapi.json">OpenAPI 3.1</a>
      <a href="/health">Health Probe</a>
      <a href="https://dbert.in" target="_blank">DBERT Sovereign Domain</a>
      <a href="https://lms.dbert.in" target="_blank">DBERT LMS Portal</a>
    </div>
    <div>&copy; 2026 DBERT. Sovereign Domain Authority: <a href="https://dbert.in" style="color:var(--gold); text-decoration:none;">https://dbert.in</a>. All rights reserved.</div>
  </footer>

  <script>
    function copyText(elementId) {
      const text = document.getElementById(elementId).innerText;
      navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard: ' + text);
      }).catch(err => {
        console.error('Failed to copy text: ', err);
      });
    }

    function switchTab(lang) {
      document.querySelectorAll('.code-tab').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');

      const tabs = ['curl', 'python', 'js', 'node'];
      tabs.forEach(t => {
        const el = document.getElementById('code-' + t);
        if (el) el.style.display = (t === lang) ? 'block' : 'none';
      });
    }

    function copyCurrentCode() {
      const tabs = ['curl', 'python', 'js', 'node'];
      for (let t of tabs) {
        const el = document.getElementById('code-' + t);
        if (el && el.style.display !== 'none') {
          navigator.clipboard.writeText(el.innerText).then(() => {
            alert('Code snippet copied to clipboard!');
          });
          return;
        }
      }
    }

    function filterEndpoints() {
      const input = document.getElementById('endpointSearch').value.toLowerCase();
      const rows = document.querySelectorAll('#endpointTable tbody tr');
      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(input) ? '' : 'none';
      });
    }
  </script>
</body>
</html>
"""

def get_developer_hub_html(version: str = "1.0.0", environment: str = "production") -> str:
    """Returns responsive HTML developer portal and API instructions."""
    return _HTML_TEMPLATE.replace("__VERSION__", version).replace("__ENVIRONMENT__", environment.upper())
