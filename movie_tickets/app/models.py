from django.db import models

class Movie_details(models.Model):
    """
    This model stores the movie details like name, seat details etc..

    """
    id = models.AutoField(primary_key=True)
    theatre_name = models.CharField(max_length=100, null=False, blank=False) #saving name
    seatInfo = models.CharField(max_length=1000, null=False, blank=False) #saving the seat in jsonformat
    objects = models.Manager()  # The default manager

    class Meta:   # This is done to reprent how it should be represented in the database
        ordering = ["id"]
        verbose_name = u'Movie Detail' #It reprensent the table name
        verbose_name_plural = u'Movie Details' #It reprensent the table name

    def __str__(self): # It repesents how will we identify each row eg: inox
        return str(self.theatre_name)



