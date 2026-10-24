from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text, ForeignKey, JSON, Numeric
from sqlalchemy.sql import func
from backend.core.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=True)
    email = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    domain = Column(String(100), nullable=False)
    questions_json = Column(Text, nullable=False)
    answers_json = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    status = Column(String(50), default="started", index=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    attempt_number = Column(Integer, default=1)
    generator_model = Column(String(100), default="static_bank")
    evaluator_model = Column(String(100), nullable=True)
    github_enriched = Column(Boolean, default=False)
    reviewer_email = Column(String(255), nullable=True)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    domain = Column(String(100), nullable=False)
    thumbnail_url = Column(Text, nullable=True)
    price = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    author_type = Column(String(50), default="admin")
    author_id = Column(Integer, nullable=True)
    total_hours = Column(Float, default=10.0)
    total_lessons = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    instructor_name = Column(String(255), default="DBERT Faculty")
    instructor_bio = Column(Text, nullable=True)
    syllabus_json = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)
    learning_outcomes = Column(Text, nullable=True)
    coins_reward = Column(Integer, default=100)


class CourseChapter(Base):
    __tablename__ = "course_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourseSubtopic(Base):
    __tablename__ = "course_subtopics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    order_index = Column(Integer, default=1)
    duration_minutes = Column(Integer, default=15)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourseSubtopicChat(Base):
    __tablename__ = "course_subtopic_chats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id"), nullable=False, index=True)
    subtopic_id = Column(Integer, ForeignKey("course_subtopics.id"), nullable=False, index=True)
    role = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourseDayQuiz(Base):
    __tablename__ = "course_day_quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, nullable=False, index=True)
    day_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    questions_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DayQuizAttempt(Base):
    __tablename__ = "day_quiz_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id"), nullable=False, index=True)
    day_quiz_id = Column(Integer, ForeignKey("course_day_quizzes.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    max_score = Column(Integer, default=10)
    passed = Column(Boolean, default=False)
    tab_switches = Column(Integer, default=0)
    time_taken_sec = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False, index=True)
    status = Column(String(50), default="active")
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completion_percentage = Column(Float, default=0.0)
    current_day = Column(Integer, default=1)


class CourseProject(Base):
    __tablename__ = "course_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, nullable=False, index=True)
    brief = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, ForeignKey("course_enrollments.id"), nullable=False)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    github_repo_url = Column(Text, nullable=False)
    project_title = Column(Text, nullable=False)
    project_description = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    reviewed_by_staff_id = Column(Integer, ForeignKey("staff_accounts.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GLConcept(Base):
    __tablename__ = "gl_concepts"

    concept_id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    domain = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    module_id = Column(Integer, nullable=True)
    subtopic_id = Column(Integer, nullable=True)
    difficulty = Column(Integer, default=1)
    prerequisites_json = Column(JSON, default=list)
    learning_objectives_json = Column(JSON, default=list)
    assessment_criteria_json = Column(JSON, default=list)
    common_misconceptions_json = Column(JSON, default=list)
    resources_json = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GLLearningSession(Base):
    __tablename__ = "gl_learning_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False)
    concept_id = Column(Integer, nullable=True)
    status = Column(String(50), default="active")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)


class GLLearningTurn(Base):
    __tablename__ = "gl_learning_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, nullable=False, index=True)
    turn_number = Column(Integer, default=1)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    mastery_delta = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GLStudentMastery(Base):
    __tablename__ = "gl_student_mastery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    concept_id = Column(Integer, nullable=False, index=True)
    mastery_score = Column(Float, default=0.0)
    last_reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    next_review_due = Column(DateTime(timezone=True), nullable=True)


class GLCourseChunk(Base):
    __tablename__ = "gl_course_chunks"

    chunk_id = Column(String(100), primary_key=True)
    course_id = Column(Integer, nullable=False)
    course_version = Column(String(50), nullable=False)
    module_id = Column(Integer, nullable=True)
    concept_id = Column(String(100), nullable=True)
    subtopic_id = Column(Integer, nullable=True)
    difficulty = Column(Integer, default=1)
    content_type = Column(String(50), nullable=False)
    source = Column(String(255), nullable=False)
    text_content = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GLLearningEvent(Base):
    __tablename__ = "gl_learning_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_uuid = Column(String(100), nullable=False)
    student_id = Column(Integer, nullable=False)
    concept_id = Column(String(100), nullable=False)
    session_id = Column(String(100), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GLMisconceptionCatalog(Base):
    __tablename__ = "gl_misconception_catalog"

    misconception_id = Column(String(100), primary_key=True)
    concept_id = Column(String(100), ForeignKey("gl_concepts.concept_id", ondelete="CASCADE"), nullable=False)
    label = Column(String(255), nullable=False)
    pattern_description = Column(Text, nullable=False)
    remediation_strategy = Column(Text, nullable=False)
    example_trigger = Column(Text, nullable=True)


class GLStudentLearningProfile(Base):
    __tablename__ = "gl_student_learning_profile"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    overall_mastery = Column(Float, default=0.0)
    overall_confidence = Column(Float, default=0.0)
    learning_velocity = Column(Numeric(12, 2), default=1.0)
    preferred_explanation_depth = Column(String(50), default="STANDARD")
    practice_strength = Column(Float, default=0.0)
    conceptual_strength = Column(Float, default=0.0)
    recent_struggle_index = Column(Float, default=0.0)
    retention_index = Column(Float, default=1.0)
    mentor_interventions = Column(Integer, default=0)
    last_learning_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class GLTeacherLearningInstruction(Base):
    __tablename__ = "gl_teacher_learning_instructions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    course_id = Column(Integer, nullable=False)
    concept_id = Column(String(100), nullable=True)
    instruction = Column(Text, nullable=False)
    priority = Column(Integer, default=0)
    starts_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TutorProgress(Base):
    __tablename__ = "tutor_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    lessons_json = Column(JSON, default=list)
    quizzes_json = Column(JSON, default=list)
    projects_json = Column(JSON, default=list)
    completion_pct = Column(Float, default=0.0)
    total_lessons = Column(Integer, default=0)
    done_lessons = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

