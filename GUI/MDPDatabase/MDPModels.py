from django.db import models

class Password(models.Model):
    id = models.AutoField(null=False)
    site = models.CharField(null=False)
    username = models.CharField(null=False)
    password = models.CharField(null=False)

    def __list__(self):
        return [self.id, self.site, self.username, self.password]
    
