import requests
from studentdhms.models import StudentDHMSSignUp, StudentWalletTransactions
paystackSecretKey = 'sk_live_c7189e306761b8940a19ef83bdb28809c0209139'


def fetch_paystack_transactions(page=1):
    url = f"https://api.paystack.co/transaction?page={page}&perPage=100"
    headers = {
        "Authorization": f"Bearer {paystackSecretKey}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']  # List of transactions
    else:
        return None



def save_new_transactions(request):
    page = 1
    while True:
        transactions = fetch_paystack_transactions(page)
        if not transactions:
            break  # No more transactions to fetch
        
        new_transactions = []
        for transaction_data in transactions:
            transaction_id = transaction_data['id']
            # Check if the transaction already exists in the database
            if not StudentWalletTransactions.objects.filter(transactionID=transaction_id).exists():
                new_transaction = StudentWalletTransactions(
                    user = request.user,
                    transactionReference = transaction_data['reference'],
                    transactionDateFromPaystack = transaction_data['paid_at'],
                    # transactionCurrency = transaction_data['currency'],
                    transactionID = transaction_id,
                    transactionAmount = transaction_data['amount'] / 100,
                    transactionAuthCode = transaction_data['authorization']['authorization_code'],
                    transactionType = transaction_data['authorization']['card_type'],
                    # transactionBank = transaction_data['authorization']['bank'],
                    StudentEmail = transaction_data['customer']['email'],
                    # getRequestingID = StudentDHMSSignUp.objects.get(student_email = transaction_data['customer']['email']).id
                    # StudentID = StudentID,
                    transactionCustomerPhone = transaction_data['customer']['phone'],
                    transactionCustomerCode = transaction_data['customer']['customer_code'],
                    partnerAccountNumber = transaction_data['authorization']['bin']+transaction_data['authorization']['last4'],
                    partnerAccountName = transaction_data['authorization']['account_name'],
                    partnerAccountBank = transaction_data['authorization']['bank']

                )
                new_transactions.append(new_transaction)
        
        # Bulk save all new transactions to the database
        if new_transactions:
            StudentWalletTransactions.objects.bulk_create(new_transactions)
        
        page += 1  # Fetch the next page of transactions
