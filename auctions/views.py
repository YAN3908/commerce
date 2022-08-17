from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F, Case, When, Value, IntegerField
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, timedelta
from .models import User, Lot, Category, Bid, Comit
from django.db.models import Q


# import schedule
# import time
#
# def job_with_argument(name):
#     print(f"I am {name}")
#
# schedule.every(59).seconds.do(job_with_argument, name="Peter")

class NewLotForm(forms.Form):
    lot_name = forms.CharField(label="Lot name:", widget=forms.TextInput(attrs={'autofocus':'on'}))
    category = forms.ChoiceField(label="Category:", choices=[(i.id, i.category) for i in Category.objects.all()])
    description = forms.CharField(label="Description:", widget=forms.Textarea)
    starting_price = forms.IntegerField(label="Starting price:", min_value=1, max_value=99999999999999)
    picture = forms.URLField(label="URL pictures:", required=False)
    # category = forms.ChoiceField(label="Category:", choices=[(i, i.category) for i in Category.objects.all()])

    def __init__(self, *args, **kwargs):
        super(NewLotForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


def index(request):
    # lots = Lot.objects.filter(Q(price=None) | Q(time_sales__gt=datetime.now()))
    timenow = datetime.now()
    lots = Lot.objects.annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order','time_sales')
    # print(lots.lot_order)
    # for lot in lots:
    #     print(f"{lot.lot_order} - {lot.id}")
    # print(Lot.objects.annotate(userLot__user='Yan'))
    # lots = Lot.objects.exclude(Q(price=None) | Q(time_sales__gt=datetime.now()))
    print(lots)
    # sales_list= Lot.objects.price.filter(price__lt=datetime.now()).all()
    # print(category)
    return render(request, "auctions/index.html",
                  {"lots": lots, 'categories': Category.objects.all(), 't_Now': datetime.now()})


# Lot.objects.order_by(F('price').desc(nulls_last=True))             Lot.objects.order_by('-price')     Lot.objects.order_by(F('price').desc(nulls_first=True))

def category(request, category):
    timenow = datetime.now()
    # print(category)
    # category_object = Category.objects.filter(category=category).first()
    return render(request, "auctions/index.html",
                  {"lots": Lot.objects.filter(category__category=category).annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order'),
                   'categories': Category.objects.all(),
                   'category': category.title(), 't_Now': timenow})


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
        return render(request, "auctions/login.html", {'categories': Category.objects.all()})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request, lot_id=0):
    class PageInit(forms.Form):
        page = forms.IntegerField(widget=forms.HiddenInput(), initial=lot_id)

    # print(lot_id)
    # print(request.GET)
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        form = PageInit(request.POST)
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.", "form": form
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.", "form": form
            })
        login(request, user)

        page = request.POST["page"]
        if page == '0':
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("lot", args=(page,)))
    else:

        return render(request, "auctions/register.html", {"form": PageInit, 'categories': Category.objects.all()})


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
            # lotsuser = user.userLot.all()
            # for lot in lotsuser:
            # print(lot.lot_name)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_lot.html", {'form': form, 'categories': Category.objects.all()})

    return render(request, "auctions/create_lot.html", {'form': NewLotForm, 'categories': Category.objects.all()})


def lot(request, lot_id):
    lot = Lot.objects.filter(pk=int(lot_id)).first()

    # if delta_time < timedelta(hours=0):

    # print(lot.price.order_by("-id")[0:5]) #############################
    if lot.price.first():
        min_value = int(lot.price.last().price) + 1
        initial = int(lot.price.last().price)

        # print(lot.price.last().price)
    else:
        min_value = int(lot.starting_price) + 1
        initial = int(lot.starting_price)
        # print('work')

    class Bid_forms(forms.Form):
        bid = forms.IntegerField(label="Bid:", min_value=min_value, max_value=99999999999999, initial=initial)

    class Comment_forms(forms.Form):
        comment = forms.CharField(label="Сomment:", widget=forms.Textarea)

    if request.method == "POST":
        print(request.POST)
        if request.user.is_authenticated:
            user = User.objects.get(pk=int(request.user.id))
            if 'bid' in request.POST:
                form = Bid_forms(request.POST)
                if form.is_valid():
                    print('valid')
                    recBid = Bid(
                        user=user,
                        price=form.cleaned_data['bid'],
                        time_lot=datetime.now() + timedelta(hours=1.5)
                    )
                    recBid.save()
                    lot.price.add(recBid)
                    lot.time_sales = datetime.now() + timedelta(hours=1.5)
                    lot.save()

                    # lot.starting_price = form.cleaned_data["starting_price"]
                    # lot.save()
                    return HttpResponseRedirect(reverse('lot', args=(lot_id,)))
                else:
                    return render(request, 'auctions/lot_page.html', {"lot": lot, "form": form})
            if 'comment' in request.POST:
                form = Comment_forms(request.POST)
                if form.is_valid():
                    print('valid')
                    recComit=Comit(
                        user=user,
                        comit=form.cleaned_data['comment']
                    )
                    recComit.save()
                    lot.user_comit.add(recComit)
                    lot.save()
                    return HttpResponseRedirect(request.path)
                else:
                    return render(request, 'auctions/lot_page.html', {"lot": lot, "form": form})
        else:
            return HttpResponseRedirect(reverse("registerlot", args=(lot_id,)))
    return render(request, "auctions/lot_page.html",
                  {"lot": lot, "form": Bid_forms, "comment_forms": Comment_forms, 'categories': Category.objects.all(),
                   't_Now': datetime.now()})

#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
