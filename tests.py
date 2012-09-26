import unittest
from antiquity import HistoricalDate

class TestDate(unittest.TestCase):
    # test data from http://www.fourmilab.ch/documents/calendar/

    def setUp(self):
        self.recent_birthday = HistoricalDate(2012,1,24)
        self.ancient_birthday = HistoricalDate(-1000,1,24)
        self.old_birthday = HistoricalDate(1066,1,24)
        self.last_day_of_20thC = HistoricalDate(2000,12,31)
        self.first_day_of_21stC = HistoricalDate(2001,1,1)
        self.last_day_of_1stC_BC = HistoricalDate(-10,12,31)
        self.first_day_of_1stC_BC = HistoricalDate(-10,1,1)
        
    def test_basics(self):
        
        self.assertEqual(self.recent_birthday.julian_day, 2455951.0)
        self.assertEqual(self.old_birthday.julian_day, 2110432.0)
        self.assertEqual(self.ancient_birthday.julian_day, 1356206.0)
                
        # should raise an exception for year zero (which does not exist)
        with self.assertRaises(ValueError):
            stupid_date = HistoricalDate(0,1,24)
            
    def test_centuries(self):
        self.assertEqual(self.last_day_of_20thC.century, 20)
        self.assertEqual(self.first_day_of_21stC.century, 21)
        self.assertEqual(self.last_day_of_1stC_BC.century, -1)
        self.assertEqual(self.first_day_of_1stC_BC.century, -1)


if __name__ == '__main__':
    unittest.main()