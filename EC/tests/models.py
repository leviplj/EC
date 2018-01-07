from django.db import models

from ecweb.models import ClassRoom, Student


class Test(models.Model):
    LISTENING = 'listening'
    READING = 'reading'

    TYPE_CHOICES = (
        (LISTENING, 'Listening'),
        (READING, 'Reading'),
    )

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    attendances = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return "{}: {}".format(self.type, self.date)