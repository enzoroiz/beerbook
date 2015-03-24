# beerbook
Coursework Web Application Development -  University of Glasgow
----------------------------------------------------------------
Team D1:
-----------------
Enzo Rioz
Liam Bergin
Tomasz Hippner
-----------------


Beerbook is a website that allows users to search for and review beers.
The site also allows users to create events to socially try out beers.



Pip requirements List:
-----------------------------------
Django==1.7
django-bootstrap-toolkit==2.15.0
django-countries==3.2
django-easy-maps==0.9
django-registration-redux==1.1
geopy==1.9.1
Pillow==2.7.0
pycparser==2.10
six==1.9.0


INSTRUCTIONS:
- install necessary packages manualy or by using pip requirements.txt
- clone repository to desired location
- run: python manage.py makemigrations beerbookapp
- run: python manage.py migrate
- (optional) populate with sample data


Population with sample data:
-----------------------------------
1.) Run: python populate_bbook.py
note: Script doesnt add images to models, these have to be added manualy,
Some sample images can be found in resources/images/

