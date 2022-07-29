# from django.contrib.auth import authenticate, login, logout
# from django.db import IntegrityError
# from django import forms
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
#
# from .models import User, Lot, Category,Bid


class NewLotForm(forms.Form):
    lot_name = forms.CharField(label="Lot name:")
    description = forms.CharField(label="Description:", widget=forms.Textarea)
    starting_price = forms.IntegerField(label="Starting price:", min_value=1)
    picture = forms.URLField(label="URL pictures:", required=False)
    # category = forms.ChoiceField(label="Category:", choices=[(i, i.category) for i in Category.objects.all()])
    category = forms.ChoiceField(label="Category:", choices=[(i.id, i.category) for i in Category.objects.all()])

def index(request):
    user = User.objects.get(pk=int(request.user.id))
    if request.method == "POST":
        form = NewLotForm(request.POST)
        if form.is_valid():
            # print(request.POST['starting_price'])
            # print(Category.objects.first())
            recBid = Bid(
                user=user,
                price=form.cleaned_data['starting_price']
            )
            recBid.save()

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
            bid=Bid.objects.filter(user=user, price=form.cleaned_data['starting_price']).first()
            lot = Lot.objects.last()
            print(lot.lot_name)
            lot.price.add(bid)
            print(bid.price)
            # Lot.price.add(recBid)
            # pictures = Lot.objects.filter(pk=8).first()

    # use = User.objects.get(pk=int(request.user.id))
    # print(use.userLot.filter(lot_name='tvar'))

    # for ca in pictures:lot
        # print(ca.picture)
    # print(ca)
    # categ = Category.objects.all()
    #  categ = Category.objects.get(pk=2).category
    # print(categ.lotCategory)
    # lot = Lot.objects.get(pk=2)
    # print(lot.category.category)

    # print(Category.objects.only('category'))
    # cat = Category.objects.all()
    # save = [(i, i.category) for i in Category.objects.all()]
    # print(save)
    # for ca in cat:
    #     print(ca)
    # rec = Lot(
    #     lot_name="buyan",
    #     description="qwertyui",
    #     starting_price=1,
    #     picture="",
    #     category=categ,
    #     userLot=use
    # )
    # rec.save()

    return render(request, "auctions/index.html", {'form': NewLotForm})


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


def register(request):
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
