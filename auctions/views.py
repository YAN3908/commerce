from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Lot, Category, Bid


class NewLotForm(forms.Form):
    lot_name = forms.CharField(label="Lot name:")
    description = forms.CharField(label="Description:", widget=forms.Textarea)
    starting_price = forms.IntegerField(label="Starting price:", min_value=1)
    picture = forms.URLField(label="URL pictures:", required=False)
    # category = forms.ChoiceField(label="Category:", choices=[(i, i.category) for i in Category.objects.all()])
    category = forms.ChoiceField(label="Category:", choices=[(i.id, i.category) for i in Category.objects.all()])


def index(request):
    return render(request, "auctions/index.html", {"lots": Lot.objects.all()})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request, lot_id=0):
    class PageInit(forms.Form):
        page = forms.IntegerField(widget=forms.HiddenInput(), initial=lot_id)

    print(lot_id)
    print(request.GET)
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        page = request.POST["page"]
        if page == 0:
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("lot", args=(page,)))
    else:
        return render(request, "auctions/register.html", {"form": PageInit})


def create_lot(request):
    user = User.objects.get(pk=int(request.user.id))

    if request.method == "POST":
        # print(request.POST)
        form = NewLotForm(request.POST)
        if form.is_valid():
            rec = Lot(
                lot_name=form.cleaned_data['lot_name'],
                description=form.cleaned_data['description'],
                starting_price=form.cleaned_data['starting_price'],
                picture=form.cleaned_data['picture'],
                # price=Bid.objects.filter(user=user, price=form.cleaned_data['starting_price']),
                # category=form.cleaned_data['category'],
                category=Category.objects.filter(pk=form.cleaned_data['category']).first(),
                userLot=user
            )
            rec.save()
            user = User.objects.get(pk=int(request.user.id))
            user.userLot.add(rec)
            lotsuser = user.userLot.all()
            for lot in lotsuser:
                print(lot.lot_name)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_lot.html", {'form': form})

    return render(request, "auctions/create_lot.html", {'form': NewLotForm})


def lot(request, lot_id):
    lot = Lot.objects.filter(pk=int(lot_id)).first()
    # print(lot.price.order_by("-id")[0:5]) #############################
    if lot.price.first():
        min_value = int(lot.price.last().price) + 1
        initial = int(lot.price.last().price)

        # print(lot.price.last().price)
    else:
        min_value = int(lot.starting_price) + 1
        initial = int(lot.starting_price)
        print('work')

    class Bid_forms(forms.Form):
        bid = forms.IntegerField(label="Bid:", min_value=min_value, initial=initial)

    if request.method == "POST":
        if request.user.is_authenticated:
            user = User.objects.get(pk=int(request.user.id))
            form = Bid_forms(request.POST)
            if form.is_valid():
                recBid = Bid(
                    user=user,
                    price=form.cleaned_data['bid']
                )
                recBid.save()
                lot.price.add(recBid)

                # lot.starting_price = form.cleaned_data["starting_price"]
                # lot.save()
                return HttpResponseRedirect(reverse('lot', args=(lot_id,)))
            else:
                return render(request, 'auctions/lot_page.html', {"lot": lot, "form": form})
        else:
            return HttpResponseRedirect(reverse("registerlot", args=(lot_id,)))
    return render(request, "auctions/lot_page.html", {"lot": lot, "form": Bid_forms})
