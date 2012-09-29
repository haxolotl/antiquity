
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
       
class PJDay:

        
	def __init__(self,day_number):
		self.number = int(math.floor(day_number))
# 		for now we'll just use integers. fractional days can come later.

	@property
	def date(self):
		j = self.number + 32045
		g = j/146097
		dg = j % 146097
		c = (dg/36524 + 1 ) * 3/4 
		dc = dg - c * 36524
		b = dc/1461
		db = dc % 1461
		a = (db/365 + 1 ) * 3/4
		da = db - a * 365
		y = g * 400 + c * 100 + b * 4 + a 
		m = (da * 5 +308)/153 - 2 
		d = da - (m + 4) * 153/5 + 122
		Y = y - 4800 + (m + 2)/12
		M = (m + 2) % 12 + 1 
		D = d + 1
		return (Y, M, D)
	
	@property
	def year(self):
		return self.date[0]

	@property		
	def month(self):
		return self.date[1]
		
	@property
	def day(self):
		return self.date[2]