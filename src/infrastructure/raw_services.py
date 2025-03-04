from django.db import models

class RawServicesBase:

    def raw_delete(self, model: models.Model, *args):
        m = model.objects.raw("DELETE FROM %s WHERE id IN %s", [*args])
        print(m.query)
    
    
    def delete_many_records(self,model: models.Model, *args, **kwargs):
        model.objects.filter(**kwargs).delete()