from base64 import urlsafe_b64decode
from django.shortcuts import render, redirect, HttpResponse
from .models import Account, MovieCategory
from .models import Movie, Screen
from .models import Showtime
from .models import CardEncr
from .models import Promotion
from .models import Ticket
from .models import Order
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from .enums import Price
from users.models import User
from .forms import CreatePromo,SendPromo
from .models import Account, MovieCategory,Movie, Screen,Showtime,CardEncr,Promotion,Ticket,Order
from home.validators import validate_password, validate_email,validate_username,confirm_password
import ast

def login_view(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if(request.GET.get('next') == '/booking'):
                return redirect(request.GET.get('next')+'?movie='+request.GET.get('movie'))
            elif(request.GET.get('next') == '/seatselect'):
                return redirect(request.GET.get('next')+'?shownum='+request.GET.get('shownum'))
            elif(request.GET.get('next') == '/orderedit'):
                return redirect(request.GET.get('next')+'?shownum='+request.GET.get('shownum')+'&selectedSeats='+request.GET.get('selectedSeats'))
            else:
                return redirect('/')
        else:
            return render(request, '../templates/registration/login.html', {'error': 'Invalid username or password'})
    else:
        if(request.GET.get('next') == '/booking'):
            context = {'next':request.GET.get('next'),'movie':request.GET.get('movie')}
        elif(request.GET.get('next') == '/seatselect'):
            context = {'next':request.GET.get('next'),'shownum':request.GET.get('shownum')}
        elif(request.GET.get('next') == '/orderedit'):
            context = {'next':request.GET.get('next'),'shownum':request.GET.get('shownum'),'selectedSeats':request.GET.get('selectedSeats')}
        else:
            context = {}
        return render(request, '../templates/registration/login.html',context)

def registration(request):
    if request.method == 'POST':
        # Process form data
        user_name = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        address = request.POST['address']
        phone = request.POST['phone']
        if 'enrollForPromotions' in request.POST and request.POST['enrollForPromotions'] == 'on':
            enrollForPromotions = True
        else:
            enrollForPromotions = False

        # Create a new user object but don't save it yet
        # if email and user_name and password1 and  password2:
        try:
            if email:
                validate_email(email)
            if user_name:
                validate_username(user_name)
            if password1:
                validate_password(password1)
            if password1 and password2:
                confirm_password(password1,password2)
        except ValidationError as e:
            messages.error(request,str(e.message))
            return render(request, '../templates/registration.html')
        
        user = User.objects.create_user(
            user_name=user_name,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=False,
            is_staff=False,
            address=address,
            phone=phone if phone != '' else None,
            is_admin=False,
            enrollForPromotions=enrollForPromotions
        )

        # Generate activation link
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uidb64, 'token': token}))

        # Send activation email to the user's email address
        subject = 'Activate Your Account'
        message = f'Hi {first_name},\n\nPlease click the following link to activate your account:\n\n{activation_link}'
        from_email = 'SEteamc9@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return HttpResponseRedirect(reverse('registration_success'))

    else:
        # Display empty registration form
        return render(request, '../templates/registration.html')

def activation_success(request):
    return render(request, '../templates/activation_success.html')

def activate(request, uidb64, token):
    # Get user object by primary key
    try:
        uidb64 += '=' * ((4 - len(uidb64) % 4) % 4)
        uid = force_str(urlsafe_b64decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse('Invalid activation link')

    # Activate user account
    user.is_active = True
    user.save()

    # Redirect to success page
    return HttpResponseRedirect(reverse('activation_success'))

def registration_success(request):
    return render(request, '../templates/registration_success.html')

def resetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user is not None:
                # Generate activation link
                activation_link = request.build_absolute_uri(reverse('forgotpassword',kwargs={'username':user.user_name}))
                subject = "Reset your password"
                message = f'Hi {user.first_name},\n\nPlease click the following link to reset your password:\n\n{activation_link}'
                from_email = 'SEteamc9@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return HttpResponseRedirect(reverse('resetpassword_email'))
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist as e:
            error = True
            return render(request, "../templates/resetpassword.html", {'error': error})
    return render(request, "../templates/resetpassword.html")

def resetpassword_email(request):
    return render(request, '../templates/resetpassword_email.html')

def resetpassword_success(request):
    return render(request, '../templates/resetpassword_success.html')

def forgotpassword(request,username):
    if request.method == 'POST':
        newpassword = request.POST.get('newpassword')
        newpassword1 = request.POST.get('newpassword1')
        # try to find user with matching email and change password
        try:
            user = User.objects.get(user_name=username)
            if user is not None:
                if newpassword != '' and newpassword is not None:
                    try:
                        validate_password(newpassword)
                        confirm_password(newpassword,newpassword1)
                    except ValidationError as e:
                        messages.error(request, str(e.message))
                        return render(request, '../templates/forgotpassword.html')
                user.set_password(newpassword)
                user.save()
                return redirect('/resetpassword_success')
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist as e:
            error = True
            return render(request, "../templates/forgotpassword.html", {'error': error})
    context = {'user_name':username}
    return render(request, "../templates/forgotpassword.html",context)

def changepassword(request):
    if request.method == 'POST':
        username = request.user.user_name
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        newpassword1 = request.POST.get('newpassword1')
        # try to find user with matching email and change password
        try:
            user = authenticate(username=username,password=oldpassword)
            if user is not None:
                if newpassword and newpassword1:
                    try:
                        validate_password(newpassword)
                        confirm_password(newpassword,newpassword1)
                    except ValidationError as e:
                        messages.error(request, str(e.message))
                        return render(request, '../templates/changepassword.html')
                user.set_password(newpassword)
                user.save()
                
                # Send activation email to the user's email address
                subject = 'Password change'
                message = f'Hi {user.first_name},\n\n Your password was changed, if it was not you please contact admin at seteamc9@gmail.com'
                from_email = 'SEteamc9@gmail.com'
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                return redirect('/')
            else:
                raise User.DoesNotExist()
        except User.DoesNotExist as e:
            error = True
            return render(request, "../templates/changepassword.html", {'error': error})
    # context = {'user':request.user}
    return render(request, "../templates/changepassword.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, '../templates/logout.html')
    else:
        return render(request, '../templates/home.html')

def user_profile(request):
    users = request.user
    users = User.objects.get(user_name = users)
    cards = Account.objects.filter(user=users)
    orders = Order.objects.filter(userID= users)
    cardList = []
    if cards.count() == 0:
        accountRemaining = 3
    else:
        accountRemaining = 3 - cards.count()
        for card in cards:
            cardno = card.cardNo
            fernet = CardEncr.fernet
            bites = bytes(cardno, 'utf-8')
            decoded = fernet.decrypt(bites).decode()
            decoded = decoded[-4:]
            cardList.append(decoded)
    context = {'users': users, 'accountRemain': accountRemaining, 'cards': cardList,'orders':orders}
    return render(request, '../templates/user-profile.html', context)

def editprofile(request):
    context = {}
    if request.method == 'POST':
        users = request.user
        cards = Account.objects.filter(user=users)
        context = {'users': users,'cards': cards}
        f = request.POST.get('fname')
        if f is not None and len(f) != 0 :
            users.first_name = f
        l = request.POST.get('lname')
        if l is not None and len(l) != 0:
            users.last_name = l
        a = request.POST.get('address')
        if a is not None and len(a) != 0:
            users.address = a
        p = request.POST.get('password')
        if p is not None and len(p) != 0:
            users.set_password(request.POST.get('password'))
            update_session_auth_hash(request, User)
        enroll = request.POST.get('enrollForPromotions', False)
        if enroll is not None and enroll == 'on' :
            users.enrollForPromotions = True
        else:
            users.enrollForPromotions = False
        t = request.POST.get('phone')
        if t is not None and len(t) != 0:
            users.phone = t
        users.save()
        return HttpResponse(user_profile(request))
    return render(request, '../templates/editprofile.html', context)

def addCard(request):
    user = request.user
    
    count = Account.objects.filter(user=user).count()
    cards = Account.objects.filter(user= user)
    context = {'cards':cards,'accountRemain':3-count}
    if request.method == "POST" and count < 3:
        cardno = request.POST.get('cardno')
        exp = request.POST.get('exp')
        if cardno and exp :
            fernet = CardEncr.fernet
            # cardno = cardno.encode()
            # cardNoEnc = fernet.encrypt(cardno).decode()
            cardNoEnc = fernet.encrypt(cardno.encode()).decode()
            # account = Account()
            # account.cardNo=cardNoEnc
            # account.exp=exp
            # account.user=user
            # account.save()
            account = Account(cardNo=cardNoEnc, exp=exp, user=user)
            account.save()
            return HttpResponse(user_profile(request))
    return render(request, '../templates/add-card.html', context)

def addmovie(request):
    context = {}
    if request.method == 'POST':
        movie = Movie()
        if('title' in request.POST):
            movie.title = request.POST['title']
            movie.cast = request.POST['cast']
            movie.synopsis = request.POST['synopsis']
            movie.rating = request.POST['rating']
            movie.release_date = request.POST['release_date']
            movie.trailer_picture = request.POST['trailer_picture']
            movie.trailer_video = request.POST['trailer_video']
            movie.genre = request.POST['genre']
            movie.director = request.POST['director']
            movie.producer = request.POST['producer']
            cert = request.POST['certificate']
            movie.certificate = MovieCategory.objects.get(pk=cert)
            if 'playing_now' in request.POST and request.POST['playing_now'] == 'on':
                movie.playing_now = True
            else:
                movie.playing_now = False
            movie.save()
    return render(request,'../templates/addmovie.html',context)

def schedule_movie(request):
    now_playing = None
    message = None
    now_playing = Movie.objects.filter(playing_now=True)
    if request.method == 'POST':
        showtime = Showtime()
        movie = Movie.objects.get(title = request.POST.get('movieID'))
        showtime.movieID = movie
        screen = Screen.objects.get(screen = request.POST['screenID'])
        showtime.screenID = screen
        showtime.time = request.POST['time']
        entered_time = datetime.strptime(request.POST['time'], '%Y-%m-%dT%H:%M')
        hours = int(movie.duration[:2])
        minutes = int(movie.duration[3:5])
        showtime.end_time = entered_time + timedelta(hours=hours, minutes=minutes)
        showtime.save()
        showtime.createSeats()
    context = {'movies':now_playing,'message':message}
    return render(request, '../templates/schedule_movies.html',context)

def home(request):
    user = request.user
    now_playing = Movie.objects.filter(playing_now=True)
    coming_soon = Movie.objects.filter(playing_now=False)
            
    context = {'user':user,'playing_now': now_playing, 'coming_soon': coming_soon}

    if request.method == 'POST':
        searchStr = request.POST.get('search')
        filt = request.POST.get('filter')
        if filt == 'genre':
            # catSearch = Movie.objects.filter(genre__icontains=searchStr)
            now_playing = Movie.objects.filter(genre__icontains=searchStr, playing_now=True)
            coming_soon = Movie.objects.filter(genre__icontains=searchStr, playing_now=False)
            context = {'user':user,'playing_now': now_playing, 'coming_soon': coming_soon}
        elif filt == 'title':
            now_playing = Movie.objects.filter(title__icontains=searchStr, playing_now=True)
            coming_soon = Movie.objects.filter(title__icontains=searchStr, playing_now=False)
        context = {'user':user,'playing_now': now_playing, 'coming_soon': coming_soon}
        return render(request, '../templates/search.html', context)
    return render(request, '../templates/home.html', context)

def search(request, new_context):
    user = request.user
    context = new_context

    if request.method == 'POST':
        searchStr = request.POST.get('search')
        filt = request.POST.get('filter')
        if filt == 'genre':
            # catSearch = Movie.objects.filter(genre__icontains=searchStr)
            now_playing = Movie.objects.filter(genre__icontains=searchStr, playing_now=True)
            coming_soon = Movie.objects.filter(genre__icontains=searchStr, playing_now=False)
            context = {'user':user,'playing_now': now_playing, 'coming_soon': coming_soon}
        elif filt == 'title':
            now_playing = Movie.objects.filter(title__icontains=searchStr, playing_now=True)
            coming_soon = Movie.objects.filter(title__icontains=searchStr, playing_now=False)
        context = {'user':user,'playing_now': now_playing, 'coming_soon': coming_soon}
        return render(request, '../templates/search.html', context)

    return render(request, '../templates/search.html', context)

def adminPromo(request):
    promos = Promotion.objects.all()
    if request.method =="POST":
        form = CreatePromo(request.POST)
        form2 = SendPromo()
        if form.is_valid():
            form.save()
            form = CreatePromo()
            return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})
        # send promo to emails of users who enrolled for promotions
    if request.method == "POST" and not form.is_valid():
        form = CreatePromo()
        form2 = SendPromo(request.POST)
        if form2.is_valid():
            users = User.objects.filter(is_staff=False)
            promo = form2.cleaned_data['promos']
            for user in users:
                if user.enrollForPromotions:
                    emailAddr = user.email
                    name = user.first_name
                    promoId = promo.promoID
                    promoAmount = promo.amount
                    promoValid = promo.valid_thru
                    template = render_to_string('../templates/email-template2.html',
                                                {'name': name, 'id': promoId, 'amount': promoAmount, 'valid': promoValid})
                    email = EmailMessage(
                        'We have a new promotion for you!',
                        template,
                        settings.EMAIL_HOST_USER,
                        [emailAddr]
                    )
                    email.fail_silently = True
                    email.send()
            form2 = SendPromo()
            return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})

    form = CreatePromo()
    form2 = SendPromo()
    return render(request, '../templates/admin-promo.html', {'promos': promos, 'form': form, 'form2': form2})

def send_promo(request):
    # update code
    context = {}
    return render(request, '../templates/admin-send-promo.html', context)

def booking(request):
    moviestring = ''
    if request.method == 'GET':
        moviestring = request.GET.get('movie')
    movie = Movie.objects.get(title=moviestring)
    genreStr = movie.genre
    showtimes = Showtime.objects.filter(movieID=movie).order_by('time')
    show = []
    for showtime in showtimes:
        if showtime.time > datetime.now(showtime.time.tzinfo):
            show.append(showtime)
    context = {'movie': movie, 'showtimes': show, 'genre': genreStr}
    return render(request, '../templates/movie_details.html', context)

def seatselect(request):
    user = request.user
    num = chr(65)
    shownum = request.GET.get('shownum')
    showtime = Showtime.objects.get(shownum=shownum)
    movie = showtime.movieID
    seats = Ticket.objects.filter(shownum=showtime)
    context = {'movie': movie, 'showtime': showtime, 'seats': seats, 'num': num, 'user': user}
    if request.method == 'POST':
        selectedSeats = request.POST.getlist('seat')
        if len(selectedSeats) == 0:
            error = True
            context = {'movie': movie, 'showtime': showtime, 'seats': seats, 'num': num, 'user': user, 'error': error}
            return render(request, '../templates/seatselection.html', context)
        else:
            return redirect(reverse('orderedit') + '?shownum=' + str(showtime.shownum) + '&selectedSeats=' + str(selectedSeats))
    return render(request, '../templates/seatselection.html', context)

def orderedit(request):
    user = request.user
    shownum = request.GET.get('shownum')
    selectedSeats = request.GET.get('selectedSeats')
    selectedSeats = ast.literal_eval(selectedSeats)
    showtime = Showtime.objects.get(shownum=shownum)
    movie = showtime.movieID
    context = {'showtime': showtime, 'movie': movie,'selectedSeats':selectedSeats}
    tickets = []
    if request.method == 'POST':
        adult = int(request.POST.get('adult'))
        child = int(request.POST.get('child'))
        senior = int(request.POST.get('senior'))
        totalCount = adult + child + senior
        if totalCount != len(selectedSeats):
            error = True
            context = {'showtime': showtime, 'movie': movie, 'error': error}
            return render(request, '../templates/order_edit.html', context)
        else:
            for seat in selectedSeats:
                ticket = {}
                ticket['seatNum'] = seat
                tickets.append(ticket)
            count = 0
            for ticket in tickets:                
                if count < adult:
                    ticket['price'] = Price.ADULT.value
                elif count < adult + child:
                    ticket['price'] = Price.CHILD.value
                else:
                    ticket['price'] = Price.SENIOR.value
                count = count + 1
        return redirect(reverse('checkout') + '?shownum=' + shownum + '&tickets=' + str(tickets))
    return render(request, '../templates/order_edit.html', context)

def checkout(request):
    context = {}
    user = request.user
    shownum = request.GET.get('shownum')
    tickets = request.GET.getlist('tickets')
    showtime = Showtime.objects.get(shownum=shownum)
    movie = showtime.movieID
    accounts = Account.objects.filter(user=user)
    numAccounts = accounts.count()
    tickets = tickets[0]
    tickets = ast.literal_eval(tickets)
    ticketCount = len(tickets)
    seatPrices = 0
    for ticket in tickets:
        seatPrices += ticket['price']
    tax = round((seatPrices * .07), 3)
    total = seatPrices + tax
    cardApplied = False
    order = {}
    context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
               'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied}
    if request.method == 'POST':
        formName = request.POST.get('name')
        if formName == 'cardsForm':
            card = request.POST.get('card')
            account = Account.objects.get(accountID=card)
            prmoamt = 0
            if request.POST.get('PromoAmount'):
                prmoamt = round(int(request.POST.get('PromoAmount')[0:]),2)
                order['total'] = total - prmoamt
            else:
                order['total'] = total
            order['numTickets'] = ticketCount
            order['total'] = round(order['total'],2)
            order['accountID'] = account.accountID
            cardApplied = True
            context = {'showtime': showtime, 'card': card, 'PromoAmount':prmoamt ,'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                       'tax': tax, 'total': order['total'], 'accounts': accounts, 'cardApplied': cardApplied,'order':order}
            return render(request, '../templates/checkout.html', context)
        if formName == 'cardinfoForm' and numAccounts < 3:
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            ccnum = request.POST.get('cardnumber')
            exp = request.POST.get('exp')
            if len(address) != 0 and len(city) != 0 and len(zip) != 0 and len(ccnum) != 0 and len(exp) != 0 or state is not None:
                us = User.objects.get(user_name = request.user)
                us.address = address +','+ city + zip
                fernet = CardEncr.fernet
                cardno = ccnum.encode('utf-8')
                cardNoEnc = fernet.encrypt(cardno).decode()
                account = Account(cardNo=cardNoEnc, exp=exp,  user=user)
                account.save()
                order['total'] = total
                order['numTickets'] = ticketCount
                order['accountID'] = account.accountID
                cardApplied = True
                context = {'showtime': showtime,'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                           'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied,'order':order}
                return render(request, '../templates/checkout.html', context)
            else:
                errorNewCard = True
                context = {'showtime': showtime,'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                    'tax': tax, 'total': total, 'accounts': accounts, 'errorNewCard': errorNewCard}
                return render(request, '../templates/checkout.html', context)
        if formName == 'promoForm':
            promoCode = request.POST.get('promo')
            card = 0
            order = {}
            order['accountID'] = 0
            if request.POST.get('card'):
                card = request.POST.get('card')
                account = Account.objects.get(accountID=card)
                order['accountID'] = account.accountID
            try:
                promo = Promotion.objects.get(promoCode=promoCode)
            except Promotion.DoesNotExist:
                errorPromo = True
                context = {'showtime': showtime, 'card':card,'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                           'tax': tax, 'total': total, 'accounts': accounts, 'errorPromo': errorPromo}
                return render(request, '../templates/checkout.html', context)
            total = round((total - promo.amount), 2)
            order['total'] = total
            order['numTickets'] = ticketCount
            cardApplied = True
            context = {'showtime': showtime, 'card':card,'movie': movie, 'tickets': tickets, 'seatprices': seatPrices,
                       'tax': tax, 'total': total, 'accounts': accounts, 'cardApplied': cardApplied,'order':order,'PromoAmount': promo.amount}
            return render(request, '../templates/checkout.html', context)
    return render(request, '../templates/checkout.html', context)

def orderconfirm(request):
    user = request.user
    shownum = request.GET.get('shownum')
    tickets = request.GET.get('tickets')
    order = request.GET.get('order')
    tickets = ast.literal_eval(tickets)
    order = ast.literal_eval(order)
    showtime = Showtime.objects.get(shownum=shownum)
    account = Account.objects.get(accountID = order['accountID'])
    movie = showtime.movieID
    order = Order(total=order['total'], numTickets=order['numTickets'], userID=user, shownum=showtime, accountID=account)
    order.save()
    for ticket in tickets:
        t = Ticket.objects.get(seatNum=ticket['seatNum'],shownum=showtime)
        t.price = ticket['price']
        t.user = user
        t.order = order
        t.save()
    
    name = user.first_name
    emailAddr = user.email
    template = render_to_string('../templates/email_template3.html',
                                {'name': name, 'showtime': showtime, 'movie': movie, 'tickets': tickets, 'order': order})
    email = EmailMessage(
        'Your order has been set',
        template,
        settings.EMAIL_HOST_USER,
        [emailAddr]
    )
    email.fail_silently = True
    email.send()
    context = {'showtime': showtime, 'movie': movie, 'tickets': tickets, 'order': order}
    return render(request, '../templates/confirmation.html', context)