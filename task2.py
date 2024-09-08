from django.db import models
from django.http.response import HttpResponse
import csv


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField()


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    # Заводим дополнительное поле для приза
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, null=True)

    # Вызываем метод ниже, когда порйден уровень.
    def assign_prize(self):
        if self.is_completed:
            self.prize = Prize.objects.first()
            self.save()


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()


# Метод для выгрузки данных в csv-файл.
def export_data(request):
    player_levels = PlayerLevel.objects.all()
    data = [{'id': player_level.player.player_id,
             'title': player_level.level.title,
             'is level comleted': player_level.is_completed,
             'level prize': player_level.prize.title} for player_level in player_levels]

    with open('data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'is level comleted', 'level prize'])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return HttpResponse('The data has been successfully exported')
