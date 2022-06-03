from django.db import models


class EatenFood(models.Model):
    feels = (
        ('good', 'good'),
        ('normal', 'normal'),
        ('can be bad', 'can be bad'),
        ('bad', 'bad')
    )

    ate_food = models.CharField('food', max_length=100, null=True)
    feelings = models.CharField('feelings after food', choices=feels, max_length=100, null=True)

    def __str__(self):
        return f'{self.ate_food} ({self.feelings})'


class Meal(models.Model):
    feels = (
        ('good', 'good'),
        ('normal', 'normal'),
        ('bad', 'bad')
    )

    meals = (
        ('breakfast', 'breakfast'),
        ('brunch', 'brunch'),
        ('first_course', 'first course'),
        ('main_course', 'main_course'),
        ('snack', 'snack'),
        ('evening_meal', 'evening meal')
    )

    date = models.DateField('date', auto_now_add=True)
    time = models.TimeField('eating time', auto_now_add=True)
    meal = models.CharField('meal type', choices=meals, max_length=100, default=1)
    eaten_food = models.ManyToManyField(EatenFood, name='ate food')
    feelings = models.CharField('feelings after food', choices=feels, max_length=100, null=False)
    photo = models.ImageField('food photo', blank=True)

    def __str__(self):
        return f'{self.date}: {self.meal} ({self.feelings})'

