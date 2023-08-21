from django.test import TestCase
from .models import Member
import datetime
from datetime import date, timedelta

# Create your tests here.


class PaymentUnitTest(TestCase):
        def setUp(self):
            self.member = Member.objects.create(
                 username="test"
                 )
            self.member.save()
        
        def test_has_paid(self):
            self.assertFalse(
                  self.member.has_paid(),
                  "Initial member should have empty paid_until attr"
            )

        def test_different_date_values(self):
            current_date = date(2020, 2, 4)
            _30days = timedelta(days=30)
            self.member.set_paid_until(current_date + _30days)
            self.assertTrue(
                self.member.has_paid(
                 current_date=current_date
                )  
            )

            self.member.set_paid_until(current_date - _30days)
            self.assertFalse(
                self.member.has_paid(
                 current_date=current_date
                )  
            )

        # def test_different_date_types(self):
        #     current_date = date(2020, 2, 4)
        #     _30days = timedelta(days=30)
            
        #     ts_in_future = datetime.timedelta(current_date + _30days)

        #     self.member.set_paid_until(
        #          int(ts_in_future)
        #     )
        #     self.member.set_paid_until(
        #          '1212344545'
        #     )


            