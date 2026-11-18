import re

def clean_phone_number(raw_phone) -> str:
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", str(raw_phone))
    if digits.startswith("91") and len(digits) == 12:
        return digits
    if len(digits) == 10:
        return f"91{digits}"
    return ""

def format_revenue_whatsapp_message(cand: dict) -> str:
    name = (cand.get("name") or "Candidate").strip()
    amount = cand.get("amount", 499)
    domain = cand.get("domain") or "Applied AI Engineering"
    email = cand.get("email", "").strip()

    if amount == 499:
        # Caution deposit message
        return (
            f"🎓 *DBERT Incubation Admission & Caution Deposit Notice*\n"
            f"\n"
            f"Dear {name},\n"
            f"\n"
            f"Congratulations on your selection for the *{domain}* Incubation track!\n"
            f"\n"
            f"🔗 *1-Tap Fast-Pay & LMS Access (Line 8):*\n"
            f"👉 https://lms.dbert.in/portal\n"
            f"\n"
            f"📋 *Admissions Helpdesk WhatsApp (Line 11):*\n"
            f"👉 https://wa.me/918192911360\n"
            f"\n"
            f"📧 *Email Dispatch Notice:*\n"
            f"Official seat confirmation email dispatched from abhinav.sharma@dbert.in to {email}.\n"
            f"\n"
            f"📌 *Financial Ledger Breakdown:*\n"
            f"• *Candidate:* {name}\n"
            f"• *Track:* {domain}\n"
            f"• *Caution Deposit:* ₹499 (100% Credited / Refundable)\n"
            f"• *Batch Kickoff:* Monday, 6:00 PM IST\n"
            f"• *Cutoff:* Today, 6:00 PM IST\n"
            f"\n"
            f"🚀 *What ₹499 Unlocks:*\n"
            f"1️⃣ Immediate access to LMS interactive coding lab & AI mentor.\n"
            f"2️⃣ 100% credited against your fee or refundable upon sprint milestones.\n"
            f"3️⃣ Unlocks eligibility for the *₹5,000 fellowship stipend*.\n"
            f"4️⃣ Official Letter of Selection on sovereign domain dbert.in.\n"
            f"\n"
            f"📲 *Next Steps:* Login at https://lms.dbert.in/portal and complete ₹499 via Google Pay, PhonePe, or Paytm.\n"
            f"\n"
            f"Queries? Reply directly to this WhatsApp message."
        )
    else:
        # ₹299 Credential Verification message
        return (
            f"🎓 *DBERT Fellowship Advancement & Stipend Release Notice*\n"
            f"\n"
            f"Dear {name},\n"
            f"\n"
            f"Your technical progress in the *{domain}* Fellowship is outstanding!\n"
            f"\n"
            f"🔗 *Unlock Gate 3 Verification (Line 8):*\n"
            f"👉 https://dbert.in/enroll/1999\n"
            f"\n"
            f"📋 *Google Form Verification (Line 11):*\n"
            f"👉 https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform\n"
            f"\n"
            f"📧 *Official Email Notice:*\n"
            f"Milestone audit dispatched from abhinav.sharma@dbert.in to {email}.\n"
            f"\n"
            f"📌 *4-Gate Stipend Progression Status:*\n"
            f"• *Gate 1 (LinkedIn):* ✓ Connected / Active\n"
            f"• *Gate 2 (Case Study):* Ready for Review\n"
            f"• *Gate 3 (₹299 Verification):* ⏳ PENDING UNLOCK\n"
            f"• *Gate 4 (GitHub Repo):* ✓ Connected / Active\n"
            f"\n"
            f"💰 *Why Complete Gate 3 (₹299) Today:*\n"
            f"1️⃣ Releases your *₹5,000 cash stipend* directly to your LMS UPI wallet.\n"
            f"2️⃣ Official 3-Document Executive Packet: Certificate, Evaluation Rubric (Score/100), and signed Director LOR.\n"
            f"3️⃣ Permanent listing on Pre-Vetted Engineers Directory (dbert.in/verify/directory).\n"
            f"\n"
            f"📲 *Next Steps:* Visit https://dbert.in/enroll/1999 to complete ₹299 verification.\n"
            f"\n"
            f"Questions? Reply directly or WhatsApp Mentorship Desk at +91 89580 06294."
        )

if __name__ == "__main__":
    sample_499 = {"name": "Aayush Aryan", "amount": 499, "domain": "Data Analytics", "email": "aayush@gmail.com"}
    sample_299 = {"name": "Priyanshu Kalondia", "amount": 299, "domain": "AI Engineering", "email": "priyanshu@gmail.com"}

    print("--- SAMPLE ₹499 WHATSAPP ---")
    msg499 = format_revenue_whatsapp_message(sample_499)
    print(msg499)
    lines499 = msg499.split("\n")
    print("Line 8:", lines499[7] if len(lines499) > 7 else "N/A")
    print("Line 11:", lines499[10] if len(lines499) > 10 else "N/A")

    print("\n--- SAMPLE ₹299 WHATSAPP ---")
    msg299 = format_revenue_whatsapp_message(sample_299)
    print(msg299)
    lines299 = msg299.split("\n")
    print("Line 8:", lines299[7] if len(lines299) > 7 else "N/A")
    print("Line 11:", lines299[10] if len(lines299) > 10 else "N/A")
