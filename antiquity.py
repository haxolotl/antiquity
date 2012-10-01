
import math
from datetime import date, timedelta
from exceptions import ValueError
       
class PJDay(object):
        
    def __init__(self, day_number):
        self.number = int(math.floor(day_number))
#       for now we'll just use integers. fractional days can come later.

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
        
    def __repr__(self):
        return "antiquity.PJDay(%d)" % self.number
        
    def __str__(self):
        return "Julian Day: %d" % self.number
        
    def __cmp__(self, other):
        return self.number - other.number
        
    def __sub__(self, other):
        return timedelta(days=self.number - other.number)
        
    def __add__(self, other):
        if not isinstance(other, timedelta):
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (self.__class__, other.__class__))
        return self.__class__(self.number + other.days)
        
class PGDate(PJDay):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super(PGDate, self).__init__(int(args[0]))
        elif len(args) == 3:
            year = int(args[0])
            if year < 0:
                year = year + 1
            elif year == 0:
                raise ValueError("There is no year zero - http://lmgtfy.com/?q=year+0")
            month = int(args[1])
            if month > 12 or month < 1:
                raise ValueError("Month must not be less than 1 or greater than 12")
            day = int(args[2]) # TO DO - validate input
            a = (14-month)/12
            y = year + 4800 - a
            m = month + 12*a - 3
            super(PGDate, self).__init__(day+(153*m+2)/5+365*y+y/4-y/100+y/400-32046)
        else:
            raise TypeError("__init__() takes either 1 or 3 arguments")

    def __repr__(self):
        return "antiquity.PGDate(%d, %d, %d)" % (self.year, self.month, self.day)
    
    def __str__(self):
        if self.year < 0:
            return "Proleptic Gregorian Date: %dBCE-%d-%d" % (abs(self.year), self.month, self.day)
        else:
            return "Proleptic Gregorian Date: %d-%d-%d" % (self.year, self.month, self.day)

class FuzzyPJDay(PJDay):
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.fuzziness = args[1]
            super(FuzzyPJDay, self).__init__(int(args[0]))
        else:
            raise TypeError("__init__() takes 2 arguments")

    def __repr__(self):
        return "antiquity.FuzzyPJDay(%d, %r)" % (self.number, self.fuzziness)
    
    def __str__(self):
        return "Julian Day: %d +/- %d days" % (self.number, self.fuzziness.days)
        
class FuzzyPGDate(PGDate):
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.fuzziness = args[1]
            super(FuzzyPGDate, self).__init__(int(args[0]))
        elif len(args) == 4:
            self.fuzziness = args[3]
            year = int(args[0])
            if year < 0:
                year = year + 1
            elif year == 0:
                raise ValueError("There is no year zero - http://lmgtfy.com/?q=year+0")
            month = int(args[1])
            if month > 12 or month < 1:
                raise ValueError("Month must not be less than 1 or greater than 12")
            day = int(args[2]) # TO DO - validate input
            a = (14-month)/12
            y = year + 4800 - a
            m = month + 12*a - 3
            super(FuzzyPGDate, self).__init__(day+(153*m+2)/5+365*y+y/4-y/100+y/400-32046)
        else:
            raise TypeError("__init__() takes either 2 or 4 arguments")

    def __repr__(self):
        return "antiquity.FuzzyPGDate(%d, %d, %d, %r)" % (self.year, self.month, self.day, self.fuzziness)
    
    def __str__(self):
        if self.year < 0:
            return "Proleptic Gregorian Date: %dBCE-%d-%d +/- %d days" % (abs(self.year), self.month, self.day, self.fuzziness.days)
        else:
            return "Proleptic Gregorian Date: %d-%d-%d +/- %d days" % (self.year, self.month, self.day, self.fuzziness.days)
        
