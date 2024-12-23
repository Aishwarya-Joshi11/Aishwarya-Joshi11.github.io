from django.db import models


class PredResults(models.Model):

    input1 = models.CharField(max_length=100)
    input2 = models.CharField(max_length=100)
    input3 = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)


    def __str__(self):
        return self.classification