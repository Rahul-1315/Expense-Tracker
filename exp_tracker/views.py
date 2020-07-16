from django.shortcuts import render, redirect
from exp_tracker.models import User, Transcation, Wallet
from django.shortcuts import HttpResponse
import random

# Login with credentials if existing user


def login(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        password = request.POST['password']
        try:
            cred = User.objects.get(pk=user_id)
            if user_id == cred.user_id and password == cred.password:
                return redirect(f'expense/{user_id}')
            else:
                return HttpResponse("Wrong cred")
        except:
            return HttpResponse("Wrong cred")

    return render(request, "login.html")


# Signup if new user


def signup(request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        user_id = request.POST['user_id']
        password = request.POST['password']
        try:
            cred = User.objects.get(pk=user_id)
            return redirect("/signup/")
            # new_user = user.objects.create(user_id=user_id,user_name=user_name,password=password)
            # return render(request, "entry.html")
        except:
            # return HttpResponse("")
            new_user = User.objects.create(
                user_id=user_id, name=user_name, password=password)
            return redirect('/create_wallet/')
    return render(request, "signup.html")


# After signup user will have to create wallet for his account
def create_wallet(request):
    # Random module is implemented so that a unique wallet-ID can be generated
    rand = random.randint(100000, 3000000)
    if request.method == "POST":
        user_id = request.POST['user_id']
        user = User.objects.get(pk=user_id)
        uid = user.user_id
        wallet_id = request.POST['wallet_id']
        balance = request.POST['balance']
        try:
            walletID = Wallet.objects.get(pk=wallet_id)
            return redirect('/create_wallet/')
        except:
            new_wallet = Wallet(
                user_id=user, wallet_id=wallet_id, balance=balance)
            new_wallet.save()
            return redirect(f'/expense/{uid}')
    return render(request, "createWallet.html", {'random_no': rand})

# user can add his/her expenses into the database


def expense(request, user_id):
    wallet_object = Wallet.objects.filter(user_id=user_id)
    w_id = wallet_object[0]
    balance = float(0)
    for i in wallet_object:
        balance = i.balance
    print(w_id)
    user_object = User.objects.get(pk=user_id)
    uid = user_object.user_id
    print(user_object)
    try:
        transact_object = Transcation.objects.filter(user_id=uid)
        if request.method == "POST":
            amount = request.POST['amount']
            transaction_type = request.POST['transaction_type']
            print(transaction_type)
            transaction_details = request.POST['transaction_details']
            transaction_time = request.POST['transaction_time']

            if transaction_type == "Debit":
                print('debit')
                if balance < 0:
                    balance = 0
                else:
                    balance -= float(amount)
            else:
                print('credit')
                balance += float(amount)
            print(balance)
            new_balance = Wallet(user_id=user_object,
                                 wallet_id=w_id, balance=balance)
            new_balance.save()
            new_transaction = Transcation(user_id=user_object, wallet_id=w_id, amount=amount, transaction_type=transaction_type,
                                          transaction_details=transaction_details, transaction_time=transaction_time)
            new_transaction.save()
            return redirect(f'/expense/{uid}')
        return render(request, 'expense.html', {'balance': balance, 'wallet_object': w_id, 'user_object': user_object, 'transact_object': transact_object})

    except:
        if request.method == "POST":
            amount = request.POST['amount']
            transaction_type = request.POST['transaction_type']
            print(transaction_type)
            transaction_details = request.POST['transaction_details']
            transaction_time = request.POST['transaction_time']
            balance = balance-float(amount)
            if transaction_type == "Debit":
                if balance < 0:
                    print('debit')
                    balance = 0
                else:
                    balance = balance

            else:
                print('credit')
                balance += float(amount)
            print(balance)
            new_balance = Wallet(user_id=user_object,
                                 wallet_id=w_id, balance=balance)
            new_balance.save()
            new_transaction = Transcation(user_id=user_object, wallet_id=w_id, amount=amount, transaction_type=transaction_type,
                                          transaction_details=transaction_details, transaction_time=transaction_time)
            new_transaction.save()
            return HttpResponse('helli')
        return render(request, 'expense.html', {'balance': balance, 'wallet_object': w_id, 'user_object': user_object})
