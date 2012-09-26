
import math
from datetime import date


class HistoricalDate:

    def __init__(self, year, month, day):
        """
        see http://www.hermetic.ch/cal_stud/jdn.htm#comp
        http://www.merlyn.demon.co.uk/daycount.htm#GDDC
        http://www.tondering.dk/claus/cal/julperiod.php#formula
        http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?bibcode=1983IAPPP..13...16F&db_key=AST&page_ind=0&data_type=GIF&type=SCREEN_VIEW&classic=YES
        """

        year = int(year)
        month = int(month)
        day = int(day)
        a = (14-month)/12
        y = year + 4800 - a
#        print a,"a"
        m = month + 12*a - 3
#        print m,"m"
#        print y,"y"
        self.julian_day = day+(153*m+2)/5+365*y+y/4-y/100+y/400-32045

    
