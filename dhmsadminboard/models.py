from django.db import models

# Create your models here.

SUPER_ADMIN_ACCESS = (
    ("ALLAPPS", "ALLAPPS"),
    ("ORGDHMS", "ORGDHMS"),
    ("FAMILYDHMS", "FAMILYDHMS"),
)


class SuperAdminsModel(models.Model):    
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # count = models.IntegerField(default = 10)
    email = models.EmailField(max_length= 300, default = 300)
    firstname = models.CharField(max_length= 300, default = 300)
    lastname = models.CharField(max_length= 300, default = 300)
    UniqueID = models.CharField(max_length= 300, default = 300)
    password = models.CharField(max_length= 300, default = 300)
    adminaccesslevel = models.CharField(max_length= 300,choices = SUPER_ADMIN_ACCESS, default = 'ORGDHMS', null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.email
    
    
    
    
    
