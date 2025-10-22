from django.shortcuts import render, redirect, get_object_or_404
from .models import Horse, Bet, Bettor, Race
from .forms import BetForm
from .utils import calculate_payouts

def betting_view(request):
    race, created = Race.objects.get_or_create(is_open = True)
    horses = Horse.objects.all()
    total_pool = race.total_pool()
    return render(request, "betting/betting.html", {
        "horses": horses,
        "total_pool": total_pool,
        "race": race,
    })


def place_bet(request, horse_id):
    horse = get_object_or_404(Horse, id = horse_id)
    if request.method == "POST":
        form = BetForm(request.POST)
        if form.is_valid():
            bettor, _ = Bettor.objects.get_or_create(
                rut = form.cleaned_data["rut"]
                defaults = {"name": form.cleaned_data["name"]} 
            )
            Bet.objects.create(
                bettor = bettor,
                horse = horse,
                amount = form.cleaned_data["amount"]
            )
            return redirect("betting_view")
    else:
        form = BetForm()
    return render(request, "betting/place_bet.html", {"form": form, "horse", horse})


def close_bets(request):
    race = Race.objects.filter(is_open = True).first()
    if race:
        race.is_open = False
        race.save()
    return redirect("betting_view")


def select_winner(request, horse_id):
    race = Race.objects.filter(is_open = False, winerr_isnull = True).first()
    if race:
        race.winner_id = horse_id
        race.save()
    return redirect("result_view", race_id = race.id)


def result_view(request, race_id):
    race = get_object_or_404(Race, id = race_id)
    payouts = Bet.objects.calculate_payouts()
    return render(request, "betting/results.html", {
        "race": race,
        "payouts": payouts
    })


def index(request):
    horses = Horse.objects.all()
    bets = Bet.objects.all()
    payouts = calculate_payouts(bets)
    total_bets = sum(b.amount for b in bets)

    for horse in horses:
        horse.total_bet = sum(b.amount for b in bets if b.horse == horse)
        horse.payout_ratio = round(payouts.get(horse, 0), 2)

    return render(request, "betting/index.html", {
        "horses": horses,
        "total_bets": total_bets,
    })

