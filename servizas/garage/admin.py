from django.contrib import admin
from . import models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer', 'phone_number', 'number_plate',
                    'car_model', 'car_make', 'vin_number', 'year', 'engine_type', 
                    'engine_power_kw', 'engine_capacity', 'suspension_type', 'mechanic', 'created_date']
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['car_make'].widget.attrs['onchange'] = 'update_car_models(this.value);'
        return form
    
    class Media:
        js = ('custom_script.js',) 
    # fieldsets = (cus
    #     (None, {
    #         "fields": (
    #             'name', 'owner',
    #         ),
    #     }),
    # )

    def total_cars(self, obj: models.Customer):
        return obj.customer.count()
    total_cars.short_description = "total cars repaired"


class MechanicAdmin(admin.ModelAdmin):
    list_display = ['name']
   

class RepairAdmin(admin.ModelAdmin):
    list_display = ['part_description', 'part_price', 'labor_price', 'total_price']
    
    

admin.site.register(models.Customer, CustomerAdmin )  
admin.site.register(models.Mechanic, MechanicAdmin)
admin.site.register(models.Repair, RepairAdmin)