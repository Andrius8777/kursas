from django.db import models
from django.contrib.auth import get_user_model
import datetime, decimal
 

class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    username = models.CharField(max_length=150) 
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)
    number_plate = models.CharField(max_length=10)
    vin_number = models.CharField(max_length=17)
    year = models.IntegerField()
    year_choices = [(year, year) for year in range(1990, datetime.date.today().year + 1)]
    engine_type = models.CharField(
        max_length=10, choices=[('diesel', 'Diesel'),
        ('petrol', 'Petrol'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric')],
    )
    engine_power_choices = [(kw, kw) for kw in range(40, 401)]
    engine_power_kw = models.IntegerField(choices=engine_power_choices)
    engine_capacity_choices = [(decimal.Decimal(str(litre)),
        decimal.Decimal(str(litre))) for litre in [round(0.1 * i, 1) for i in range(9, 61)]]
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1, choices=engine_capacity_choices)
    created_date = models.DateTimeField(auto_now_add=True)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.SET_NULL, null=True)
    repairs = models.ManyToManyField('Repair', blank=True)

    CAR_MAKE_CHOICES = [
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('MB', 'MB'),
        ('VW', 'VW'),
        ('VOLVO', 'VOLVO'),
        ('PEUGOET', 'PEUGOET'),
        ('LEXUS', 'LEXUS'),
        ('SKODA', 'SKODA'),
        ('RENAULT', 'RENAULT'),
        ('CITROEN', 'CITROEN'),
        ('FIAT', 'FIAT'),
        ('TOYOTA', 'TOYOTA'),
        ('FORD', 'FORD'),
        ('OPEL', 'OPEL'),
        ('PORSCHE', 'PORSCHE'),
    ]

    car_make = models.CharField(max_length=100, choices=CAR_MAKE_CHOICES)
    car_model = models.CharField(max_length=100, choices=[], blank=True)

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(*args, **kwargs)
        self._set_car_model_choices()

    def _set_car_model_choices(self):
        if self.car_make:
            car_models = {'Audi': [('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A5', 'A5'), 
                    ('Q3', 'Q3'), ('Q5', 'Q5'), ('Q7', 'Q7')],
                'BMW': [('1 Series', '1 Series'), ('2 Series', '2 Series'), ('3 Series', '3 Series'), 
                    ('4 Series', '4 Series'), ('5 Series', '5 Series'), ('X1', 'X1'), ('X3', 'X3'), ('X5', 'X5')],
                'MB': [('A-Class', 'A-Class'), ('C-Class', 'C-Class'), ('E-Class', 'E-Class'), ('S-Class', 'S-Class'),
                    ('GLA', 'GLA'), ('GLC', 'GLC'), ('GLE', 'GLE'), ('GLS', 'GLS')],
                'VOLVO': [('S60', 'S60'), ('S90', 'S90'), ('V60', 'V60'), ('V90', 'V90'),
                    ('XC40', 'XC40'), ('XC60', 'XC60'), ('XC90', 'XC90')],
                'PEUGOET': [('108', '108'), ('208', '208'), ('308', '308'), ('508', '508'),
                    ('2008', '2008'), ('3008', '3008'), ('5008', '5008')],
                'LEXUS': [('CT', 'CT'), ('IS', 'IS'), ('ES', 'ES'), ('GS', 'GS'), 
                    ('NX', 'NX'), ('RX', 'RX'), ('RX', 'RX'), ('UX', 'UX')],
                'SKODA': [('Fabia', 'Fabia'), ('Octavia', 'Octavia'), ('Superb', 'Superb'),
                    ('Kodiaq', 'Kodiaq'), ('Karoq', 'Karoq')],
                'RENAULT': [('Clio', 'Clio'), ('Megane', 'Megane'), ('Scenic', 'Scenic'),
                    ('Captur', 'Captur'), ('Kadjar', 'Kadjar')],
                'CITROEN': [('C1', 'C1'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'),
                    ('Berlingo', 'Berlingo')],
                'FIAT': [('500', '500'), ('Panda', 'Panda'), ('Tipo', 'Tipo'),
                    ('500L', '500L'), ('500X', '500X')],
                'TOYOTA': [('Yaris', 'Yaris'), ('Corolla', 'Corolla'), ('Camry', 'Camry'),
                    ('RAV4', 'RAV4'), ('Highlander', 'Highlander')],
                'FORD': [('Fiesta', 'Fiesta'), ('Focus', 'Focus'), ('Mondeo', 'Mondeo'),
                    ('Kuga', 'Kuga'), ('Edge', 'Edge')],
                'OPEL': [('Corsa', 'Corsa'), ('Astra', 'Astra'), ('Insignia', 'Insignia'),
                    ('Crossland X', 'Crossland X'), ('Grandland X', 'Grandland X')],
                'PORSCHE': [('911', '911'), ('Cayenne', 'Cayenne'), ('Panamera', 'Panamera'),
                    ('Macan', 'Macan'), ('Taycan', 'Taycan')],
        }
        self.car_model_choices = car_models.get(self.car_make, [])
        self._meta.get_field('car_model').choices = self.car_model_choices
        
    def save(self, *args, **kwargs):
        self._set_car_model_choices()  
        super(Customer, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self._set_car_model_choices()  
        super(Customer, self).save(*args, **kwargs)
        
        
class Mechanic(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    

class Repair(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    part_description = models.CharField(max_length=255)
    part_price = models.DecimalField(max_digits=10, decimal_places=2)  
    labor_price = models.DecimalField(max_digits=10, decimal_places=2)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  


