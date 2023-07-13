from .models import *

def fulfill_order(session):
    email = session['customer_details']['email']
    user_id = session['metadata']['user_id']
    product_id = session['metadata']['product_id']
    
    user = Users.objects.get(user_id=user_id)
    product = Products.objects.get(id=product_id)

    user.add_characters(product.num_characters)

    transaction = Transactions(
        user_id=user_id,  
        product_id=product_id, 
        amount_paid=session['amount_total'],  
    )
    transaction.save()

    email = session['customer_details']['email']

    #TODO
    return
