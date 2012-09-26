
import math
from datetime import date
from exceptions import ValueError


class HistoricalDate:

    def __init__(self, year, month, day):
        """
        see http://www.hermetic.ch/cal_stud/jdn.htm#comp
        http://www.merlyn.demon.co.uk/daycount.htm#GDDC
        http://www.tondering.dk/claus/cal/julperiod.php#formula
        http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?bibcode=1983IAPPP..13...16F&db_key=AST&page_ind=0&data_type=GIF&type=SCREEN_VIEW&classic=YES
        """
        self.year = int(year)
        # _year is for internal calculations only, not for humans
        # 1BC = 0, 2BC = -1 etc.
        if int(year) > 0:
            self._year = int(year)
        elif int(year) < 0:
            self._year = int(year) + 1
        else:
            raise ValueError("http://lmgtfy.com/?q=year+0")
        self.month = int(month)
        self.day = int(day)
        self.julian_day = self._julian_day()    
        self.century = self._century()

    def _century(self):
        if self._year > 0:
            return (self._year-1)/100+1
        else:
            return (self._year-1)/100 # integer division of negative number is weird!
        
    def _julian_day(self):
        a = (14-self.month)/12
        y = self._year + 4800 - a
        m = self.month + 12*a - 3
        return self.day+(153*m+2)/5+365*y+y/4-y/100+y/400-32045
        
