
import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

for t in ['security_deposits', 'payments', 'course_payments', 'intern_certificates', 'intern_offer_letters']:
    c.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t}';")
    cols = [r[0] for r in c.fetchall()]
    print(f"{t}: {cols}")

conn.close()
