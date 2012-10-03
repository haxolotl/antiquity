import unittest
from antiquity import *

class TestDate(unittest.TestCase):
    # test data from http://www.fourmilab.ch/documents/calendar/

    def setUp(self):
        self.real_dates = {
            'great_fire_of_london': {
                'gregorian_date': (1666,9,12), # Paris
                'julian_date': (1666,9,2), # London
                'julian_day': 2329808.5,
                'mod_julian_day': -70192,
            },
            'october_revolution': {
                'gregorian_date': (1917,11,7), # the West (actually November)
                'julian_date': (1917,10,25), # Petrograd
                'julian_day': 2421539.5,
                'mod_julian_day': 21539,
            },
            'invasion_day': {
                'gregorian_date': (1788,1,26), # Sydney
                'julian_date': (1788,1,15), # Bulgaria and Russia
                'julian_day': 2374138.5,
                'mod_julian_day': -25862,
            },
            'nick_drake': {
                'gregorian_date': (1974,11,25), 
                'julian_date': (1974,11,12), # Berbers and Mt Athos only
                'julian_day': 2442376.5,
                'mod_julian_day': 42376,
            }
        }
        self.fire = PGDate(*self.real_dates['great_fire_of_london']['gregorian_date'])
        self.october = PGDate(*self.real_dates['october_revolution']['gregorian_date'])
        self.invasion = PGDate(*self.real_dates['invasion_day']['gregorian_date'])
        self.drake = PGDate(*self.real_dates['nick_drake']['gregorian_date'])
        self.impossible_dates = (
            (0,1,24),
            (2012,0,15),
            (2012,13,8),
#             (2012,9,0), # haven't figured out how to validate days yet
#             (2012,9,31),
#             (2011,2,29),
        )
        
#         self.gregorian_date_tuples = {
#             'great_fire': (1666,9,12), # was (1666,9,2) in London (Julian)
#             'october': (1917,11,7), # was (1917,10,25) in Petrograd (Julian)
#             'invasion': (1788,1,26),
#             'tet': (1968,1,31),
#             'nick_drake': (1974,11,25),
#             'peterloo': (1819,8,16),
#             'leila': (1969,8,29),
#             'venus': (1639,12,4),
#         }
#         self.julian_date_tuples{
#             'joan': (1431,5,30),
#             'great_fire': (1666,9,2),
#             'october': (1917,10,25),
#             'venus': (1639,11,24),
#             'eclipse': (-1998,5,6), 
#         }

    def test_impossible_dates(self):
        # this doesn't indicate which one failed
        for test_date in self.impossible_dates:
            with self.assertRaises(ValueError):
                stupid_date = PGDate(*test_date)
            
    def test_leap_years(self):
        leap_day = PGDate(2012,2,29)
#         bad_day = PGDate(2011,2,29) # this should actually fail
    

    def test_PJDay_to_PGDate(self):
        for value in self.real_dates.values():
            self.assertEqual(PJDay(julian_day=value['julian_day']), PGDate(*value['gregorian_date']))
            
    def test_leapiness(self):
        self.assertEqual(PGDate(1964,1,1).leap_year, True)
        self.assertEqual(PGDate(1963,1,1).leap_year, False)
        self.assertEqual(PGDate(1900,1,1).leap_year, False)
        self.assertEqual(PGDate(2000,1,1).leap_year, True)
        self.assertEqual(PGDate(2011,1,1).year_length, 365)
        self.assertEqual(PGDate(2012,1,1).year_length, 366)

    def test_month_length(self):
        self.assertEqual(PGDate(1964,1,1).month_length, 31)
        self.assertEqual(PGDate(1964,2,1).month_length, 29)
        self.assertEqual(PGDate(1963,2,1).month_length, 28)
        self.assertEqual(PGDate(1964,3,1).month_length, 31)
        self.assertEqual(PGDate(1964,4,1).month_length, 30)
        self.assertEqual(PGDate(1964,5,1).month_length, 31)
        self.assertEqual(PGDate(1964,6,1).month_length, 30)
        self.assertEqual(PGDate(1964,7,1).month_length, 31)
        self.assertEqual(PGDate(1964,8,1).month_length, 31)
        self.assertEqual(PGDate(1964,9,1).month_length, 30)
        self.assertEqual(PGDate(1964,10,1).month_length, 31)
        self.assertEqual(PGDate(1964,11,1).month_length, 30)
        self.assertEqual(PGDate(1964,12,1).month_length, 31)
        
    def test_comparison(self):
        self.assertTrue(self.drake > self.invasion)
        self.assertTrue(self.fire < self.october)
        self.assertTrue(PGDate(-400,3,4) > PGDate(-500,1,1))
        self.assertTrue(FuzzyPGDate(1930) > FuzzyPGDate(1820))
        sorted_dates = sorted([self.drake, self.invasion, self.fire, self.october])
        self.assertEquals(sorted_dates[0], self.fire)
        self.assertEquals(sorted_dates[3], self.drake)
            
#     def test_centuries(self):
#         self.assertEqual(self.last_day_of_20thC.century, 20)
#         self.assertEqual(self.first_day_of_21stC.century, 21)
#         self.assertEqual(self.last_day_of_1stC_BC.century, -1)
#         self.assertEqual(self.first_day_of_1stC_BC.century, -1)


if __name__ == '__main__':
    unittest.main()