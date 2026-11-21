import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app
from extensions import db
from models import InternOfferLetter, User, CautionDepositEnrollment

with app.app_context():
    u = User.query.filter_by(email='stage3_selected@dbert.test').first()
    if u:
        o = InternOfferLetter.query.filter_by(user_id=u.id).first()
        print('User found:', u.id, u.email, u.full_name)
        if o:
            print('Offer:', o.id, o.offer_letter_id, 'sig:', repr(o.signature_name), 'acc_at:', repr(o.accepted_at), 'status:', o.caution_deposit_status)
        else:
            print('No offer for user')
        c = CautionDepositEnrollment.query.filter_by(user_id=u.id).first()
        if c:
            print('Caution deposit enrollment:', c.id, c.utr, c.payment_status)
        else:
            print('No caution deposit enrollment')
    else:
        print('User stage3_selected@dbert.test not found')
