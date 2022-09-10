from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import F, Case, When, Value, IntegerField, Q
from django import forms
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, timedelta
from .models import User, Lot, Category, Bid, Comit, Imagetab


# import schedule
# import time
#
# def job_with_argument(name):
#     print(f"I am {name}")
#
# schedule.every(59).seconds.do(job_with_argument, name="Peter")

class NewLotForm(forms.ModelForm):
    uploadimage = forms.ImageField(label="Up to five images can be uploaded.", required=False,
                                   widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Add category"
        # self.fields['category'].attrs={'class': 'form-control'}
        # def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
        #              required=True, widget=None, label=None, initial=None,
        #              help_text=None, to_field_name=None, *args, **kwargs):

    class Meta:
        model = Lot
        fields = ['lot_name', 'category', 'description', 'starting_price']
        widgets = {
            'lot_name': forms.TextInput(attrs={'autofocus': 'on', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': True})
        }


# class NewLotForm(forms.Form):
#     lot_name = forms.CharField(label="Lot name:",
#                                widget=forms.TextInput(attrs={'autofocus': 'on', 'class': 'form-control'}))
#     category = forms.ChoiceField(label="Category:", choices=[(i.id, i.category) for i in Category.objects.all()],
#                                  widget=forms.Select(attrs={'class': 'form-control'}))
#     description = forms.CharField(label="Description:", widget=forms.Textarea(attrs={'class': 'form-control'}))
#     starting_price = forms.IntegerField(label="Starting price:", min_value=1, max_value=99999999999999,
#                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     # picture = forms.URLField(label="URL pictures:", required=False)
#     uploadimage = forms.ImageField(label="Up to five images can be uploaded.", required=False,
#                                    widget=forms.ClearableFileInput(attrs={'multiple': True}))
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['category'].empty_label = "Категория не выбрана"

# image_img1 = forms.ImageField(label='') attrs={'class': 'lotUp formElemInlineHeight'}
# image_url2 = forms.URLField(label="URL pictures:", required=False)
# image_img2 = forms.ImageField(label='')
# image_url3 = forms.URLField(label="URL pictures:", required=False)
# image_img3 = forms.ImageField(label='')
# image_url4 = forms.URLField(label="URL pictures:", required=False)
# image_img4 = forms.ImageField(label='')
# image_url5 = forms.URLField(label="URL pictures:", required=False)
# image_img5 = forms.ImageField(label='')
# class Meta:
#     model = Lot
#     fields = ('lot_name',)

# class Meta:
#     model = Imagetab
#     fields = ('uploadimage',)
# fields = '__all__'

# category = forms.ChoiceField(label="Category:", choices=[(i, i.category) for i in Category.objects.all()])

# def __init__(self, *args, **kwargs):
#     super(NewLotForm, self).__init__(*args, **kwargs)
#     for visible in self.visible_fields():
#         visible.field.widget.attrs['class'] = 'form-control'


def index(request):
    if "page" in request.session:
        page = request.session["page"]
        del request.session['page']
        return HttpResponseRedirect(reverse("lot", args=(page,)))
    timenow = datetime.now()
    # print(request)
    # lots= Lot.objects.all().order_by(F('price').asc(nulls_last=True))
    # lots = Lot.objects.all().order_by(Coalesce('price', 'time_lot').desc(nulls_first=True))
    # lots = Lot.objects.filter(Q(price=None) | Q(time_sales__gt=datetime.now())).order_by(
    #     F('price').asc(nulls_last=True), 'time_sales', '-time_lot')
    # lots = Lot.objects.all().order_by('time_sales', 'time_lot').reverse()
    # lots = Lot.objects.values('time_sales').annotate()
    # Lot.objects.filter(time_sales__lt=timenow).update(sale=False)

    # lots = Lot.objects.annotate(
    #     lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=None,
    #                    output_field=IntegerField())).distinct().order_by(F('lot_order').asc(nulls_last=True),
    #                                                                      'time_sales', '-time_lot', )

    lots = Lot.objects.annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order', 'time_sales', '-time_lot', )

    # lots = Lot.objects.extra(select={'val': "time_sales = %s"}, select_params=(datetime(1, 1, 1, 0, 0),),)

    # print(lots.lot_order)
    # for lot in lots:
    #     print(f"{lot.lot_order} - {lot.id}")
    # print(Lot.objects.annotate(userLot__user='Yan'))

    # lots_sale = Lot.objects.exclude(Q(price=None) | Q(time_sales__gt=timenow)).order_by('-time_sales')
    # lots = Lot.objects.filter(price=None).order_by('-time_sales')
    # lots_bid = Lot.objects.filter(time_sales__gt=timenow).order_by('time_sales')

    # print(lots)
    # sales_list= Lot.objects.price.filter(price__lt=datetime.now()).all()
    # print(category)
    paginator = Paginator(lots, 15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, "auctions/index.html",
                  {"lots": page_object, 'categories': Category.objects.all(), 't_Now': timenow})
    # return render(request, "auctions/index.html",
    #               {"lots": lots, 'categories': Category.objects.all(), 't_Now': timenow})


#


# Lot.objects.order_by(F('price').desc(nulls_last=True))             Lot.objects.order_by('-price')     Lot.objects.order_by(F('price').desc(nulls_first=True))

def mylots(request):
    timenow = datetime.now()
    # lots_all = Lot.objects.filter(userLot=request.user)
    lots = Lot.objects.filter(userLot=request.user).annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order', 'time_sales', '-time_lot', )
    # lots_sale = lots_all.exclude(Q(price=None) | Q(time_sales__gt=timenow)).order_by('-time_sales')
    # lots = lots_all.filter(price=None).order_by('-time_sales')
    # lots_bid = lots_all.filter(time_sales__gt=timenow).order_by('time_sales')
    paginator = Paginator(lots, 15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, "auctions/index.html",
                  {"lots": page_object, 'category': 'My lots',
                   'categories': Category.objects.all(), 't_Now': timenow})
    # return HttpResponse(request.user)


def mybids(request):
    # lots = Lot.objects.filter(price__user=request.user).distinct()
    timenow = datetime.now()
    # lots_all = Lot.objects.filter(price__user=request.user).distinct()
    #
    # lots_sale = lots_all.exclude(Q(price=None) | Q(time_sales__gt=timenow)).order_by('-time_sales')
    # lots = lots_all.filter(price=None).order_by('-time_sales')
    # lots_bid = lots_all.filter(time_sales__gt=timenow).order_by('time_sales')

    lots = Lot.objects.filter(price__user=request.user).distinct().annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order', 'time_sales', '-time_lot', )
    paginator = Paginator(lots, 15)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, "auctions/index.html",
                  {"lots": page_object, 'category': 'My bids',
                   'categories': Category.objects.all(), 't_Now': timenow})


def category(request, category):
    timenow = datetime.now()
    # lots_all = Lot.objects.filter(category__category=category)
    #
    # lots_sale = lots_all.exclude(Q(price=None) | Q(time_sales__gt=timenow)).order_by('-time_sales')
    # lots = lots_all.filter(price=None).order_by('-time_sales')
    # lots_bid = lots_all.filter(time_sales__gt=timenow).order_by('time_sales')
    lots = Lot.objects.filter(category__category=category).annotate(
        lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
                       output_field=IntegerField())).distinct().order_by('lot_order', 'time_sales', '-time_lot', )
    paginator = Paginator(lots, 6)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, "auctions/index.html",
                  {"lots": page_object, 'category': category.title(),
                   'categories': Category.objects.all(), 't_Now': timenow})

    # print(category)
    # category_object = Category.objects.filter(category=category).first()
    # return render(request, "auctions/index.html",
    #               {"lots": Lot.objects.filter(category__category=category).annotate(
    #                   lot_order=Case(When(price=None, then=2), When(time_sales__gt=timenow, then=1), default=3,
    #                                  output_field=IntegerField())).distinct().order_by('lot_order'),
    #                'categories': Category.objects.all(),
    #                'category': category.title(), 't_Now': timenow})


def login_view(request):  # not used
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


def register(request, lot_id=0):  # not used
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
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        page = request.POST["page"]
        if page == '0':
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("lot", args=(page,)))
    else:

        return render(request, "auctions/register.html", {"form": PageInit, 'categories': Category.objects.all()})


def create_lot(request):
    # print(Imagetab.objects.last().uploadimage)
    # if request.method == 'POST':
    #     form = NewLotForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # file is saved
    #         form.save()
    #         return HttpResponseRedirect(reverse("index"))
    # else:
    #     form = NewLotForm()
    #     return render(request, "auctions/create_lot.html", {'form': form, 'categories': Category.objects.all(), 'images': Imagetab.objects.all()})

    user = User.objects.get(pk=int(request.user.id))

    if request.method == "POST":
        # print(request.POST)
        form = NewLotForm(request.POST, request.FILES)
        files = request.FILES.getlist("uploadimage")

        if form.is_valid():
            if len(files) > 5:
                return render(request, "auctions/create_lot.html", {'form': form, 'categories': Category.objects.all(),
                                                                    "message": "Only five images allowed."})
            else:
                # print(files)
                rec = Lot(
                    lot_name=form.cleaned_data['lot_name'],
                    description=form.cleaned_data['description'],
                    starting_price=form.cleaned_data['starting_price'],
                    # picture=form.cleaned_data['picture'],
                    # price=Bid.objects.filter(user=user, price=form.cleaned_data['starting_price']),
                    category=form.cleaned_data['category'],
                    # category=Category.objects.filter(pk=form.cleaned_data['category']).first(),
                    userLot=user
                )
                rec.save()
                user = User.objects.get(pk=int(request.user.id))
                user.userLot.add(rec)
                # print(files)
                for i in files:
                    print(i)

                    rec.image.add(Imagetab.objects.create(uploadimage=i))
            # lotsuser = user.userLot.all()
            # for lot in lotsuser:
            # print(lot.lot_name)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_lot.html", {'form': form, 'categories': Category.objects.all()})

    return render(request, "auctions/create_lot.html",
                  {'form': NewLotForm, 'categories': Category.objects.all(), 'images': Imagetab.objects.all()})


def lot(request, lot_id):
    print(request)
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
        bid = forms.IntegerField(label=False, min_value=min_value, max_value=99999999999999, initial=initial)

        # def __init__(self, *args, **kwargs):
        #     super(Bid_forms, self).__init__(*args, **kwargs)
        #     for visible in self.visible_fields():
        #         visible.field.widget.attrs['class'] = 'form-control'

    class Comment_forms(forms.Form):
        comment = forms.CharField(label=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

        # comment = forms.CharField(label=False, widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
        def __init__(self, *args, **kwargs):
            super(Comment_forms, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

    if request.method == "POST":

        if request.user.is_authenticated:
            user = User.objects.get(pk=int(request.user.id))
            if 'bid' in request.POST:
                form = Bid_forms(request.POST)
                if form.is_valid():

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

                    recComit = Comit(
                        user=user,
                        comit=form.cleaned_data['comment']
                    )
                    recComit.save()
                    lot.user_comit.add(recComit)
                    lot.save()
                    return HttpResponseRedirect(request.path + "#scrol")

                else:
                    return render(request, 'auctions/lot_page.html', {"lot": lot, "form": form})
        else:
            # return HttpResponseRedirect(reverse("registerlot", args=(lot_id,)))
            request.session["page"] = lot_id
            return HttpResponseRedirect(reverse("account_login"))
            # return render(request, 'account/login.html')
    return render(request, "auctions/lot_page.html",
                  {"lot": lot, "form": Bid_forms, "comment_forms": Comment_forms, 'categories': Category.objects.all(),
                   't_Now': datetime.now()})

#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
