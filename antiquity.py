
import math
from datetime import date
from exceptions import ValueError
       
class PJDay:

        
	def __init__(self, day_number):
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
		if Y < 1:
		  Y = Y - 1
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
		
class PGDate(PJDay):
    def __init__(self, year, month, day):
        year = int(year)
        if year < 0:
            year = year + 1
        elif year == 0:
            raise ValueError("http://lmgtfy.com/?q=year+0")
        month = int(month)
        if month > 12 or month < 1:
            raise ValueError("Month must not be less than 1 or greater than 12")
        day = int(day) # TO DO - validate input
        a = (14-month)/12
        y = year + 4800 - a
        m = month + 12*a - 3
        self.number = day+(153*m+2)/5+365*y+y/4-y/100+y/400-32046
    
    