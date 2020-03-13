from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True
 
    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)
 
    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


# Create your models here.
class QRcodeConfig(SingletonModel):
    img_width = models.DecimalField(default=1.57,  max_digits=19, decimal_places=2)
    font_size = models.DecimalField(default=0.25, max_digits=19, decimal_places=2)
    inventory_margin_top=models.DecimalField(default=-0.25, max_digits=19, decimal_places=2)
    model_visibility =models.BooleanField(default=False)
    model_font_size = models.DecimalField(default=0.25, max_digits=19, decimal_places=2)
    def __str__(self):
        return 'Configuration'