from django.db import models

class Horse(models.Model):
    name = models.CharField(max_length = 50)
    color = models.CharField(max_length = 20)
    photo = models.ImageField(upload_to = "horses/")

    def total_bets(self):
        return sum(x.amount for x in self.bets.all())

    def __str__(self):
        return self.name


class Bettor(models.Model):
    name = models.CharField(max_length = 80)
    rut = models.CharField(max_length = 12, unique = True)

    def __str__(self):
        return f"{self.name} ({self.rut})"


class Bet(models.Model):
    bettor = models.ForeignKey(Bettor, on_delete = models.CASCADE)
    horse = models.ForeignKey(Horse, on_delete = models.CASCADE, related_name = "bets")
    amount = models.PositiveIntegerField()

    def calculate_payouts(house_edge = 0.1):
        bets = Bet.objects.all()
        total_bet = sum(x.amount for x in bets)
        pool = total_bet*(1-house_edge)
        payouts = {}
        for horse in Horse.objects.all():
            horse_total = sum(x.amount for x in bets if x.horse == horse)
            payouts[horse] = pool/horse_total if horse_total>0 else 1
        return payouts


    def __str__(self):
        return f"{self.bettor} -> {self.horse} (${self.amount})"


class Race(models.Model):
    is_open = models.BooleanField(default = True)
    winner = models.ForeignKey(Horse, on_delete = models.SET_NULL, null = True, blank = True)

    def total_pool(self):
        return sum(x.amount for x in Bet.objects.all())

    def __str__(self):
        return f"Carrera #{self.id}"
