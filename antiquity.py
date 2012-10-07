
import math
from datetime import date, timedelta
from exceptions import ValueError
from utils import is_leap_year, get_year_length, get_month_length       

class PJDay(object):
    """
    This is the base class from which all our other classes inherit.
    
    It defines a date as a Proleptic Julian Day number, and defines a bunch of methods to convert
    to other date systems.
    
    You probably don't want to use it directly unless you're an astronomer, or for some reason you're 
    starting off with a Julian Day number.
    
    Takes a single arg, which should be an int (or a float or string which can be coerced to one)
    
    eg. PJDay(2456203)
    
    TO DO - accept non-integer values

    """
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('days'):
            self.days = float(kwargs['days'])
        else:
            raise TypeError("__init__() takes a keyword arg called 'days'")
#       for now we'll just use integers. fractional days can come later.

    @property
    def date(self):
        """
        Returns a tuple of 3 ints representing the year, month and day in the Proleptic Gregorian calendar
        
        Years BCE are represented as negative numbers. There is no year zero. Hence 1BCE = -1.
        """
        j = self.days + 32045
        g = j//146097
        dg = j % 146097
        c = (dg//36524 + 1 ) * 3//4 
        dc = dg - c * 36524
        b = dc//1461
        db = dc % 1461
        a = (db//365 + 1 ) * 3//4
        da = db - a * 365
        y = g * 400 + c * 100 + b * 4 + a 
        m = (da * 5 +308)//153 - 2 
        d = da - (m + 4) * 153//5 + 122
        Y = y - 4800 + (m + 2)//12
        M = (m + 2) % 12 + 1 
        D = d + 1
        if Y < 1:
            Y = Y - 1
        return (int(Y), int(M), int(D))
    
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
        return "antiquity.PJDay(%d)" % self.days
        
    def __str__(self):
        return "Julian Day: %d" % self.days
        
    def __cmp__(self, other):
        return self.days - other.days
        
    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(days=self.days - other.days)            
        if isinstance(other, PJDay):
            return timedelta(days=self.days - other.days)
        
    def __add__(self, other):
        if not isinstance(other, timedelta):
            raise TypeError("unsupported operand type(s) for +: '%s' and '%s'" % (self.__class__, other.__class__))
        return self.__class__(days=self.days + other.days)
        
    @property
    def weekday(self):
        return int(math.ceil(self.days)) % 7    
     
    @property
    def isoweekday(self):
        return self.weekday + 1 
    
class PGDate(PJDay):
    """
    Represents a Proleptic Gregorian Date.
        
    Most likely, you will want to pass this 3 args, just like you would with a standard python date object.
    Alternatively, it will accept a kwarg called days. If this is present, it overrides any args.
        
    eg. PGDate(1995,6,17) or PGDate(days=2449885)
    
    """
    def __init__(self, *args, **kwargs):
        if kwargs.has_key('days'):
            super(PGDate, self).__init__(**kwargs)
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
            super(PGDate, self).__init__(days=(day+(153*m+2)/5+365*y+y/4-y/100+y/400-32046)+0.5)
        else:
            raise TypeError("__init__() takes either a kwarg called 'days' or 3 args")

    def __repr__(self):
        return "antiquity.PGDate(%d, %d, %d)" % (self.year, self.month, self.day)
    
    def __str__(self):
        if self.year < 0:
            return "Proleptic Gregorian Date: %dBCE-%d-%d" % (abs(self.year), self.month, self.day)
        else:
            return "Proleptic Gregorian Date: %d-%d-%d" % (self.year, self.month, self.day)

    @property
    def leap_year(self):
        return is_leap_year(self.year)
        
    @property
    def year_length(self):
        return get_year_length(self.year)
        
    @property
    def month_length(self):
        return get_month_length(self.year, self.month)

class FuzzyPJDay(PJDay):
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            self.fuzziness = args[1]
            super(FuzzyPJDay, self).__init__(**kwargs)
        else:
            raise TypeError("__init__() takes 2 arguments")

    def __repr__(self):
        return "antiquity.FuzzyPJDay(%d, %r)" % (self.days, self.fuzziness)
    
    def __str__(self):
        return "Julian Day: %d +/- %d days" % (self.days, self.fuzziness.days)
    
    @property
    def start(self):
        return self - self.fuzziness
        
    @property
    def end(self):
        return self + self.fuzziness
    
class FuzzyPGDate(PGDate):
    """
    Just like a PGDate, only fuzzy!
    
    Can represent date ranges or less granular dates, like 1956, or July 1670
    
    Takes up to 3 int args - year, month and day, as well as an optional 'fuzziness' kwarg, which should be a timedelta

    Alternatively, it will accept a kwarg called days. If this is present, it overrides any args.    
    
    """
    def __init__(self, *args, **kwargs):
        self.fuzziness = kwargs.get('fuzziness', timedelta(days=0))
        if kwargs.has_key('days'):
            # julian_day
            super(FuzzyPGDate, self).__init__(**kwargs)
            return
        if len(args) == 3:
            self.create_from_YMD(*args) 
        
        elif len(args) == 2:
            self.create_from_YM(*args)
            
              
        elif len(args) == 1:
            self.create_from_Y(*args)
            
        else:
            raise TypeError("__init__() takes either 2 or 4 arguments")
           
    def create_from_YMD(self, year, month, day):
        year = int(year)
        if year < 0:
            year = year + 1
        elif year == 0:
            raise ValueError("There is no year zero - http://lmgtfy.com/?q=year+0")
        month = int(month)
        if month > 12 or month < 1:
            raise ValueError("Month must not be less than 1 or greater than 12")
        day = int(day) 
        maxdays = get_month_length(year, month)
        if day < 1 or day > maxdays:
            raise ValueError("Day must not be less than 1 or greater than %s" % maxdays)
        a = (14-month)/12
        y = year + 4800 - a
        m = month + 12*a - 3
        super(FuzzyPGDate, self).__init__(days=day+(153*m+2)/5+365*y+y/4-y/100+y/400-32046)
    
    def create_from_YM(self, year, month):
        year = int(year)
        if year < 0:
            year = year + 1
        elif year == 0:
            raise ValueError("There is no year zero - http://lmgtfy.com/?q=year+0")
        month = int(month)
        if month > 12 or month < 1:
            raise ValueError("Month must not be less than 1 or greater than 12")
        day = get_month_length(year, month)/2.0 
        self.fuzziness = self.fuzziness + timedelta(days= day)
        self.create_from_YMD(year, month, day)
            
    def create_from_Y(self, year):
        year = int(year)
        if year < 0:
            year = year + 1
        elif year == 0:
            raise ValueError("There is no year zero - http://lmgtfy.com/?q=year+0")
        month = 7 
        if is_leap_year(year):
            day = 3
            self.fuzziness = self.fuzziness + timedelta(days=366/2.0)
        else:
            day = 2.5
            self.fuzziness = self.fuzziness + timedelta(days=365/2.0)
        self.create_from_YMD(year, month, day)

            
    def __repr__(self):
        return "antiquity.FuzzyPGDate(%d, %d, %d, %r)" % (self.year, self.month, self.day, self.fuzziness)
    
    def __str__(self):
        if self.year < 0:
            return "Proleptic Gregorian Date: %dBCE-%d-%d +/- %d days" % (abs(self.year), self.month, self.day, self.fuzziness.days)
        else:
            return "Proleptic Gregorian Date: %d-%d-%d +/- %d days" % (self.year, self.month, self.day, self.fuzziness.days)
        
    @property
    def start(self):
        return self - self.fuzziness
        
    @property
    def end(self):
        return self + self.fuzziness
    