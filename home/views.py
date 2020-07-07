from django.shortcuts import render


from firebase import Firebase
import os
import requests
import json
from requests.auth import HTTPBasicAuth
import datetime
from django.http import HttpResponse, JsonResponse
from .card_retrieval import fetch_card_design_names


# Create your views here.

config = {}

firebase = Firebase(config)
auth = firebase.auth()
db = firebase.database()

groupUser = 'userGivenDuringHackathon'
groupPass = 'passwordGivenDuringHackathon'



def index(request):
    if "username" in request.session:
        mambuAcc = db.child("Users").child(request.session.get("username")).child("mambuID").get().val()
        buy = ""
        
        if request.method == "POST":
            deductSend = {
                "type": "TRANSFER",
                "amount": "",
                "notes": "",
                "toSavingsAccount": "",
                "method":"bank"
            }
            if request.POST.get("blizzard_5"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "5"
                deductSend["notes"] = "Transfer to Blizzard"
                buy = "Bought $5 Credits for Blizzard!"

            elif request.POST.get("blizzard_50"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "50"
                deductSend["notes"] = "Transfer to Blizzard"
                buy = "Bought $50 Credits for Blizzard!"

            elif request.POST.get("steam_5"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "5"
                deductSend["notes"] = "Transfer to Steam"
                buy = "Bought $5 Credits for Steam!"

            elif request.POST.get("steam_50"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "50"
                deductSend["notes"] = "Transfer to Steam"
                buy = "Bought $50 Credits for Steam!"

            elif request.POST.get("pubg_5"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "5"
                deductSend["notes"] = "Transfer to PUBG"
                buy = "Bought $5 Credits for PUBG!"

            elif request.POST.get("pubg_50"):
                deductSend["toSavingsAccount"] = ""
                deductSend["amount"] = "50"
                deductSend["notes"] = "Transfer to PUBG"
                buy = "Bought $50 Credits for PUBG!"
            
            transferMoney = requests.post(f"https://razerhackathon.sandbox.mambu.com/api/savings/{mambuAcc}/transactions",auth=HTTPBasicAuth(groupUser, groupPass),json=deductSend)
        
        #get the account number from firebase
        uName = db.child("Users").child(request.session.get("username")).child("FirstName").get().val() + " " + db.child("Users").child(request.session.get("username")).child("LastName").get().val()
        #connect to mambu to get all transaction
        uTransactions = requests.get(f"https://razerhackathon.sandbox.mambu.com/api/savings/{mambuAcc}/transactions",auth=HTTPBasicAuth(groupUser, groupPass))
        uTransactions = uTransactions.json()
        #populate with account information 
        monthlyTransactions = []
        tempMonthlyTransactions = {}
        today = datetime.date.today()
        today = today.strftime("%Y-%m")
        #populate monthlyTransactions list
        for j in range(11,-1,-1):
            if int(today.split("-")[1]) - j <= 0:
                transMonth = int(today.split("-")[1]) - j + 12
                transYear = int(today.split("-")[0]) - 1 
            else:
                transMonth = int(today.split("-")[1]) - j
                transYear = int(today.split("-")[0])
            monthlyString = str(transYear) + "-" + str(transMonth)
            monthlyTransactions.append([monthlyString])
        for i in uTransactions:
            entryDate = i["entryDate"].split("T")[0]
            entryDate = entryDate[:7]
            entryDate = datetime.datetime.strptime(entryDate, "%Y-%m")
            entryDate = entryDate.strftime("%Y-%m")
            num_months = (int(today.split("-")[0]) - int(entryDate.split("-")[0])) * 12 + (int(today.split("-")[1]) - int(entryDate.split("-")[1]))
            entryDate1 = int(entryDate.split("-")[0])
            entryDate2 = int(entryDate.split("-")[1])
            entryDate = str(entryDate1) + "-" + str(entryDate2)
            if num_months < 12:
                # WAS GOING TO CALCULATE THE INDIVIDUAL AMOUNTS SPENT THEN ADD AND SUBTRACT, GOOD FOR GRANULARITY BUT NOT NECESSARY FOR DATA TO DISPLAY
                # if entryDate.year+"-"+entryDate.month in tempMonthlyTransactions:
                #     if i["type"] == "DEPOSIT":
                #         tempMonthlyTransactions[entryDate.year+"-"+entryDate.month] = tempMonthlyTransactions[entryDate.year+"-"+entryDate.month] + i[""]
                if entryDate in tempMonthlyTransactions:
                    if i["entryDate"] > tempMonthlyTransactions[entryDate]['timestamp']:
                        tempMonthlyTransactions[entryDate]['timestamp'] = i["entryDate"]
                        tempMonthlyTransactions[entryDate]['balance'] = i["balance"]
                else:
                    tempMonthlyTransactions[entryDate] = {"timestamp":i["entryDate"],"balance":i["balance"]}
        lastMonthlyBalance = 0
        print(tempMonthlyTransactions,"monthly")
        for k in monthlyTransactions:
            if k[0] not in tempMonthlyTransactions:
                k.append(lastMonthlyBalance)
            else:
                k.append(tempMonthlyTransactions[k[0]]["balance"])
                lastMonthlyBalance = tempMonthlyTransactions[k[0]]["balance"]

        context = {"digitalWallet":monthlyTransactions,"uName":uName,"lastMonthlyBalance":lastMonthlyBalance,"bought":buy}
            
    else:
        context = {"digitalWallet":[0,0,0,0,0,0,0,0,0,0,0,0,0],"uName":"Please Log In","bought":buy}
    return render(request,'home/index.html',context=context)

def login(request):
    request.session["username"] = ""
    if request.method == "POST":
        #check if the credentials are correct, if not direct back to login form and ask to key in again
        if request.POST.get('username') in db.child("Users").get().val() and request.POST.get('password') in db.child("Users").child(request.POST.get('username')).child("pass").get().val():
            page = 'home/index.html'
            request.session["username"] = request.POST.get('username')
            context={"session": request.session["username"]}
            return index(request)
        else:
            page = 'home/login.html'
            context = {'err_msg':'Incorrect account.'}
    else:
        page = 'home/login.html'

        context = {'err_msg':''}
    return render(request,page,context=context)


def register(request):
    if request.method == "POST":
        #check if the database has any same username, if not then send in the data 

        if request.POST.get('username') in db.child("Users").get().val():
            page = 'home/register.html'
            context = {'err_msg':'Username taken!'}
        else:
            branchinfo = requests.get("https://razerhackathon.sandbox.mambu.com/api/branches/Team4",auth=HTTPBasicAuth(groupUser, groupPass))
            branchinfo = branchinfo.json()
            guid = len(db.child("Users").get().val())
            toSend = {
                "client": {
                    "firstName": request.POST.get('firstName'),
                    "lastName": request.POST.get('lastName'),
                    "preferredLanguage": "ENGLISH",
                    "notes": "testest",
                    "assignedBranchKey": ""
                },
                "idDocuments": [
                    {
                        "identificationDocumentTemplateKey": "",
                        "issuingAuthority": "Immigration Authority of Singapore",
                        "documentType": "NRIC/Passport Number",
                        "validUntil": request.POST.get('validUntil'),
                        "documentId": request.POST.get('nricPassport')
                    }
                ],
                "addresses": [],
                "customInformation": [
                    {
                        "value":request.POST.get('birthCountry'),
                        "customFieldID":"countryOfBirth"
                        
                    },
                    {
                        "value": guid + 4,
                        "customFieldID":"razerID"
                        
                    }
                    ]
            }
            mambuDataCreateClient = requests.post("https://razerhackathon.sandbox.mambu.com/api/clients",auth=HTTPBasicAuth(groupUser, groupPass),json=toSend)
            mambuDataCreateClient = mambuDataCreateClient.json()
            toSendAccount = {
                "savingsAccount": {
                    "name": "Digital Account",
                    "accountHolderType": "CLIENT",
                    "accountHolderKey": mambuDataCreateClient['client']['encodedKey'],
                    "accountState": "APPROVED",
                    "productTypeKey": "",
                    "accountType": "CURRENT_ACCOUNT",
                    "currencyCode": "SGD",
                    "allowOverdraft": "true",
                    "overdraftLimit": "100",
                    "overdraftInterestSettings": {
                        "interestRate": 5
                    },
                        "interestSettings": {
                    "interestRate": "1.25"
                }
                }

            }
            mambuDataCreateAccount = requests.post("https://razerhackathon.sandbox.mambu.com/api/savings",json=toSendAccount,auth=HTTPBasicAuth(groupUser, groupPass))
            mambuDataCreateAccount = mambuDataCreateAccount.json()
            fireDbInfo = {"pass":request.POST.get('password'),"DOB":request.POST.get('dob'),"mambuID":mambuDataCreateAccount["savingsAccount"]["id"],"FirstName":request.POST.get('firstName'),"LastName":request.POST.get('lastName')}
            db.child("Users").child(request.POST.get('username')).set(fireDbInfo)
            page = 'home/index.html'
            context = {}
            request.session["username"] = request.POST.get('username')
            return index(request)
    else:
        context = {'err_msg':''}
        page = 'home/register.html'
        return render(request,page,context=context)

def buttons(request):
    return render(request, 'home/buttons.html')

def get_cards(request):
    print(request.GET)
    game = request.GET.get("game")
    print("request was ", game)
    return JsonResponse(fetch_card_design_names(game))

notfound_image = "img/notfound.png"

def get_image_resource(request):
    image_path = "img/" + request.GET.get("design") + ".jpg"
    try:
        with open(image_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpg")
    except IOError as e:
        with open(notfound_image, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpg")

def cards(request):
    return render(request,'home/cards.html')
