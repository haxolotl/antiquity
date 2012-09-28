Development Notes
=================

These can form the basis of the docs once everything's working.

The Problem
-----------

Python dates are good for handling recent dates, but becomes progressively less useful for historical dates. Specifically:

* BC dates aren't recognised at all.
* All python dates are proleptic Gregorian dates, which become (in some regions) problematic prior to the 1930s, and are pretty much globally useless prior to 1582.
* Python dates can't represent dates with a coarser resolution than a single day. In human terms, many historical dates are only specific to a month, year, century etc. For instance, Python lacks an object that represents a single year (eg. '1770').
* Some date methods are broken pre 1900, eg. strftime
* It ignores all other cultural and regional calendrical systems

Since a proleptic Julian day seems to be the best rosetta stone for converting dates, I think we should create a PJDay class which stores the date as a Decimal (or maybe float?) value. It should have most of the same attributes and methods as the datetime.date object, as well a shit-load of methods that perform all the conversions into other date systems. We can then subclass PJDay for each type of date object (eg. Islamic dates, Jewish dates, Gregorian dates), and override the __init__ method to convert these into a PJDay internally from whatever input parameters make sense for that class of dates.

To handle date ranges, we can subclass PJDay to create a 'fuzzy' Julian Day, by adding a timedelta attribute to indicate range either side of the centre date. FYI, I've checked the maximum size for timedeltas, and it seems it can handle < 2.7million years, so we're good on that score. By basing date ranges around a centre point, we get easy and useful sorting functionality. This approach also allows us to specify dates with a resolution greater than 1 day - eg. 1948, March 1845, 15th Century, and even approximate dates like 'mid 9th Century', 'circa 1860'.


Objects
-------

ProlepticJulianDay (PJDay) - base class which handles conversion to all other calendar system. Stores Julian Day info as a Decimal (float / int?)

FuzzyProlepticJulianDay (FPJDay) - inherits from PJDay, but adds a timedelta to indicate range either side (NB timedelta can handle < 2.7million years, so we're good)

GregorianDate (GDate) - raises error if prior to introduction of the Gregorian Calendar

FGDate

PGDate - 

FPGDate

JDate

PJDate