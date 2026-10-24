# DBERT Complete REST API Route Catalog
> **Total Discovered Routes:** 312 across Flask codebase

This document maps every existing Flask endpoint to its target FastAPI endpoint under `/api/v1/`.

## Admin Control Plane (86 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/admin` | `/api/v1/admin` | `admin_page()` | [app.py:4988](file:///apps\portal\app.py#L4988) |
| `GET` | `/admin/abuse-log` | `/api/v1/admin/abuse-log` | `admin_abuse_log()` | [app.py:16477](file:///apps\portal\app.py#L16477) |
| `POST` | `/admin/add-application` | `/api/v1/admin/add-application` | `admin_add_application()` | [app.py:16555](file:///apps\portal\app.py#L16555) |
| `POST` | `/admin/add-mentor` | `/api/v1/admin/add-mentor` | `admin_add_mentor()` | [app.py:16506](file:///apps\portal\app.py#L16506) |
| `GET` | `/admin/ambassador-payouts` | `/api/v1/admin/ambassador-payouts` | `admin_ambassador_payouts()` | [ambassador.py:222](file:///apps\portal\routes\ambassador.py#L222) |
| `POST` | `/admin/ambassador-payouts/<int:wid>/decision` | `/api/v1/admin/ambassador-payouts/<int:wid>/decision` | `admin_ambassador_decision()` | [ambassador.py:261](file:///apps\portal\routes\ambassador.py#L261) |
| `POST` | `/admin/ambassador-payouts/<int:wid>/upi` | `/api/v1/admin/ambassador-payouts/<int:wid>/upi` | `admin_ambassador_reveal_upi()` | [ambassador.py:238](file:///apps\portal\routes\ambassador.py#L238) |
| `POST` | `/admin/application/edit` | `/api/v1/admin/application/edit` | `admin_application_edit()` | [app.py:16323](file:///apps\portal\app.py#L16323) |
| `POST` | `/admin/application/update` | `/api/v1/admin/application/update` | `admin_application_update()` | [app.py:15994](file:///apps\portal\app.py#L15994) |
| `GET` | `/admin/applications` | `/api/v1/admin/applications` | `admin_applications()` | [app.py:15769](file:///apps\portal\app.py#L15769) |
| `POST` | `/admin/applications/bulk-delete` | `/api/v1/admin/applications/bulk-delete` | `admin_applications_bulk_delete()` | [app.py:16667](file:///apps\portal\app.py#L16667) |
| `GET` | `/admin/apply-hotfix-oct` | `/api/v1/admin/apply-hotfix-oct` | `admin_apply_hotfix_oct()` | [app.py:15550](file:///apps\portal\app.py#L15550) |
| `GET` | `/admin/articles` | `/api/v1/admin/articles` | `admin_articles_list()` | [app.py:5864](file:///apps\portal\app.py#L5864) |
| `POST` | `/admin/articles/delete` | `/api/v1/admin/articles/delete` | `admin_articles_delete()` | [app.py:5952](file:///apps\portal\app.py#L5952) |
| `POST` | `/admin/articles/publish` | `/api/v1/admin/articles/publish` | `admin_articles_publish()` | [app.py:5967](file:///apps\portal\app.py#L5967) |
| `POST` | `/admin/articles/review` | `/api/v1/admin/articles/review` | `admin_articles_review()` | [app.py:5873](file:///apps\portal\app.py#L5873) |
| `POST` | `/admin/articles/save` | `/api/v1/admin/articles/save` | `admin_articles_save()` | [app.py:5915](file:///apps\portal\app.py#L5915) |
| `GET` | `/admin/attendance` | `/api/v1/admin/attendance` | `admin_attendance()` | [app.py:15332](file:///apps\portal\app.py#L15332) |
| `GET` | `/admin/backfill-course-certificates` | `/api/v1/admin/backfill-course-certificates` | `admin_backfill_course_certificates()` | [app.py:15695](file:///apps\portal\app.py#L15695) |
| `GET` | `/admin/clean-stale-keys` | `/api/v1/admin/clean-stale-keys` | `admin_clean_stale_keys()` | [app.py:15741](file:///apps\portal\app.py#L15741) |
| `GET` | `/admin/cohorts` | `/api/v1/admin/cohorts` | `admin_cohorts()` | [app.py:10172](file:///apps\portal\app.py#L10172) |
| `POST` | `/admin/cohorts/<int:cohort_id>/review` | `/api/v1/admin/cohorts/<int:cohort_id>/review` | `admin_cohort_review()` | [app.py:10197](file:///apps\portal\app.py#L10197) |
| `GET` | `/admin/companies` | `/api/v1/admin/companies` | `admin_companies()` | [app.py:11874](file:///apps\portal\app.py#L11874) |
| `POST` | `/admin/companies/approve` | `/api/v1/admin/companies/approve` | `admin_company_approve()` | [app.py:11890](file:///apps\portal\app.py#L11890) |
| `POST` | `/admin/companies/approve` | `/api/v1/admin/companies/approve` | `admin_company_approve()` | [admin.py:22](file:///apps\portal\routes\admin.py#L22) |
| `POST` | `/admin/companies/suspend` | `/api/v1/admin/companies/suspend` | `admin_company_suspend()` | [app.py:11904](file:///apps\portal\app.py#L11904) |
| `POST` | `/admin/companies/suspend` | `/api/v1/admin/companies/suspend` | `admin_company_suspend()` | [admin.py:43](file:///apps\portal\routes\admin.py#L43) |
| `GET` | `/admin/course-payments` | `/api/v1/admin/course-payments` | `admin_course_payments()` | [app.py:8354](file:///apps\portal\app.py#L8354) |
| `POST` | `/admin/course-payments/<int:pay_id>/review` | `/api/v1/admin/course-payments/<int:pay_id>/review` | `_signal_tutor_course_unlock()` | [app.py:8372](file:///apps\portal\app.py#L8372) |
| `GET` | `/admin/courses` | `/api/v1/admin/courses` | `admin_courses_list()` | [app.py:9879](file:///apps\portal\app.py#L9879) |
| `POST` | `/admin/courses/<int:course_id>/review` | `/api/v1/admin/courses/<int:course_id>/review` | `admin_course_review()` | [app.py:9901](file:///apps\portal\app.py#L9901) |
| `POST` | `/admin/courses/<int:course_id>/toggle` | `/api/v1/admin/courses/<int:course_id>/toggle` | `admin_course_toggle()` | [app.py:9921](file:///apps\portal\app.py#L9921) |
| `GET` | `/admin/csv/applications` | `/api/v1/admin/csv/applications` | `admin_csv_applications()` | [app.py:17180](file:///apps\portal\app.py#L17180) |
| `GET` | `/admin/csv/attendance` | `/api/v1/admin/csv/attendance` | `admin_csv_attendance()` | [app.py:17274](file:///apps\portal\app.py#L17274) |
| `GET` | `/admin/csv/devices` | `/api/v1/admin/csv/devices` | `admin_csv_devices()` | [app.py:17323](file:///apps\portal\app.py#L17323) |
| `GET` | `/admin/csv/enrollments` | `/api/v1/admin/csv/enrollments` | `admin_csv_enrollments()` | [app.py:17209](file:///apps\portal\app.py#L17209) |
| `GET` | `/admin/csv/interviews` | `/api/v1/admin/csv/interviews` | `admin_csv_interviews()` | [app.py:17347](file:///apps\portal\app.py#L17347) |
| `POST` | `/admin/csv/upload` | `/api/v1/admin/csv/upload` | `admin_csv_upload_legacy()` | [app.py:17150](file:///apps\portal\app.py#L17150) |
| `POST` | `/admin/delete-application` | `/api/v1/admin/delete-application` | `admin_delete_application()` | [app.py:16628](file:///apps\portal\app.py#L16628) |
| `POST` | `/admin/delete-mentor` | `/api/v1/admin/delete-mentor` | `admin_delete_mentor()` | [app.py:16537](file:///apps\portal\app.py#L16537) |
| `GET` | `/admin/devices` | `/api/v1/admin/devices` | `admin_devices()` | [app.py:16464](file:///apps\portal\app.py#L16464) |
| `POST` | `/admin/devices/bulk-delete` | `/api/v1/admin/devices/bulk-delete` | `admin_devices_bulk_delete()` | [app.py:16725](file:///apps\portal\app.py#L16725) |
| `GET` | `/admin/diag` | `/api/v1/admin/diag` | `admin_diag()` | [app.py:18072](file:///apps\portal\app.py#L18072) |
| `POST` | `/admin/enrollment/bulk-review` | `/api/v1/admin/enrollment/bulk-review` | `admin_enrollment_bulk_review()` | [app.py:15945](file:///apps\portal\app.py#L15945) |
| `POST` | `/admin/enrollment/edit` | `/api/v1/admin/enrollment/edit` | `admin_enrollment_edit()` | [app.py:16257](file:///apps\portal\app.py#L16257) |
| `POST` | `/admin/enrollment/review` | `/api/v1/admin/enrollment/review` | `admin_enrollment_review()` | [app.py:15901](file:///apps\portal\app.py#L15901) |
| `GET` | `/admin/enrollments` | `/api/v1/admin/enrollments` | `admin_enrollments()` | [app.py:15826](file:///apps\portal\app.py#L15826) |
| `POST` | `/admin/enrollments/bulk-delete` | `/api/v1/admin/enrollments/bulk-delete` | `admin_enrollments_bulk_delete()` | [app.py:16689](file:///apps\portal\app.py#L16689) |
| `GET` | `/admin/heal` | `/api/v1/admin/heal` | `admin_heal()` | [app.py:18141](file:///apps\portal\app.py#L18141) |
| `GET` | `/admin/insights/content` | `/api/v1/admin/insights/content` | `admin_insights_content()` | [app.py:15234](file:///apps\portal\app.py#L15234) |
| `GET` | `/admin/integrity-dashboard` | `/api/v1/admin/integrity-dashboard` | `admin_integrity_dashboard()` | [admin.py:77](file:///apps\portal\routes\admin.py#L77) |
| `POST` | `/admin/integrity/heal` | `/api/v1/admin/integrity/heal` | `admin_integrity_heal()` | [admin.py:112](file:///apps\portal\routes\admin.py#L112) |
| `POST` | `/admin/intern/edit` | `/api/v1/admin/intern/edit` | `admin_intern_edit()` | [app.py:16172](file:///apps\portal\app.py#L16172) |
| `GET` | `/admin/interview/<path:email>` | `/api/v1/admin/interview/<path:email>` | `admin_interview_view()` | [app.py:13349](file:///apps\portal\app.py#L13349) |
| `POST` | `/admin/interview/bulk-reset` | `/api/v1/admin/interview/bulk-reset` | `admin_interview_bulk_reset()` | [app.py:13421](file:///apps\portal\app.py#L13421) |
| `POST` | `/admin/interview/reset` | `/api/v1/admin/interview/reset` | `admin_interview_reset()` | [app.py:13402](file:///apps\portal\app.py#L13402) |
| `GET` | `/admin/learning-analytics` | `/api/v1/admin/learning-analytics` | `admin_learning_analytics()` | [app.py:6204](file:///apps\portal\app.py#L6204) |
| `GET` | `/admin/ledger` | `/api/v1/admin/ledger` | `admin_ledger()` | [app.py:8745](file:///apps\portal\app.py#L8745) |
| `GET`, `POST` | `/admin/logout` | `/api/v1/admin/logout` | `admin_logout()` | [app.py:5000](file:///apps\portal\app.py#L5000) |
| `GET` | `/admin/masterclass/registrations` | `/api/v1/admin/masterclass/registrations` | `admin_masterclass_registrations()` | [masterclass.py:189](file:///apps\portal\routes\masterclass.py#L189) |
| `GET` | `/admin/mentors` | `/api/v1/admin/mentors` | `admin_mentors()` | [app.py:16493](file:///apps\portal\app.py#L16493) |
| `POST` | `/admin/mentors/bulk-delete` | `/api/v1/admin/mentors/bulk-delete` | `admin_mentors_bulk_delete()` | [app.py:16707](file:///apps\portal\app.py#L16707) |
| `GET` | `/admin/post-hire-deposits` | `/api/v1/admin/post-hire-deposits` | `admin_post_hire_deposits()` | [app.py:8276](file:///apps\portal\app.py#L8276) |
| `POST` | `/admin/post-hire-deposits/<int:dep_id>/refund` | `/api/v1/admin/post-hire-deposits/<int:dep_id>/refund` | `admin_post_hire_deposit_refund()` | [app.py:8334](file:///apps\portal\app.py#L8334) |
| `POST` | `/admin/post-hire-deposits/<int:dep_id>/review` | `/api/v1/admin/post-hire-deposits/<int:dep_id>/review` | `admin_post_hire_deposit_review()` | [app.py:8307](file:///apps\portal\app.py#L8307) |
| `GET` | `/admin/post-questions` | `/api/v1/admin/post-questions` | `admin_post_questions()` | [app.py:11919](file:///apps\portal\app.py#L11919) |
| `POST` | `/admin/post-questions/<int:question_id>/review` | `/api/v1/admin/post-questions/<int:question_id>/review` | `admin_post_question_review()` | [app.py:11938](file:///apps\portal\app.py#L11938) |
| `POST` | `/admin/push-test` | `/api/v1/admin/push-test` | `admin_push_test()` | [app.py:16141](file:///apps\portal\app.py#L16141) |
| `GET` | `/admin/screenshot/<filename>` | `/api/v1/admin/screenshot/<filename>` | `admin_screenshot()` | [app.py:17384](file:///apps\portal\app.py#L17384) |
| `GET` | `/admin/seed-gl-concepts` | `/api/v1/admin/seed-gl-concepts` | `admin_seed_gl_concepts()` | [app.py:15618](file:///apps\portal\app.py#L15618) |
| `GET` | `/admin/sourcing-dashboard` | `/api/v1/admin/sourcing-dashboard` | `admin_sourcing_dashboard()` | [app.py:18168](file:///apps\portal\app.py#L18168) |
| `GET` | `/admin/sourcing/click/<int:job_id>` | `/api/v1/admin/sourcing/click/<int:job_id>` | `admin_sourcing_click()` | [app.py:18241](file:///apps\portal\app.py#L18241) |
| `GET` | `/admin/spotlights` | `/api/v1/admin/spotlights` | `admin_spotlights_list()` | [app.py:6131](file:///apps\portal\app.py#L6131) |
| `POST` | `/admin/spotlights/add` | `/api/v1/admin/spotlights/add` | `admin_spotlights_add()` | [app.py:6141](file:///apps\portal\app.py#L6141) |
| `POST` | `/admin/spotlights/delete` | `/api/v1/admin/spotlights/delete` | `admin_spotlights_delete()` | [app.py:6188](file:///apps\portal\app.py#L6188) |
| `POST` | `/admin/spotlights/edit` | `/api/v1/admin/spotlights/edit` | `admin_spotlights_edit()` | [app.py:6164](file:///apps\portal\app.py#L6164) |
| `GET` | `/admin/stats` | `/api/v1/admin/stats` | `admin_stats()` | [app.py:15262](file:///apps\portal\app.py#L15262) |
| `GET` | `/admin/sync_attendance` | `/api/v1/admin/sync_attendance` | `admin_sync_attendance()` | [app.py:15450](file:///apps\portal\app.py#L15450) |
| `GET` | `/admin/telemetry` | `/api/v1/admin/telemetry` | `admin_telemetry()` | [app.py:17852](file:///apps\portal\app.py#L17852) |
| `GET` | `/admin/telemetry` | `/api/v1/admin/telemetry` | `admin_telemetry()` | [admin.py:64](file:///apps\portal\routes\admin.py#L64) |
| `POST` | `/admin/update-application-status` | `/api/v1/admin/update-application-status` | `admin_update_application_status()` | [app.py:16033](file:///apps\portal\app.py#L16033) |
| `POST` | `/admin/update-enrollment-status` | `/api/v1/admin/update-enrollment-status` | `admin_update_enrollment_status()` | [app.py:16083](file:///apps\portal\app.py#L16083) |
| `POST` | `/admin/upload-csv` | `/api/v1/admin/upload-csv` | `admin_upload_csv()` | [app.py:16961](file:///apps\portal\app.py#L16961) |
| `POST` | `/admin/upload-csv-accepted` | `/api/v1/admin/upload-csv-accepted` | `admin_upload_csv_accepted()` | [app.py:17116](file:///apps\portal\app.py#L17116) |
| `GET` | `/admin/users` | `/api/v1/admin/users` | `admin_users()` | [app.py:16383](file:///apps\portal\app.py#L16383) |
| `POST` | `/admin/users/bulk-delete` | `/api/v1/admin/users/bulk-delete` | `admin_users_bulk_delete()` | [app.py:16743](file:///apps\portal\app.py#L16743) |

## Applications & Admissions (5 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `POST` | `/apply` | `/api/v1/apply` | `apply()` | [app.py:8825](file:///apps\portal\app.py#L8825) |
| `GET` | `/apply-token` | `/api/v1/apply-token` | `apply_token()` | [app.py:8810](file:///apps\portal\app.py#L8810) |
| `GET` | `/apply/<int:post_id>` | `/api/v1/apply/<int:post_id>` | `apply_entry()` | [app.py:11580](file:///apps\portal\app.py#L11580) |
| `POST` | `/enroll` | `/api/v1/enroll` | `enroll()` | [app.py:13703](file:///apps\portal\app.py#L13703) |
| `GET` | `/enrollment-count` | `/api/v1/enrollment-count` | `enrollment_count()` | [app.py:4862](file:///apps\portal\app.py#L4862) |

## Auth & Security (25 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/admin-login` | `/api/v1/admin-login` | `admin_login_page()` | [app.py:4909](file:///apps\portal\app.py#L4909) |
| `GET` | `/admin/csv/incomplete-signups` | `/api/v1/admin/csv/incomplete-signups` | `admin_csv_incomplete_signups()` | [app.py:17234](file:///apps\portal\app.py#L17234) |
| `GET`, `POST` | `/admin/login` | `/api/v1/admin/login` | `admin_login()` | [app.py:4920](file:///apps\portal\app.py#L4920) |
| `POST` | `/admin/reset-intern-password` | `/api/v1/admin/reset-intern-password` | `admin_reset_intern_password()` | [app.py:16846](file:///apps\portal\app.py#L16846) |
| `POST` | `/auth/send-otp` | `/api/v1/auth/send-otp` | `auth_send_otp()` | [app.py:8110](file:///apps\portal\app.py#L8110) |
| `POST` | `/auth/verify-otp` | `/api/v1/auth/verify-otp` | `auth_verify_otp()` | [app.py:8182](file:///apps\portal\app.py#L8182) |
| `POST` | `/company/change-password` | `/api/v1/company/change-password` | `company_change_password()` | [app.py:13543](file:///apps\portal\app.py#L13543) |
| `GET` | `/company/login` | `/api/v1/company/login` | `company_login_page()` | [app.py:9592](file:///apps\portal\app.py#L9592) |
| `POST` | `/company/login` | `/api/v1/company/login` | `company_login()` | [app.py:9597](file:///apps\portal\app.py#L9597) |
| `GET` | `/company/signup` | `/api/v1/company/signup` | `company_signup_page()` | [app.py:9546](file:///apps\portal\app.py#L9546) |
| `POST` | `/company/signup` | `/api/v1/company/signup` | `company_signup()` | [app.py:9551](file:///apps\portal\app.py#L9551) |
| `POST` | `/forgot-password` | `/api/v1/forgot-password` | `forgot_password()` | [app.py:17561](file:///apps\portal\app.py#L17561) |
| `POST` | `/intern/change-password` | `/api/v1/intern/change-password` | `intern_change_password()` | [app.py:13505](file:///apps\portal\app.py#L13505) |
| `POST` | `/intern/login` | `/api/v1/intern/login` | `intern_login()` | [app.py:9435](file:///apps\portal\app.py#L9435) |
| `POST` | `/intern/login` | `/api/v1/intern/login` | `intern_login()` | [auth.py:42](file:///apps\portal\routes\auth.py#L42) |
| `POST` | `/mentor/login` | `/api/v1/mentor/login` | `mentor_login()` | [app.py:12494](file:///apps\portal\app.py#L12494) |
| `GET` | `/reset` | `/api/v1/reset` | `reset_password_page()` | [app.py:4834](file:///apps\portal\app.py#L4834) |
| `POST` | `/reset-password` | `/api/v1/reset-password` | `reset_password()` | [app.py:17656](file:///apps\portal\app.py#L17656) |
| `POST` | `/set-password` | `/api/v1/set-password` | `set_password()` | [app.py:17557](file:///apps\portal\app.py#L17557) |
| `GET` | `/signin` | `/api/v1/signin` | `signin_page()` | [app.py:4754](file:///apps\portal\app.py#L4754) |
| `GET` | `/signup` | `/api/v1/signup` | `signup_page()` | [app.py:4760](file:///apps\portal\app.py#L4760) |
| `POST` | `/signup/stage1` | `/api/v1/signup/stage1` | `signup_stage1()` | [app.py:9147](file:///apps\portal\app.py#L9147) |
| `POST` | `/signup/stage2` | `/api/v1/signup/stage2` | `signup_stage2()` | [app.py:9269](file:///apps\portal\app.py#L9269) |
| `POST` | `/signup/stage3` | `/api/v1/signup/stage3` | `signup_stage3()` | [app.py:9319](file:///apps\portal\app.py#L9319) |
| `GET`, `POST` | `/staff/login` | `/api/v1/staff/login` | `staff_login()` | [app.py:6676](file:///apps\portal\app.py#L6676) |

## CV & Credential Verification (7 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/certificate/<cert_id>` | `/api/v1/certificate/<cert_id>` | `portal_print_certificate()` | [app.py:8709](file:///apps\portal\app.py#L8709) |
| `GET` | `/cv/<slug>` | `/api/v1/cv/<slug>` | `cv_public()` | [app.py:12464](file:///apps\portal\app.py#L12464) |
| `GET` | `/cv/<slug>.pdf` | `/api/v1/cv/<slug>.pdf` | `cv_pdf()` | [app.py:12442](file:///apps\portal\app.py#L12442) |
| `GET` | `/portal/certificate/<cert_id>` | `/api/v1/portal/certificate/<cert_id>` | `portal_view_certificate()` | [app.py:8726](file:///apps\portal\app.py#L8726) |
| `GET` | `/portal/certificate/<cert_id>/print` | `/api/v1/portal/certificate/<cert_id>/print` | `portal_print_certificate()` | [app.py:8708](file:///apps\portal\app.py#L8708) |
| `GET` | `/portal/cv` | `/api/v1/portal/cv` | `portal_cv_editor()` | [app.py:12386](file:///apps\portal\app.py#L12386) |
| `POST` | `/portal/cv` | `/api/v1/portal/cv` | `portal_cv_save()` | [app.py:12408](file:///apps\portal\app.py#L12408) |

## Campus Ambassador (1 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/ambassador` | `/api/v1/ambassador` | `ambassador_page()` | [ambassador.py:20](file:///apps\portal\routes\ambassador.py#L20) |

## Cohorts (1 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `POST` | `/cohorts/<int:cohort_id>/enroll` | `/api/v1/cohorts/<int:cohort_id>/enroll` | `cohort_enroll()` | [app.py:10252](file:///apps\portal\app.py#L10252) |

## Company & Employer Portal (23 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/companies/<slug>` | `/api/v1/companies/<slug>` | `company_profile()` | [app.py:10351](file:///apps\portal\app.py#L10351) |
| `GET` | `/company` | `/api/v1/company` | `company_dashboard()` | [app.py:9697](file:///apps\portal\app.py#L9697) |
| `POST` | `/company/applications/<int:app_id>/status` | `/api/v1/company/applications/<int:app_id>/status` | `company_app_status()` | [app.py:11790](file:///apps\portal\app.py#L11790) |
| `POST` | `/company/applications/<int:app_id>/status` | `/api/v1/company/applications/<int:app_id>/status` | `company_app_status()` | [company.py:20](file:///apps\portal\routes\company.py#L20) |
| `GET` | `/company/cohorts` | `/api/v1/company/cohorts` | `company_cohorts()` | [app.py:10126](file:///apps\portal\app.py#L10126) |
| `POST` | `/company/cohorts` | `/api/v1/company/cohorts` | `company_cohort_create()` | [app.py:10139](file:///apps\portal\app.py#L10139) |
| `POST` | `/company/courses` | `/api/v1/company/courses` | `company_course_create()` | [app.py:9816](file:///apps\portal\app.py#L9816) |
| `GET` | `/company/earnings` | `/api/v1/company/earnings` | `company_earnings()` | [app.py:8030](file:///apps\portal\app.py#L8030) |
| `POST` | `/company/logout` | `/api/v1/company/logout` | `company_logout()` | [app.py:9633](file:///apps\portal\app.py#L9633) |
| `POST` | `/company/posts` | `/api/v1/company/posts` | `company_post_save()` | [app.py:9733](file:///apps\portal\app.py#L9733) |
| `POST` | `/company/posts` | `/api/v1/company/posts` | `company_post_save()` | [marketplace.py:26](file:///apps\portal\routes\marketplace.py#L26) |
| `GET` | `/company/posts/<int:post_id>` | `/api/v1/company/posts/<int:post_id>` | `company_post_manage()` | [app.py:9718](file:///apps\portal\app.py#L9718) |
| `GET` | `/company/posts/<int:post_id>/applicants` | `/api/v1/company/posts/<int:post_id>/applicants` | `company_applicants()` | [app.py:11740](file:///apps\portal\app.py#L11740) |
| `POST` | `/company/posts/<int:post_id>/delete` | `/api/v1/company/posts/<int:post_id>/delete` | `company_post_delete()` | [app.py:10070](file:///apps\portal\app.py#L10070) |
| `POST` | `/company/posts/<int:post_id>/delete` | `/api/v1/company/posts/<int:post_id>/delete` | `company_post_delete()` | [marketplace.py:136](file:///apps\portal\routes\marketplace.py#L136) |
| `POST` | `/company/posts/<int:post_id>/publish` | `/api/v1/company/posts/<int:post_id>/publish` | `company_post_publish()` | [app.py:9993](file:///apps\portal\app.py#L9993) |
| `POST` | `/company/posts/<int:post_id>/publish` | `/api/v1/company/posts/<int:post_id>/publish` | `company_post_publish()` | [marketplace.py:97](file:///apps\portal\routes\marketplace.py#L97) |
| `GET` | `/company/posts/<int:post_id>/questions` | `/api/v1/company/posts/<int:post_id>/questions` | `company_post_questions_list()` | [app.py:9935](file:///apps\portal\app.py#L9935) |
| `POST` | `/company/posts/<int:post_id>/questions` | `/api/v1/company/posts/<int:post_id>/questions` | `company_post_questions_save()` | [app.py:9954](file:///apps\portal\app.py#L9954) |
| `POST` | `/company/posts/<int:post_id>/unpublish` | `/api/v1/company/posts/<int:post_id>/unpublish` | `company_post_unpublish()` | [app.py:10048](file:///apps\portal\app.py#L10048) |
| `POST` | `/company/posts/<int:post_id>/unpublish` | `/api/v1/company/posts/<int:post_id>/unpublish` | `company_post_unpublish()` | [marketplace.py:119](file:///apps\portal\routes\marketplace.py#L119) |
| `GET` | `/company/posts/new` | `/api/v1/company/posts/new` | `company_post_new()` | [app.py:9710](file:///apps\portal\app.py#L9710) |
| `GET`, `POST` | `/company/profile` | `/api/v1/company/profile` | `company_profile_edit()` | [app.py:9665](file:///apps\portal\app.py#L9665) |

## Courses & Guided Learning (GL) (18 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/api/learning/v2/concept-tree/<int:course_id>` | `/api/v1/api/learning/v2/concept-tree/<int:course_id>` | `api_learning_v2_concept_tree()` | [app.py:5829](file:///apps\portal\app.py#L5829) |
| `GET` | `/api/learning/v2/concept-tree/<int:course_id>` | `/api/v1/api/learning/v2/concept-tree/<int:course_id>` | `api_learning_v2_concept_tree()` | [learning.py:89](file:///apps\portal\routes\learning.py#L89) |
| `GET` | `/api/learning/v2/reviews-due` | `/api/v1/api/learning/v2/reviews-due` | `api_learning_v2_reviews_due()` | [app.py:5815](file:///apps\portal\app.py#L5815) |
| `GET` | `/api/learning/v2/reviews-due` | `/api/v1/api/learning/v2/reviews-due` | `api_learning_v2_reviews_due()` | [learning.py:76](file:///apps\portal\routes\learning.py#L76) |
| `POST` | `/api/learning/v2/session` | `/api/v1/api/learning/v2/session` | `api_learning_v2_session()` | [app.py:5732](file:///apps\portal\app.py#L5732) |
| `POST` | `/api/learning/v2/session` | `/api/v1/api/learning/v2/session` | `api_learning_v2_session()` | [learning.py:21](file:///apps\portal\routes\learning.py#L21) |
| `POST` | `/api/learning/v2/turn` | `/api/v1/api/learning/v2/turn` | `api_learning_v2_turn()` | [app.py:5761](file:///apps\portal\app.py#L5761) |
| `POST` | `/api/learning/v2/turn` | `/api/v1/api/learning/v2/turn` | `api_learning_v2_turn()` | [learning.py:49](file:///apps\portal\routes\learning.py#L49) |
| `GET` | `/courses` | `/api/v1/courses` | `courses_catalog()` | [app.py:5056](file:///apps\portal\app.py#L5056) |
| `GET` | `/courses/<int:course_id>` | `/api/v1/courses/<int:course_id>` | `course_detail()` | [app.py:5112](file:///apps\portal\app.py#L5112) |
| `POST` | `/courses/<int:course_id>/enroll` | `/api/v1/courses/<int:course_id>/enroll` | `course_enroll()` | [app.py:5167](file:///apps\portal\app.py#L5167) |
| `POST` | `/courses/<int:course_id>/enroll-coins` | `/api/v1/courses/<int:course_id>/enroll-coins` | `course_enroll_coins()` | [app.py:7733](file:///apps\portal\app.py#L7733) |
| `GET` | `/courses/<int:course_id>/learn` | `/api/v1/courses/<int:course_id>/learn` | `course_learn_page()` | [app.py:5631](file:///apps\portal\app.py#L5631) |
| `GET` | `/courses/<int:course_id>/quiz/<int:day_number>` | `/api/v1/courses/<int:course_id>/quiz/<int:day_number>` | `course_quiz_page()` | [app.py:6314](file:///apps\portal\app.py#L6314) |
| `POST` | `/courses/<int:course_id>/quiz/<int:day_number>/submit` | `/api/v1/courses/<int:course_id>/quiz/<int:day_number>/submit` | `course_quiz_submit()` | [app.py:6434](file:///apps\portal\app.py#L6434) |
| `GET`, `POST` | `/courses/<int:course_id>/submit-project` | `/api/v1/courses/<int:course_id>/submit-project` | `course_submit_project()` | [app.py:6779](file:///apps\portal\app.py#L6779) |
| `GET` | `/courses/<int:course_id>/subtopic/<int:subtopic_id>` | `/api/v1/courses/<int:course_id>/subtopic/<int:subtopic_id>` | `course_subtopic_detail()` | [app.py:5250](file:///apps\portal\app.py#L5250) |
| `POST` | `/courses/<int:course_id>/subtopic/<int:subtopic_id>/chat` | `/api/v1/courses/<int:course_id>/subtopic/<int:subtopic_id>/chat` | `course_subtopic_chat()` | [app.py:5338](file:///apps\portal\app.py#L5338) |

## Direct Messaging (10 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/messages` | `/api/v1/messages` | `messages_inbox()` | [app.py:12064](file:///apps\portal\app.py#L12064) |
| `GET` | `/messages/<int:conv_id>` | `/api/v1/messages/<int:conv_id>` | `messages_thread()` | [app.py:12113](file:///apps\portal\app.py#L12113) |
| `GET` | `/messages/<int:conv_id>/poll` | `/api/v1/messages/<int:conv_id>/poll` | `messages_poll()` | [app.py:12161](file:///apps\portal\app.py#L12161) |
| `POST` | `/messages/<int:conv_id>/send` | `/api/v1/messages/<int:conv_id>/send` | `messages_send()` | [app.py:12132](file:///apps\portal\app.py#L12132) |
| `POST` | `/messages/start` | `/api/v1/messages/start` | `messages_start()` | [app.py:12084](file:///apps\portal\app.py#L12084) |
| `GET` | `/portal/messages` | `/api/v1/portal/messages` | `messages_inbox()` | [app.py:12065](file:///apps\portal\app.py#L12065) |
| `GET` | `/portal/messages/<int:conv_id>` | `/api/v1/portal/messages/<int:conv_id>` | `messages_thread()` | [app.py:12114](file:///apps\portal\app.py#L12114) |
| `GET` | `/portal/messages/<int:conv_id>/poll` | `/api/v1/portal/messages/<int:conv_id>/poll` | `messages_poll()` | [app.py:12162](file:///apps\portal\app.py#L12162) |
| `POST` | `/portal/messages/<int:conv_id>/send` | `/api/v1/portal/messages/<int:conv_id>/send` | `messages_send()` | [app.py:12133](file:///apps\portal\app.py#L12133) |
| `POST` | `/portal/messages/start` | `/api/v1/portal/messages/start` | `messages_start()` | [app.py:12085](file:///apps\portal\app.py#L12085) |

## Infrastructure & Health (6 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/ads.txt` | `/ads.txt` | `ads_txt()` | [app.py:4676](file:///apps\portal\app.py#L4676) |
| `GET` | `/health` | `/health` | `health()` | [app.py:17829](file:///apps\portal\app.py#L17829) |
| `GET` | `/ready` | `/ready` | `ready()` | [app.py:17837](file:///apps\portal\app.py#L17837) |
| `GET` | `/robots.txt` | `/robots.txt` | `robots_txt()` | [app.py:4632](file:///apps\portal\app.py#L4632) |
| `GET` | `/sitemap.xml` | `/sitemap.xml` | `sitemap_xml()` | [app.py:4692](file:///apps\portal\app.py#L4692) |
| `GET` | `/status` | `/status` | `check_status()` | [app.py:15095](file:///apps\portal\app.py#L15095) |

## Intern Workspace (49 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `POST` | `/attendance/ping` | `/api/v1/attendance/ping` | `attendance_ping()` | [app.py:14627](file:///apps\portal\app.py#L14627) |
| `GET` | `/dashboard` | `/api/v1/dashboard` | `dashboard_page()` | [app.py:4880](file:///apps\portal\app.py#L4880) |
| `GET` | `/intern/ambassador` | `/api/v1/intern/ambassador` | `intern_ambassador()` | [ambassador.py:57](file:///apps\portal\routes\ambassador.py#L57) |
| `POST` | `/intern/ambassador/upi` | `/api/v1/intern/ambassador/upi` | `intern_ambassador_upi()` | [ambassador.py:126](file:///apps\portal\routes\ambassador.py#L126) |
| `POST` | `/intern/ambassador/withdraw` | `/api/v1/intern/ambassador/withdraw` | `intern_ambassador_withdraw()` | [ambassador.py:164](file:///apps\portal\routes\ambassador.py#L164) |
| `GET` | `/intern/articles` | `/api/v1/intern/articles` | `intern_articles_list()` | [app.py:8537](file:///apps\portal\app.py#L8537) |
| `POST` | `/intern/articles/save` | `/api/v1/intern/articles/save` | `intern_articles_save()` | [app.py:8547](file:///apps\portal\app.py#L8547) |
| `GET` | `/intern/attendance` | `/api/v1/intern/attendance` | `intern_attendance()` | [app.py:14760](file:///apps\portal\app.py#L14760) |
| `GET` | `/intern/certificates` | `/api/v1/intern/certificates` | `intern_certificates_json()` | [app.py:8664](file:///apps\portal\app.py#L8664) |
| `GET` | `/intern/certificates` | `/api/v1/intern/certificates` | `intern_certificates_json()` | [intern.py:16](file:///apps\portal\routes\intern.py#L16) |
| `GET` | `/intern/cohorts` | `/api/v1/intern/cohorts` | `intern_cohorts()` | [app.py:10225](file:///apps\portal\app.py#L10225) |
| `GET` | `/intern/coins` | `/api/v1/intern/coins` | `intern_coins_json()` | [app.py:8639](file:///apps\portal\app.py#L8639) |
| `GET` | `/intern/cv-meta` | `/api/v1/intern/cv-meta` | `intern_cv_meta()` | [app.py:12473](file:///apps\portal\app.py#L12473) |
| `GET` | `/intern/ecosystem-spotlights` | `/api/v1/intern/ecosystem-spotlights` | `intern_ecosystem_spotlights()` | [app.py:8582](file:///apps\portal\app.py#L8582) |
| `POST` | `/intern/follow/<int:company_id>` | `/api/v1/intern/follow/<int:company_id>` | `intern_follow_company()` | [app.py:10322](file:///apps\portal\app.py#L10322) |
| `POST` | `/intern/interview/profile-urls` | `/api/v1/intern/interview/profile-urls` | `interview_profile_urls()` | [app.py:13047](file:///apps\portal\app.py#L13047) |
| `POST` | `/intern/interview/start` | `/api/v1/intern/interview/start` | `interview_start()` | [app.py:13074](file:///apps\portal\app.py#L13074) |
| `GET` | `/intern/interview/status` | `/api/v1/intern/interview/status` | `interview_status()` | [app.py:12963](file:///apps\portal\app.py#L12963) |
| `POST` | `/intern/interview/submit` | `/api/v1/intern/interview/submit` | `interview_submit()` | [app.py:13198](file:///apps\portal\app.py#L13198) |
| `GET` | `/intern/latest-posts` | `/api/v1/intern/latest-posts` | `intern_latest_posts()` | [app.py:12560](file:///apps\portal\app.py#L12560) |
| `GET` | `/intern/leaderboard` | `/api/v1/intern/leaderboard` | `intern_leaderboard_proxy()` | [app.py:8605](file:///apps\portal\app.py#L8605) |
| `GET` | `/intern/learning-progress` | `/api/v1/intern/learning-progress` | `intern_tutor_progress()` | [app.py:14816](file:///apps\portal\app.py#L14816) |
| `GET` | `/intern/me` | `/api/v1/intern/me` | `intern_me()` | [app.py:12600](file:///apps\portal\app.py#L12600) |
| `GET` | `/intern/messages` | `/api/v1/intern/messages` | `intern_messages_json()` | [app.py:12184](file:///apps\portal\app.py#L12184) |
| `GET` | `/intern/messages/<int:conv_id>` | `/api/v1/intern/messages/<int:conv_id>` | `intern_messages_thread_json()` | [app.py:12204](file:///apps\portal\app.py#L12204) |
| `GET` | `/intern/my-applications` | `/api/v1/intern/my-applications` | `intern_my_applications()` | [app.py:13574](file:///apps\portal\app.py#L13574) |
| `GET` | `/intern/my-applications` | `/api/v1/intern/my-applications` | `intern_my_applications()` | [applications.py:20](file:///apps\portal\routes\applications.py#L20) |
| `GET` | `/intern/notifications` | `/api/v1/intern/notifications` | `intern_notifications()` | [app.py:12227](file:///apps\portal\app.py#L12227) |
| `POST` | `/intern/notifications/<int:notif_id>/read` | `/api/v1/intern/notifications/<int:notif_id>/read` | `intern_notification_read()` | [app.py:12240](file:///apps\portal\app.py#L12240) |
| `POST` | `/intern/notifications/read-all` | `/api/v1/intern/notifications/read-all` | `intern_notifications_read_all()` | [app.py:12252](file:///apps\portal\app.py#L12252) |
| `POST` | `/intern/save-wizard-step` | `/api/v1/intern/save-wizard-step` | `intern_save_wizard_step()` | [app.py:14032](file:///apps\portal\app.py#L14032) |
| `POST` | `/intern/track-spotlight-click` | `/api/v1/intern/track-spotlight-click` | `intern_track_spotlight_click()` | [app.py:8591](file:///apps\portal\app.py#L8591) |
| `GET` | `/intern/tutor-progress` | `/api/v1/intern/tutor-progress` | `intern_tutor_progress()` | [app.py:14815](file:///apps\portal\app.py#L14815) |
| `POST` | `/intern/unfollow/<int:company_id>` | `/api/v1/intern/unfollow/<int:company_id>` | `intern_unfollow_company()` | [app.py:10338](file:///apps\portal\app.py#L10338) |
| `POST` | `/intern/update-profile` | `/api/v1/intern/update-profile` | `intern_update_profile()` | [app.py:13442](file:///apps\portal\app.py#L13442) |
| `GET` | `/intern/wizard-status` | `/api/v1/intern/wizard-status` | `intern_wizard_status()` | [app.py:13831](file:///apps\portal\app.py#L13831) |
| `GET` | `/internship` | `/api/v1/internship` | `_legacy_internship_root()` | [app.py:17861](file:///apps\portal\app.py#L17861) |
| `GET` | `/internship/` | `/api/v1/internship/` | `_legacy_internship_root()` | [app.py:17862](file:///apps\portal\app.py#L17862) |
| `GET` | `/internship/<path:rest>` | `/api/v1/internship/<path:rest>` | `_legacy_internship_redirect()` | [app.py:17868](file:///apps\portal\app.py#L17868) |
| `GET` | `/internship/lead/<int:job_id>` | `/api/v1/internship/lead/<int:job_id>` | `scraped_internship_detail()` | [app.py:18286](file:///apps\portal\app.py#L18286) |
| `GET` | `/internship/lead/<int:job_id>/<slug>` | `/api/v1/internship/lead/<int:job_id>/<slug>` | `scraped_internship_detail()` | [app.py:18287](file:///apps\portal\app.py#L18287) |
| `GET` | `/internships` | `/api/v1/internships` | `internships_listing()` | [app.py:11228](file:///apps\portal\app.py#L11228) |
| `GET` | `/internships/<domain_slug>/<city_slug>` | `/api/v1/internships/<domain_slug>/<city_slug>` | `internships_by_domain_and_city()` | [app.py:11310](file:///apps\portal\app.py#L11310) |
| `GET` | `/internships/<int:post_id>` | `/api/v1/internships/<int:post_id>` | `post_detail_no_slug()` | [app.py:11487](file:///apps\portal\app.py#L11487) |
| `GET` | `/internships/<page_slug>` | `/api/v1/internships/<page_slug>` | `seo_internship_landing()` | [enrollment.py:79](file:///apps\portal\routes\enrollment.py#L79) |
| `GET` | `/internships/<slug>` | `/api/v1/internships/<slug>` | `internships_by_city()` | [app.py:11280](file:///apps\portal\app.py#L11280) |
| `GET` | `/internships/<slug>-<int:post_id>` | `/api/v1/internships/<slug>-<int:post_id>` | `internship_detail()` | [app.py:11481](file:///apps\portal\app.py#L11481) |
| `GET` | `/internships/refresh-feed` | `/api/v1/internships/refresh-feed` | `internships_refresh_feed()` | [app.py:11233](file:///apps\portal\app.py#L11233) |
| `GET` | `/profile` | `/api/v1/profile` | `profile_page()` | [app.py:4875](file:///apps\portal\app.py#L4875) |

## Internship Tasks (3 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/tasks` | `/api/v1/tasks` | `tasks_list()` | [app.py:7540](file:///apps\portal\app.py#L7540) |
| `GET` | `/tasks/<int:task_id>` | `/api/v1/tasks/<int:task_id>` | `task_detail()` | [app.py:7593](file:///apps\portal\app.py#L7593) |
| `POST` | `/tasks/<int:task_id>/submit` | `/api/v1/tasks/<int:task_id>/submit` | `task_submit()` | [app.py:7634](file:///apps\portal\app.py#L7634) |

## Jobs & Sourcing Marketplace (10 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `POST` | `/api/lead/<int:job_id>/click` | `/api/v1/api/lead/<int:job_id>/click` | `scraped_lead_click_track()` | [app.py:18673](file:///apps\portal\app.py#L18673) |
| `POST` | `/api/lead/<int:job_id>/comment` | `/api/v1/api/lead/<int:job_id>/comment` | `scraped_lead_comment_add()` | [app.py:18575](file:///apps\portal\app.py#L18575) |
| `GET` | `/jobs` | `/api/v1/jobs` | `jobs_listing()` | [app.py:11223](file:///apps\portal\app.py#L11223) |
| `GET` | `/jobs/<domain_slug>/<city_slug>` | `/api/v1/jobs/<domain_slug>/<city_slug>` | `jobs_by_domain_and_city()` | [app.py:11299](file:///apps\portal\app.py#L11299) |
| `GET` | `/jobs/<int:post_id>` | `/api/v1/jobs/<int:post_id>` | `post_detail_no_slug()` | [app.py:11486](file:///apps\portal\app.py#L11486) |
| `GET` | `/jobs/<slug>` | `/api/v1/jobs/<slug>` | `jobs_by_city()` | [app.py:11267](file:///apps\portal\app.py#L11267) |
| `GET` | `/jobs/<slug>-<int:post_id>` | `/api/v1/jobs/<slug>-<int:post_id>` | `job_detail()` | [app.py:11476](file:///apps\portal\app.py#L11476) |
| `POST` | `/posts/<int:post_id>/apply` | `/api/v1/posts/<int:post_id>/apply` | `post_apply()` | [app.py:11598](file:///apps\portal\app.py#L11598) |
| `POST` | `/posts/<int:post_id>/comment` | `/api/v1/posts/<int:post_id>/comment` | `post_comment_add()` | [app.py:11691](file:///apps\portal\app.py#L11691) |
| `GET` | `/posts/<int:post_id>/comments` | `/api/v1/posts/<int:post_id>/comments` | `post_comments()` | [app.py:11676](file:///apps\portal\app.py#L11676) |

## Mentor Network (9 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/mentor` | `/api/v1/mentor` | `mentor_page()` | [app.py:4898](file:///apps\portal\app.py#L4898) |
| `GET` | `/mentor/applications` | `/api/v1/mentor/applications` | `mentor_applications()` | [app.py:15162](file:///apps\portal\app.py#L15162) |
| `GET` | `/mentor/earnings` | `/api/v1/mentor/earnings` | `mentor_earnings()` | [app.py:7995](file:///apps\portal\app.py#L7995) |
| `GET` | `/mentor/interview/<path:email>` | `/api/v1/mentor/interview/<path:email>` | `mentor_interview_view()` | [app.py:13365](file:///apps\portal\app.py#L13365) |
| `GET` | `/mentor/me` | `/api/v1/mentor/me` | `mentor_me()` | [app.py:15143](file:///apps\portal\app.py#L15143) |
| `POST` | `/mentor/update-status` | `/api/v1/mentor/update-status` | `mentor_update_status()` | [app.py:15189](file:///apps\portal\app.py#L15189) |
| `GET` | `/mentors/slots` | `/api/v1/mentors/slots` | `intern_mentor_slots()` | [app.py:7922](file:///apps\portal\app.py#L7922) |
| `POST` | `/mentors/slots/<int:slot_id>/book` | `/api/v1/mentors/slots/<int:slot_id>/book` | `intern_book_slot()` | [app.py:7954](file:///apps\portal\app.py#L7954) |
| `POST` | `/mentors/slots/<int:slot_id>/book` | `/api/v1/mentors/slots/<int:slot_id>/book` | `intern_book_slot()` | [mentor.py:18](file:///apps\portal\routes\mentor.py#L18) |

## Payments & Financial Operations (10 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/api/payment/config` | `/api/v1/api/payment/config` | `api_payment_config()` | [app.py:14343](file:///apps\portal\app.py#L14343) |
| `POST` | `/api/payment/razorpay/create-order` | `/api/v1/api/payment/razorpay/create-order` | `api_razorpay_create_order()` | [app.py:14349](file:///apps\portal\app.py#L14349) |
| `POST` | `/api/payment/razorpay/create-order` | `/api/v1/api/payment/razorpay/create-order` | `api_razorpay_create_order()` | [payment.py:36](file:///apps\portal\routes\payment.py#L36) |
| `POST` | `/api/payment/razorpay/verify-payment` | `/api/v1/api/payment/razorpay/verify-payment` | `api_razorpay_verify_payment()` | [app.py:14416](file:///apps\portal\app.py#L14416) |
| `POST` | `/api/payment/razorpay/verify-payment` | `/api/v1/api/payment/razorpay/verify-payment` | `api_razorpay_verify_payment()` | [payment.py:77](file:///apps\portal\routes\payment.py#L77) |
| `POST` | `/api/payment/razorpay/webhook` | `/api/v1/api/payment/razorpay/webhook` | `api_razorpay_webhook()` | [app.py:14582](file:///apps\portal\app.py#L14582) |
| `GET` | `/api/payment/status` | `/api/v1/api/payment/status` | `api_payment_status()` | [payment.py:26](file:///apps\portal\routes\payment.py#L26) |
| `POST` | `/enrollment/paid-1999` | `/api/v1/enrollment/paid-1999` | `enrollment_paid_1999()` | [app.py:8062](file:///apps\portal\app.py#L8062) |
| `POST` | `/paid/enroll` | `/api/v1/paid/enroll` | `paid_enroll()` | [app.py:14253](file:///apps\portal\app.py#L14253) |
| `POST` | `/post-hire/deposit` | `/api/v1/post-hire/deposit` | `post_hire_deposit()` | [app.py:13626](file:///apps\portal\app.py#L13626) |

## Public Website & General (34 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/` | `/api/v1/` | `index()` | [app.py:4608](file:///apps\portal\app.py#L4608) |
| `GET` | `/accelerate` | `/api/v1/accelerate` | `accelerate_checkout()` | [enrollment.py:71](file:///apps\portal\routes\enrollment.py#L71) |
| `GET` | `/account/coins` | `/api/v1/account/coins` | `account_coins_ledger()` | [app.py:7784](file:///apps\portal\app.py#L7784) |
| `GET`, `POST` | `/account/gemini-key` | `/api/v1/account/gemini-key` | `account_gemini_key()` | [app.py:6575](file:///apps\portal\app.py#L6575) |
| `GET` | `/api/admin/sourcing-stats` | `/api/v1/api/admin/sourcing-stats` | `api_admin_sourcing_stats()` | [app.py:18173](file:///apps\portal\app.py#L18173) |
| `GET` | `/api/auth/status` | `/api/v1/api/auth/status` | `api_auth_status()` | [auth.py:28](file:///apps\portal\routes\auth.py#L28) |
| `POST` | `/api/masterclass/register` | `/api/v1/api/masterclass/register` | `masterclass_register_api()` | [masterclass.py:137](file:///apps\portal\routes\masterclass.py#L137) |
| `GET` | `/api/public/blog-posts` | `/api/v1/api/public/blog-posts` | `public_blog_posts()` | [app.py:6009](file:///apps\portal\app.py#L6009) |
| `GET` | `/api/public/blog-posts/<slug>` | `/api/v1/api/public/blog-posts/<slug>` | `public_blog_post_detail()` | [app.py:6055](file:///apps\portal\app.py#L6055) |
| `GET` | `/api/public/courses` | `/api/v1/api/public/courses` | `api_public_courses()` | [app.py:10442](file:///apps\portal\app.py#L10442) |
| `GET` | `/api/stats/openings` | `/api/v1/api/stats/openings` | `api_stats_openings()` | [app.py:10542](file:///apps\portal\app.py#L10542) |
| `GET` | `/articles/<int:article_id>` | `/api/v1/articles/<int:article_id>` | `article_redirect_to_main_blog()` | [app.py:5986](file:///apps\portal\app.py#L5986) |
| `GET` | `/articles/<slug>-<int:article_id>` | `/api/v1/articles/<slug>-<int:article_id>` | `article_redirect_to_main_blog()` | [app.py:5987](file:///apps\portal\app.py#L5987) |
| `POST` | `/check-email` | `/api/v1/check-email` | `check_email()` | [app.py:17504](file:///apps\portal\app.py#L17504) |
| `POST` | `/cohort/<int:cohort_id>/enroll` | `/api/v1/cohort/<int:cohort_id>/enroll` | `cohort_enroll()` | [enrollment.py:19](file:///apps\portal\routes\enrollment.py#L19) |
| `GET` | `/e/o.gif` | `/api/v1/e/o.gif` | `email_open_pixel()` | [app.py:4813](file:///apps\portal\app.py#L4813) |
| `GET` | `/first-run` | `/api/v1/first-run` | `first_run()` | [app.py:9427](file:///apps\portal\app.py#L9427) |
| `POST` | `/generate-tutor-token` | `/api/v1/generate-tutor-token` | `generate_tutor_token()` | [app.py:5043](file:///apps\portal\app.py#L5043) |
| `GET` | `/interview` | `/api/v1/interview` | `interview_page()` | [app.py:4885](file:///apps\portal\app.py#L4885) |
| `GET` | `/jd/<domain>` | `/api/v1/jd/<domain>` | `get_jd()` | [app.py:8788](file:///apps\portal\app.py#L8788) |
| `GET` | `/launchpad` | `/api/v1/launchpad` | `launchpad_checkout()` | [enrollment.py:63](file:///apps\portal\routes\enrollment.py#L63) |
| `GET`, `POST` | `/logout` | `/api/v1/logout` | `logout()` | [app.py:12539](file:///apps\portal\app.py#L12539) |
| `GET`, `POST` | `/logout` | `/api/v1/logout` | `logout()` | [auth.py:117](file:///apps\portal\routes\auth.py#L117) |
| `GET` | `/masterclass/data-analyst` | `/api/v1/masterclass/data-analyst` | `masterclass_landing()` | [masterclass.py:78](file:///apps\portal\routes\masterclass.py#L78) |
| `GET` | `/portal` | `/api/v1/portal` | `portal_page()` | [app.py:4844](file:///apps\portal\app.py#L4844) |
| `GET` | `/post-hire/launch-tasks` | `/api/v1/post-hire/launch-tasks` | `post_hire_launch_tasks()` | [app.py:8249](file:///apps\portal\app.py#L8249) |
| `GET` | `/privacy` | `/api/v1/privacy` | `privacy_page()` | [app.py:4771](file:///apps\portal\app.py#L4771) |
| `GET` | `/program` | `/api/v1/program` | `program_page()` | [app.py:4622](file:///apps\portal\app.py#L4622) |
| `GET` | `/r/click` | `/api/v1/r/click` | `referral_click()` | [ambassador.py:28](file:///apps\portal\routes\ambassador.py#L28) |
| `GET` | `/terms` | `/api/v1/terms` | `terms_page()` | [app.py:4765](file:///apps\portal\app.py#L4765) |
| `POST` | `/track-visit` | `/api/v1/track-visit` | `track_visit()` | [app.py:15044](file:///apps\portal\app.py#L15044) |
| `GET` | `/unsubscribe` | `/api/v1/unsubscribe` | `unsubscribe()` | [app.py:4777](file:///apps\portal\app.py#L4777) |
| `GET` | `/upcoming-mondays` | `/api/v1/upcoming-mondays` | `upcoming_mondays()` | [app.py:8800](file:///apps\portal\app.py#L8800) |
| `GET` | `/uploads/<path:filename>` | `/api/v1/uploads/<path:filename>` | `serve_uploaded_file()` | [app.py:17420](file:///apps\portal\app.py#L17420) |

## Scheduled Tasks & Cron (5 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `POST` | `/cron/clean-tokens` | `/api/v1/cron/clean-tokens` | `cron_clean_tokens()` | [app.py:17790](file:///apps\portal\app.py#L17790) |
| `POST`, `GET` | `/cron/cohort-reminders` | `/api/v1/cron/cohort-reminders` | `cron_cohort_reminders()` | [app.py:10291](file:///apps\portal\app.py#L10291) |
| `POST` | `/cron/enrollment-reminders` | `/api/v1/cron/enrollment-reminders` | `cron_enrollment_reminders()` | [app.py:17752](file:///apps\portal\app.py#L17752) |
| `POST` | `/cron/expire-posts` | `/api/v1/cron/expire-posts` | `cron_expire_posts()` | [app.py:10448](file:///apps\portal\app.py#L10448) |
| `POST`, `GET` | `/cron/process-outbox` | `/api/v1/cron/process-outbox` | `cron_process_outbox()` | [app.py:17806](file:///apps\portal\app.py#L17806) |

## Staff Operations (10 endpoints)

| HTTP Method | Source Flask Route | Target FastAPI Endpoint | Flask Handler | Source Line |
|---|---|---|---|---|
| `GET` | `/staff/courses` | `/api/v1/staff/courses` | `staff_courses_redirect()` | [app.py:6764](file:///apps\portal\app.py#L6764) |
| `GET` | `/staff/dashboard` | `/api/v1/staff/dashboard` | `staff_dashboard()` | [app.py:6716](file:///apps\portal\app.py#L6716) |
| `GET` | `/staff/logout` | `/api/v1/staff/logout` | `staff_logout()` | [app.py:6708](file:///apps\portal\app.py#L6708) |
| `GET`, `POST` | `/staff/mentor-slots` | `/api/v1/staff/mentor-slots` | `staff_mentor_slots()` | [app.py:7835](file:///apps\portal\app.py#L7835) |
| `GET` | `/staff/payments` | `/api/v1/staff/payments` | `staff_payments_redirect()` | [app.py:6771](file:///apps\portal\app.py#L6771) |
| `GET` | `/staff/projects` | `/api/v1/staff/projects` | `staff_project_queue()` | [app.py:6888](file:///apps\portal\app.py#L6888) |
| `POST` | `/staff/projects/<int:submission_id>/decision` | `/api/v1/staff/projects/<int:submission_id>/decision` | `staff_project_decision()` | [app.py:6914](file:///apps\portal\app.py#L6914) |
| `GET` | `/staff/tasks` | `/api/v1/staff/tasks` | `staff_task_queue()` | [app.py:7391](file:///apps\portal\app.py#L7391) |
| `POST` | `/staff/tasks/<int:submission_id>/decision` | `/api/v1/staff/tasks/<int:submission_id>/decision` | `staff_task_decision()` | [app.py:7469](file:///apps\portal\app.py#L7469) |
| `POST` | `/staff/tasks/create` | `/api/v1/staff/tasks/create` | `staff_create_task()` | [app.py:7418](file:///apps\portal\app.py#L7418) |
