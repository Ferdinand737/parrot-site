from .models import *

def fulfill_order(session):
    email = session['customer_details']['email']
    user_id = session['metadata']['user_id']
    product_id = session['metadata']['product_id']
    
    user = Users.objects.get(user_id=user_id)
    product = ReloadOptions.objects.get(id=product_id)
    reload_credits(user, product)
    update_transactions_table(session)
    send_email(email, product, user)
    return

def reload_credits(user, product):
    user.add_characters(product.num_characters)
    return

def update_transactions_table(session):
    #TODO
    return

def send_email(email, product, user):
    #TODO
    return