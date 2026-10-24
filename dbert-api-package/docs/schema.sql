-- =====================================================================
-- DBERT Complete PostgreSQL 15 Database Schema
-- Auto-extracted and mapped from SQLite internship.db (74 tables)
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS abuse_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    ip TEXT,
    route TEXT,
    bucket TEXT,
    reason TEXT,
    email TEXT
);
CREATE INDEX IF NOT EXISTS idx_abuse_log_id ON abuse_log (id);

CREATE TABLE IF NOT EXISTS ambassador_withdrawals (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT DEFAULT 'pending',
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_by_admin_id BIGINT,
    reviewed_at TIMESTAMPTZ DEFAULT NOW(),
    admin_note TEXT,
    upi_viewed_by TEXT,
    upi_viewed_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_ambassador_withdrawals_intern_id_status ON ambassador_withdrawals (intern_id, status);

CREATE TABLE IF NOT EXISTS application_status_history (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    changed_by TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    reason TEXT,
    request_id TEXT,
    metadata JSONB
);
CREATE INDEX IF NOT EXISTS idx_application_status_history_application_id ON application_status_history (application_id);

CREATE TABLE IF NOT EXISTS applications (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    college TEXT NOT NULL,
    course TEXT NOT NULL,
    semester TEXT NOT NULL,
    year_of_passing TEXT NOT NULL,
    domain TEXT NOT NULL,
    why_join TEXT NOT NULL,
    portfolio TEXT,
    status TEXT DEFAULT 'Apply Pending',
    mentor_note TEXT,
    mentor_email TEXT,
    reviewed_at TIMESTAMPTZ DEFAULT NOW(),
    visitor_id TEXT,
    source TEXT DEFAULT 'web',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    rejected_at TIMESTAMPTZ DEFAULT NOW(),
    enroll_reminders_sent INTEGER DEFAULT 0,
    last_reminder_at TIMESTAMPTZ DEFAULT NOW(),
    intent_answers TEXT
);
CREATE INDEX IF NOT EXISTS idx_applications_email ON applications (email);
CREATE INDEX IF NOT EXISTS idx_applications_status_created_at ON applications (status, created_at);

CREATE TABLE IF NOT EXISTS check_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    email TEXT NOT NULL,
    name TEXT,
    check_count INTEGER,
    ip TEXT
);

CREATE TABLE IF NOT EXISTS coin_ledger_mirror (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    ledger_kind TEXT NOT NULL,
    delta INTEGER NOT NULL,
    balance_after INTEGER,
    reason TEXT,
    event_ts TEXT,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    idem_key TEXT,
    email TEXT
);
CREATE INDEX IF NOT EXISTS idx_coin_ledger_mirror_intern_id_ledger_kind ON coin_ledger_mirror (intern_id, ledger_kind);
CREATE INDEX IF NOT EXISTS idx_coin_ledger_mirror_intern_id_event_ts ON coin_ledger_mirror (intern_id, event_ts);

CREATE TABLE IF NOT EXISTS companies (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    website TEXT,
    about TEXT,
    password_hash TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_companies_email ON companies (email);

CREATE TABLE IF NOT EXISTS cohorts (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    skills JSONB,
    platform TEXT,
    meeting_url TEXT,
    starts_at TIMESTAMPTZ DEFAULT NOW(),
    capacity INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_cohorts_company_id FOREIGN KEY (company_id) REFERENCES companies(id)
);
CREATE INDEX IF NOT EXISTS idx_cohorts_status_starts_at ON cohorts (status, starts_at);
CREATE INDEX IF NOT EXISTS idx_cohorts_company_id_status ON cohorts (company_id, status);

CREATE TABLE IF NOT EXISTS conversations (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    counterparty_type TEXT NOT NULL,
    counterparty_id BIGINT NOT NULL,
    post_id BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_conversations_counterparty_type_counterparty_id_updated_at ON conversations (counterparty_type, counterparty_id, updated_at);
CREATE INDEX IF NOT EXISTS idx_conversations_intern_id_updated_at ON conversations (intern_id, updated_at);

CREATE TABLE IF NOT EXISTS course_payments (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    course_title TEXT,
    amount INTEGER,
    payment_screenshot TEXT,
    status TEXT DEFAULT 'pending',
    admin_note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    platform_commission_pct DOUBLE PRECISION DEFAULT 15.0,
    author_earnings_inr INTEGER DEFAULT 0,
    commission_pct_snapshot DOUBLE PRECISION DEFAULT 0.0,
    commission_amount NUMERIC(12, 2) DEFAULT 0.0,
    payee_type TEXT DEFAULT 'admin',
    settled_at TIMESTAMPTZ DEFAULT NOW(),
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_course_payments_intern_id_course_id ON course_payments (intern_id, course_id);

CREATE TABLE IF NOT EXISTS courses (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT,
    domain TEXT,
    company_id BIGINT,
    is_paid BOOLEAN DEFAULT FALSE,
    price_inr INTEGER DEFAULT 0,
    content_status TEXT DEFAULT 'pending',
    source TEXT DEFAULT 'custom',
    is_active BOOLEAN DEFAULT FALSE,
    payout_note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    level TEXT DEFAULT 'Beginner',
    estimated_hours INTEGER DEFAULT 10,
    author_type TEXT DEFAULT 'admin',
    author_id BIGINT,
    requires_project INTEGER DEFAULT 0,
    banner_gradient TEXT DEFAULT 'linear-gradient(135deg, #8B5CF6, #3B82F6)',
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    program TEXT DEFAULT 'fellowship'
);
CREATE INDEX IF NOT EXISTS idx_courses_content_status_is_active ON courses (content_status, is_active);

CREATE TABLE IF NOT EXISTS course_chapters (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL,
    day_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_course_chapters_course_id FOREIGN KEY (course_id) REFERENCES courses(id)
);
CREATE INDEX IF NOT EXISTS idx_course_chapters_course_id_day_number ON course_chapters (course_id, day_number);

CREATE TABLE IF NOT EXISTS course_day_quizzes (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL,
    day_number INTEGER NOT NULL,
    questions_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_course_day_quizzes_course_id FOREIGN KEY (course_id) REFERENCES courses(id)
);
CREATE INDEX IF NOT EXISTS idx_course_day_quizzes_course_id_day_number ON course_day_quizzes (course_id, day_number);

CREATE TABLE IF NOT EXISTS course_projects (
    id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL,
    brief TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_course_projects_course_id FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE IF NOT EXISTS course_subtopics (
    id BIGSERIAL PRIMARY KEY,
    chapter_id BIGINT NOT NULL,
    sort_order INTEGER NOT NULL,
    title TEXT NOT NULL,
    brief TEXT NOT NULL,
    key_takeaways_json JSONB,
    prompt_seed TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_course_subtopics_chapter_id FOREIGN KEY (chapter_id) REFERENCES course_chapters(id)
);
CREATE INDEX IF NOT EXISTS idx_course_subtopics_chapter_id_sort_order ON course_subtopics (chapter_id, sort_order);

CREATE TABLE IF NOT EXISTS device_profiles (
    id BIGSERIAL PRIMARY KEY,
    visitor_id TEXT,
    email TEXT,
    ip_address TEXT,
    user_agent TEXT,
    screen_res TEXT,
    timezone TEXT,
    language TEXT,
    device_type TEXT,
    referrer TEXT,
    is_return_visit BOOLEAN DEFAULT FALSE,
    visit_count INTEGER DEFAULT 1,
    time_on_page INTEGER DEFAULT 0,
    intent_score INTEGER DEFAULT 0,
    path TEXT,
    last_seen TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_device_profiles_visitor_id ON device_profiles (visitor_id);

CREATE TABLE IF NOT EXISTS ecosystem_spotlights (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL,
    target_brand TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS email_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    email TEXT NOT NULL,
    name TEXT,
    subject TEXT,
    email_sent TEXT DEFAULT 'YES',
    opened_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS enrollment_status_history (
    id BIGSERIAL PRIMARY KEY,
    enrollment_id BIGINT NOT NULL,
    old_status TEXT,
    new_status TEXT NOT NULL,
    changed_by TEXT,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    reason TEXT,
    request_id TEXT,
    metadata JSONB
);
CREATE INDEX IF NOT EXISTS idx_enrollment_status_history_enrollment_id ON enrollment_status_history (enrollment_id);

CREATE TABLE IF NOT EXISTS enrollments (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    college TEXT,
    course TEXT,
    semester TEXT,
    year_of_passing TEXT,
    domain TEXT,
    joining_date TIMESTAMPTZ DEFAULT NOW(),
    batch_label TEXT,
    payment_screenshot TEXT,
    payment_status TEXT,
    admin_note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    product TEXT DEFAULT 'free_deposit',
    amount INTEGER,
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT
);
CREATE INDEX IF NOT EXISTS idx_enrollments_email ON enrollments (email);
CREATE INDEX IF NOT EXISTS idx_enrollments_payment_status_created_at ON enrollments (payment_status, created_at);

CREATE TABLE IF NOT EXISTS event_outbox (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    retry_count INTEGER NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 3,
    next_retry_at TIMESTAMPTZ DEFAULT NOW(),
    last_error TEXT,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_event_outbox_aggregate_type_aggregate_id ON event_outbox (aggregate_type, aggregate_id);
CREATE INDEX IF NOT EXISTS idx_event_outbox_status_next_retry_at ON event_outbox (status, next_retry_at);

CREATE TABLE IF NOT EXISTS gl_concepts (
    concept_id TEXT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    domain TEXT NOT NULL,
    subject TEXT NOT NULL,
    module_id BIGINT,
    subtopic_id BIGINT,
    difficulty INTEGER DEFAULT 1,
    prerequisites_json JSONB DEFAULT '[]',
    learning_objectives_json JSONB DEFAULT '[]',
    assessment_criteria_json JSONB DEFAULT '[]',
    common_misconceptions_json JSONB DEFAULT '[]',
    resources_json JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gl_concepts_subtopic_id ON gl_concepts (subtopic_id);
CREATE INDEX IF NOT EXISTS idx_gl_concepts_domain ON gl_concepts (domain);

CREATE TABLE IF NOT EXISTS gl_course_chunks (
    chunk_id TEXT,
    course_id BIGINT NOT NULL,
    course_version TEXT NOT NULL,
    module_id BIGINT,
    concept_id TEXT,
    subtopic_id BIGINT,
    difficulty INTEGER DEFAULT 1,
    content_type TEXT NOT NULL,
    source TEXT NOT NULL,
    text_content TEXT NOT NULL,
    embedding_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gl_course_chunks_concept_id ON gl_course_chunks (concept_id);
CREATE INDEX IF NOT EXISTS idx_gl_course_chunks_course_id ON gl_course_chunks (course_id);

CREATE TABLE IF NOT EXISTS gl_learning_events (
    id BIGSERIAL PRIMARY KEY,
    event_uuid TEXT NOT NULL,
    student_id BIGINT NOT NULL,
    concept_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gl_learning_events_event_type ON gl_learning_events (event_type);
CREATE INDEX IF NOT EXISTS idx_gl_learning_events_concept_id ON gl_learning_events (concept_id);
CREATE INDEX IF NOT EXISTS idx_gl_learning_events_session_id ON gl_learning_events (session_id);
CREATE INDEX IF NOT EXISTS idx_gl_learning_events_student_id ON gl_learning_events (student_id);

CREATE TABLE IF NOT EXISTS gl_learning_sessions (
    session_id TEXT,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    subtopic_id BIGINT,
    current_concept_id TEXT,
    current_action TEXT DEFAULT 'EXPLAIN',
    action_state_json JSONB DEFAULT '{}',
    idempotency_key TEXT,
    status TEXT DEFAULT 'active',
    last_heartbeat_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_gl_learning_sessions_student_id_course_id ON gl_learning_sessions (student_id, course_id);
CREATE INDEX IF NOT EXISTS idx_gl_learning_sessions_student_id_status ON gl_learning_sessions (student_id, status);

CREATE TABLE IF NOT EXISTS gl_learning_turns (
    id BIGSERIAL PRIMARY KEY,
    turn_uuid TEXT NOT NULL,
    session_id TEXT NOT NULL,
    student_id BIGINT NOT NULL,
    concept_id TEXT NOT NULL,
    idempotency_key TEXT,
    student_input TEXT NOT NULL,
    evaluation_json JSONB NOT NULL,
    recommendation_json JSONB NOT NULL,
    assistant_response TEXT,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_gl_learning_turns_idempotency_key ON gl_learning_turns (idempotency_key);
CREATE INDEX IF NOT EXISTS idx_gl_learning_turns_student_id ON gl_learning_turns (student_id);
CREATE INDEX IF NOT EXISTS idx_gl_learning_turns_session_id ON gl_learning_turns (session_id);

CREATE TABLE IF NOT EXISTS gl_misconception_catalog (
    misconception_id TEXT,
    concept_id TEXT NOT NULL,
    label TEXT NOT NULL,
    pattern_description TEXT NOT NULL,
    remediation_strategy TEXT NOT NULL,
    example_trigger TEXT,
    CONSTRAINT fk_gl_misconception_catalog_concept_id FOREIGN KEY (concept_id) REFERENCES gl_concepts(concept_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_gl_misconception_catalog_concept_id ON gl_misconception_catalog (concept_id);

CREATE TABLE IF NOT EXISTS gl_student_learning_profile (
    student_id BIGSERIAL PRIMARY KEY,
    overall_mastery DOUBLE PRECISION DEFAULT 0.0,
    overall_confidence DOUBLE PRECISION DEFAULT 0.0,
    learning_velocity NUMERIC(12, 2) DEFAULT 1.0,
    preferred_explanation_depth TEXT DEFAULT 'STANDARD',
    practice_strength DOUBLE PRECISION DEFAULT 0.0,
    conceptual_strength DOUBLE PRECISION DEFAULT 0.0,
    recent_struggle_index DOUBLE PRECISION DEFAULT 0.0,
    retention_index DOUBLE PRECISION DEFAULT 1.0,
    mentor_interventions INTEGER DEFAULT 0,
    last_learning_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE IF NOT EXISTS gl_student_mastery (
    student_id BIGINT NOT NULL,
    concept_id TEXT NOT NULL,
    mastery_score DOUBLE PRECISION DEFAULT 0.0,
    mastery_level TEXT DEFAULT 'NOVICE',
    confidence DOUBLE PRECISION DEFAULT 0.0,
    learning_velocity NUMERIC(12, 2) DEFAULT 1.0,
    total_attempts INTEGER DEFAULT 0,
    successful_attempts INTEGER DEFAULT 0,
    consecutive_successes INTEGER DEFAULT 0,
    misconceptions_json JSONB DEFAULT '[]',
    last_evidence_json JSONB DEFAULT '{}',
    last_interaction_at TIMESTAMPTZ DEFAULT NOW(),
    last_review_at TIMESTAMPTZ DEFAULT NOW(),
    next_review_at TIMESTAMPTZ DEFAULT NOW(),
    review_interval_days DOUBLE PRECISION DEFAULT 1.0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    PRIMARY KEY (student_id, concept_id),
    CONSTRAINT fk_gl_student_mastery_concept_id FOREIGN KEY (concept_id) REFERENCES gl_concepts(concept_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_gl_student_mastery_student_id_mastery_level ON gl_student_mastery (student_id, mastery_level);
CREATE INDEX IF NOT EXISTS idx_gl_student_mastery_student_id_next_review_at ON gl_student_mastery (student_id, next_review_at);
CREATE INDEX IF NOT EXISTS idx_gl_student_mastery_student_id ON gl_student_mastery (student_id);

CREATE TABLE IF NOT EXISTS gl_teacher_learning_instructions (
    id BIGSERIAL PRIMARY KEY,
    teacher_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    concept_id TEXT,
    instruction TEXT NOT NULL,
    priority INTEGER DEFAULT 0,
    starts_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_gl_teacher_learning_instructions_student_id_course_id_concept_id ON gl_teacher_learning_instructions (student_id, course_id, concept_id);

CREATE TABLE IF NOT EXISTS intern_accounts (
    id BIGSERIAL PRIMARY KEY,
    application_id BIGINT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    city TEXT,
    college TEXT,
    course TEXT,
    semester TEXT,
    year_of_passing TEXT,
    domain TEXT,
    password_hash TEXT,
    password_set INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    tutor_completion_pct DOUBLE PRECISION DEFAULT 0.0,
    tutor_updated_at TIMESTAMPTZ DEFAULT NOW(),
    tutor_seconds_credited INTEGER DEFAULT 0,
    tutor_week_credited TEXT DEFAULT '',
    linkedin_url TEXT,
    github_url TEXT,
    interview_attempts INTEGER DEFAULT 0,
    interview_last_attempt_at TIMESTAMPTZ DEFAULT NOW(),
    interview_locked INTEGER DEFAULT 0,
    terms_accepted_at TIMESTAMPTZ DEFAULT NOW(),
    newsletter_opt_in INTEGER DEFAULT 0,
    signup_stage INTEGER DEFAULT 3,
    referral_code TEXT,
    referred_by_intern_id BIGINT,
    upi_id_encrypted TEXT,
    email_verified INTEGER DEFAULT 0,
    account_status TEXT,
    visitor_id TEXT DEFAULT NULL,
    program TEXT DEFAULT 'fellowship',
    CONSTRAINT fk_intern_accounts_application_id FOREIGN KEY (application_id) REFERENCES applications(id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_intern_accounts_referral_code ON intern_accounts (referral_code);

CREATE TABLE IF NOT EXISTS attendance (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    week_start TEXT NOT NULL,
    week_end TEXT NOT NULL,
    total_minutes INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT,
    CONSTRAINT fk_attendance_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_attendance_intern_id_week_start ON attendance (intern_id, week_start);

CREATE TABLE IF NOT EXISTS cohort_enrollments (
    id BIGSERIAL PRIMARY KEY,
    cohort_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    reminder_sent INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_cohort_enrollments_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id),
    CONSTRAINT fk_cohort_enrollments_cohort_id FOREIGN KEY (cohort_id) REFERENCES cohorts(id)
);
CREATE INDEX IF NOT EXISTS idx_cohort_enrollments_cohort_id_intern_id ON cohort_enrollments (cohort_id, intern_id);

CREATE TABLE IF NOT EXISTS company_follows (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    company_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_company_follows_company_id FOREIGN KEY (company_id) REFERENCES companies(id),
    CONSTRAINT fk_company_follows_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_company_follows_intern_id ON company_follows (intern_id);
CREATE INDEX IF NOT EXISTS idx_company_follows_company_id ON company_follows (company_id);

CREATE TABLE IF NOT EXISTS course_enrollments (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    enrolled_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ DEFAULT NOW(),
    current_day INTEGER DEFAULT 1,
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT,
    CONSTRAINT fk_course_enrollments_course_id FOREIGN KEY (course_id) REFERENCES courses(id),
    CONSTRAINT fk_course_enrollments_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_course_enrollments_email ON course_enrollments (email);
CREATE INDEX IF NOT EXISTS idx_course_enrollments_intern_id ON course_enrollments (intern_id);

CREATE TABLE IF NOT EXISTS course_subtopic_chats (
    id BIGSERIAL PRIMARY KEY,
    enrollment_id BIGINT NOT NULL,
    subtopic_id BIGINT NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_course_subtopic_chats_subtopic_id FOREIGN KEY (subtopic_id) REFERENCES course_subtopics(id),
    CONSTRAINT fk_course_subtopic_chats_enrollment_id FOREIGN KEY (enrollment_id) REFERENCES course_enrollments(id)
);
CREATE INDEX IF NOT EXISTS idx_course_subtopic_chats_enrollment_id_subtopic_id ON course_subtopic_chats (enrollment_id, subtopic_id);

CREATE TABLE IF NOT EXISTS cvs (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    slug TEXT,
    headline TEXT,
    summary TEXT,
    skills_json JSONB,
    projects_json JSONB,
    experience_json JSONB,
    education_json JSONB,
    links_json JSONB,
    is_public BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_cvs_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_cvs_slug ON cvs (slug);

CREATE TABLE IF NOT EXISTS day_quiz_attempts (
    id BIGSERIAL PRIMARY KEY,
    enrollment_id BIGINT NOT NULL,
    day_quiz_id BIGINT NOT NULL,
    score INTEGER NOT NULL,
    max_score INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    tab_switches INTEGER DEFAULT 0,
    time_taken_sec INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_day_quiz_attempts_day_quiz_id FOREIGN KEY (day_quiz_id) REFERENCES course_day_quizzes(id),
    CONSTRAINT fk_day_quiz_attempts_enrollment_id FOREIGN KEY (enrollment_id) REFERENCES course_enrollments(id)
);
CREATE INDEX IF NOT EXISTS idx_day_quiz_attempts_enrollment_id_day_quiz_id ON day_quiz_attempts (enrollment_id, day_quiz_id);

CREATE TABLE IF NOT EXISTS dbert_fallback_usage (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    usage_date TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_dbert_fallback_usage_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_dbert_fallback_usage_intern_id_usage_date ON dbert_fallback_usage (intern_id, usage_date);

CREATE TABLE IF NOT EXISTS intern_articles (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    domain TEXT,
    title TEXT NOT NULL,
    content_markdown TEXT NOT NULL,
    status TEXT DEFAULT 'DRAFT',
    mentor_feedback TEXT,
    published_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_intern_articles_intern_id_status ON intern_articles (intern_id, status);

CREATE TABLE IF NOT EXISTS intern_certificates (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    course_id BIGINT,
    course_title TEXT,
    cert_id TEXT,
    issued_at TIMESTAMPTZ DEFAULT NOW(),
    url TEXT,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    tier TEXT DEFAULT 'completed',
    email TEXT
);
CREATE INDEX IF NOT EXISTS idx_intern_certificates_intern_id ON intern_certificates (intern_id);

CREATE TABLE IF NOT EXISTS interviews (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    application_id BIGINT,
    domain TEXT,
    attempt_no INTEGER DEFAULT 1,
    status TEXT DEFAULT 'not_started',
    questions_json JSONB,
    answers_json JSONB,
    mentor_assessment_json JSONB,
    candidate_focus_json JSONB,
    github_summary TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    post_id BIGINT,
    time_taken_sec INTEGER DEFAULT 0,
    tab_switches INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_interviews_email ON interviews (email);

CREATE TABLE IF NOT EXISTS mentors (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    domain TEXT NOT NULL,
    password_hash TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL,
    sender_type TEXT NOT NULL,
    sender_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_messages_conversation_id FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id_id ON messages (conversation_id, id);

CREATE TABLE IF NOT EXISTS mobile_refresh_tokens (
    id BIGSERIAL PRIMARY KEY,
    token_hash TEXT NOT NULL,
    intern_id TEXT NOT NULL,
    email TEXT NOT NULL,
    issued_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    revoked INTEGER NOT NULL DEFAULT 0,
    last_used_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_mobile_refresh_tokens_intern_id ON mobile_refresh_tokens (intern_id);
CREATE INDEX IF NOT EXISTS idx_mobile_refresh_tokens_token_hash ON mobile_refresh_tokens (token_hash);

CREATE TABLE IF NOT EXISTS notifications (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    kind TEXT DEFAULT 'general',
    title TEXT NOT NULL,
    body TEXT,
    link TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_notifications_intern_id_is_read_created_at ON notifications (intern_id, is_read, created_at);

CREATE TABLE IF NOT EXISTS password_resets (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    token TEXT NOT NULL,
    expires_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    account_type TEXT NOT NULL DEFAULT 'intern',
    account_id BIGINT,
    used_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payment_events (
    id BIGSERIAL PRIMARY KEY,
    event_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB,
    processed_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'processed'
);
CREATE INDEX IF NOT EXISTS idx_payment_events_event_id ON payment_events (event_id);

CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    mentor_email TEXT NOT NULL,
    intern_name TEXT,
    course_title TEXT,
    amount INTEGER,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS platform_config (
    key TEXT,
    value TEXT NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS post_hire_deposits (
    id BIGSERIAL PRIMARY KEY,
    post_application_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    amount INTEGER,
    payment_screenshot TEXT,
    status TEXT DEFAULT 'pending',
    admin_note TEXT,
    refunded_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_post_hire_deposits_post_application_id ON post_hire_deposits (post_application_id);

CREATE TABLE IF NOT EXISTS posts (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL,
    post_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    title TEXT NOT NULL,
    slug TEXT,
    description TEXT,
    responsibilities TEXT,
    skills JSONB,
    location TEXT,
    work_mode TEXT,
    stipend_min INTEGER,
    stipend_max INTEGER,
    pay_period TEXT,
    is_unpaid BOOLEAN DEFAULT FALSE,
    duration TEXT,
    openings INTEGER DEFAULT 1,
    apply_by TEXT,
    certifications_json JSONB,
    eligibility TEXT,
    status TEXT DEFAULT 'draft',
    published_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW(),
    views INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_posts_company_id FOREIGN KEY (company_id) REFERENCES companies(id)
);
CREATE INDEX IF NOT EXISTS idx_posts_expires_at ON posts (expires_at);
CREATE INDEX IF NOT EXISTS idx_posts_post_type_status_domain ON posts (post_type, status, domain);
CREATE INDEX IF NOT EXISTS idx_posts_company_id_status ON posts (company_id, status);

CREATE TABLE IF NOT EXISTS post_applications (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    comment TEXT NOT NULL,
    cv_id BIGINT,
    status TEXT DEFAULT 'Applied',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    needed_certs_json JSONB,
    decision_note TEXT,
    decided_at TIMESTAMPTZ DEFAULT NOW(),
    notified_at TIMESTAMPTZ DEFAULT NOW(),
    email TEXT,
    CONSTRAINT fk_post_applications_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id),
    CONSTRAINT fk_post_applications_post_id FOREIGN KEY (post_id) REFERENCES posts(id)
);
CREATE INDEX IF NOT EXISTS idx_post_applications_intern_id ON post_applications (intern_id);
CREATE INDEX IF NOT EXISTS idx_post_applications_post_id_id ON post_applications (post_id, id);

CREATE TABLE IF NOT EXISTS post_comments (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_post_comments_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id),
    CONSTRAINT fk_post_comments_post_id FOREIGN KEY (post_id) REFERENCES posts(id)
);
CREATE INDEX IF NOT EXISTS idx_post_comments_post_id_id ON post_comments (post_id, id);

CREATE TABLE IF NOT EXISTS post_questions (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    company_id BIGINT NOT NULL,
    text TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    options TEXT DEFAULT '[]',
    CONSTRAINT fk_post_questions_post_id FOREIGN KEY (post_id) REFERENCES posts(id)
);
CREATE INDEX IF NOT EXISTS idx_post_questions_post_id_sort_order ON post_questions (post_id, sort_order);

CREATE TABLE IF NOT EXISTS rate_events (
    id BIGSERIAL PRIMARY KEY,
    bucket TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rate_events_bucket_created_at ON rate_events (bucket, created_at);

CREATE TABLE IF NOT EXISTS referrals (
    id BIGSERIAL PRIMARY KEY,
    referrer_intern_id BIGINT NOT NULL,
    referred_email TEXT,
    referred_intern_id BIGINT,
    source_code TEXT,
    status TEXT DEFAULT 'clicked',
    flagged INTEGER DEFAULT 0,
    flag_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_referrals_referred_intern_id ON referrals (referred_intern_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referred_intern_id ON referrals (referred_intern_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referrer_intern_id_status ON referrals (referrer_intern_id, status);

CREATE TABLE IF NOT EXISTS scraped_internship_comments (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    intern_name TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_scraped_internship_comments_job_id ON scraped_internship_comments (job_id);

CREATE TABLE IF NOT EXISTS scraped_internships (
    id BIGSERIAL PRIMARY KEY,
    Domain TEXT,
    Company TEXT,
    Role TEXT,
    Location TEXT,
    Is_Remote BOOLEAN DEFAULT FALSE,
    Start_Date TIMESTAMPTZ DEFAULT NOW(),
    End_Date TIMESTAMPTZ DEFAULT NOW(),
    Stipend TEXT,
    URL TEXT,
    Description TEXT,
    Source TEXT,
    Region TEXT,
    Stipend_Normalized TEXT,
    Work_Model TEXT,
    City TEXT,
    Clicks INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS security_deposits (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    amount INTEGER DEFAULT 499,
    payment_screenshot TEXT,
    status TEXT DEFAULT 'pending',
    payment_type TEXT DEFAULT 'pending',
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT,
    admin_note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS signup_otps (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    expires_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_signup_otps_email_is_used_expires_at ON signup_otps (email, is_used, expires_at);

CREATE TABLE IF NOT EXISTS spotlight_clicks (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT,
    spotlight_id BIGINT,
    clicked_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staff_accounts (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    role TEXT DEFAULT "admin"
);
CREATE INDEX IF NOT EXISTS idx_staff_accounts_email ON staff_accounts (email);

CREATE TABLE IF NOT EXISTS mentor_availability_slots (
    id BIGSERIAL PRIMARY KEY,
    mentor_staff_id BIGINT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_mentor_availability_slots_mentor_staff_id FOREIGN KEY (mentor_staff_id) REFERENCES staff_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_mentor_availability_slots_mentor_staff_id_is_booked_start_time ON mentor_availability_slots (mentor_staff_id, is_booked, start_time);

CREATE TABLE IF NOT EXISTS mentor_session_bookings (
    id BIGSERIAL PRIMARY KEY,
    slot_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    meeting_link TEXT,
    status TEXT DEFAULT 'booked',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_mentor_session_bookings_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id),
    CONSTRAINT fk_mentor_session_bookings_slot_id FOREIGN KEY (slot_id) REFERENCES mentor_availability_slots(id)
);
CREATE INDEX IF NOT EXISTS idx_mentor_session_bookings_intern_id_status ON mentor_session_bookings (intern_id, status);

CREATE TABLE IF NOT EXISTS project_submissions (
    id BIGSERIAL PRIMARY KEY,
    enrollment_id BIGINT NOT NULL,
    intern_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    github_repo_url TEXT NOT NULL,
    project_title TEXT NOT NULL,
    project_description TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    reviewed_by_staff_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_project_submissions_reviewed_by_staff_id FOREIGN KEY (reviewed_by_staff_id) REFERENCES staff_accounts(id),
    CONSTRAINT fk_project_submissions_course_id FOREIGN KEY (course_id) REFERENCES courses(id),
    CONSTRAINT fk_project_submissions_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id),
    CONSTRAINT fk_project_submissions_enrollment_id FOREIGN KEY (enrollment_id) REFERENCES course_enrollments(id)
);
CREATE INDEX IF NOT EXISTS idx_project_submissions_intern_id_course_id ON project_submissions (intern_id, course_id);
CREATE INDEX IF NOT EXISTS idx_project_submissions_status_created_at ON project_submissions (status, created_at);

CREATE TABLE IF NOT EXISTS review_log (
    id BIGSERIAL PRIMARY KEY,
    queue_name TEXT NOT NULL,
    staff_id BIGINT NOT NULL,
    subject_type TEXT NOT NULL,
    subject_id BIGINT NOT NULL,
    decision TEXT NOT NULL,
    reason_code TEXT,
    reviewed_input_snapshot TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_review_log_staff_id FOREIGN KEY (staff_id) REFERENCES staff_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_review_log_subject_type_subject_id ON review_log (subject_type, subject_id);
CREATE INDEX IF NOT EXISTS idx_review_log_queue_name_created_at ON review_log (queue_name, created_at);

CREATE TABLE IF NOT EXISTS staff_queue_roles (
    id BIGSERIAL PRIMARY KEY,
    staff_id BIGINT NOT NULL,
    queue_name TEXT NOT NULL,
    CONSTRAINT fk_staff_queue_roles_staff_id FOREIGN KEY (staff_id) REFERENCES staff_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_staff_queue_roles_staff_id_queue_name ON staff_queue_roles (staff_id, queue_name);

CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    coin_reward INTEGER NOT NULL DEFAULT 10,
    is_active BOOLEAN DEFAULT FALSE,
    author_type TEXT DEFAULT 'admin',
    author_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    task_type TEXT DEFAULT 'general',
    target_domain TEXT DEFAULT '',
    payment_type TEXT DEFAULT 'paid',
    submission_type TEXT DEFAULT 'url'
);
CREATE INDEX IF NOT EXISTS idx_tasks_is_active_created_at ON tasks (is_active, created_at);

CREATE TABLE IF NOT EXISTS task_versions (
    id BIGSERIAL PRIMARY KEY,
    task_id BIGINT NOT NULL,
    version_number INTEGER NOT NULL,
    instructions TEXT NOT NULL,
    rubric TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_task_versions_task_id FOREIGN KEY (task_id) REFERENCES tasks(id)
);
CREATE INDEX IF NOT EXISTS idx_task_versions_task_id_version_number ON task_versions (task_id, version_number);

CREATE TABLE IF NOT EXISTS task_submissions (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    task_id BIGINT NOT NULL,
    task_version_id BIGINT NOT NULL,
    submission_content TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    coins_awarded INTEGER DEFAULT 0,
    reviewed_by_staff_id BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    submission_file TEXT DEFAULT '',
    email TEXT,
    CONSTRAINT fk_task_submissions_reviewed_by_staff_id FOREIGN KEY (reviewed_by_staff_id) REFERENCES staff_accounts(id),
    CONSTRAINT fk_task_submissions_task_version_id FOREIGN KEY (task_version_id) REFERENCES task_versions(id),
    CONSTRAINT fk_task_submissions_task_id FOREIGN KEY (task_id) REFERENCES tasks(id),
    CONSTRAINT fk_task_submissions_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_task_submissions_intern_id_task_id ON task_submissions (intern_id, task_id);
CREATE INDEX IF NOT EXISTS idx_task_submissions_status_created_at ON task_submissions (status, created_at);

CREATE TABLE IF NOT EXISTS tutor_progress (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    lessons_json JSONB DEFAULT '[]',
    quizzes_json JSONB DEFAULT '[]',
    projects_json JSONB DEFAULT '[]',
    completion_pct DOUBLE PRECISION DEFAULT 0.0,
    total_lessons INTEGER DEFAULT 0,
    done_lessons INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_tutor_progress_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);

CREATE TABLE IF NOT EXISTS user_api_keys (
    id BIGSERIAL PRIMARY KEY,
    intern_id BIGINT NOT NULL,
    encrypted_key TEXT NOT NULL,
    key_hash TEXT,
    validated_at TIMESTAMPTZ DEFAULT NOW(),
    available_models_json JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT fk_user_api_keys_intern_id FOREIGN KEY (intern_id) REFERENCES intern_accounts(id)
);
CREATE INDEX IF NOT EXISTS idx_user_api_keys_intern_id ON user_api_keys (intern_id);

CREATE TABLE IF NOT EXISTS user_sessions (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    role TEXT DEFAULT 'intern',
    session_token TEXT NOT NULL,
    expires_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    next_url TEXT
);
