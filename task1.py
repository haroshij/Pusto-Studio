from django.db import models
from django.http.response import HttpResponse


class Boost(models.Model):
    boost_type = models.CharField(
        max_length=256,
        verbose_name='Boost Type')
    description = models.TextField(verbose_name='Description')


class Player(models.Model):

    name = models.CharField(
        max_length=256,
        verbose_name='Name')
    boost = models.ForeignKey(Boost, on_delete=models.SET_NULL, null=True)
    first_login = models.DateTimeField()
    daily_bonus = models.IntegerField()

    def assign_boost(self):
        if self.is_completed:
            self.boost = Boost.objects.get(boost_type='temporary')
            self.save()


# Метод для ручного назначения буста.
def assign_manual_boost(request, player_id):
    player = Player.objects.get(id=player_id)
    boosts = Boost.objects.all()
    if request.user.is_staff:
        boost = boosts.first()
        player.boost = boost
        player.save()
    return HttpResponse('Boost has been successfully assigned')
