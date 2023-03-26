from django.db import models

# Create your models here.

class Contact(models.Model):
    s_no = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)
    Email = models.EmailField(max_length=50)
    Contact = models.CharField(max_length=10)
    Subject = models.CharField(max_length=50)
    Message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__ (self) :
        return 'Message from ' + self.Name
    
