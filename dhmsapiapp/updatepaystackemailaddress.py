import requests
paystackSecretKey = 'sk_live_c7189e306761b8940a19ef83bdb28809c0209139'
 
def update_customer_email(customer_code, new_email):
    url = f"https://api.paystack.co/customer/{customer_code}"
    headers = {
        "Authorization": f"Bearer {paystackSecretKey}",
        "Content-Type": "application/json"
    }
    data = {
        "email": new_email
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        payStackEmailUpdated = True
        return response.json()
    else:
        payStackEmailUpdated = False
        return response.json()  # Handle any errors or unsuccessful responses



