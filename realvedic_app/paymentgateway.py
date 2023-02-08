import json

import environ
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response

from realvedic_app.models import PaymentOrder
from realvedic_app.serializers import OrderSerializer

env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


@api_view(['POST'])
def start_payment(request):
    amount = request.data['amount']
    name = request.data['name']

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))
   
    #cart_to_order_shift(token)

    payment = client.order.create({"amount": eval(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    order = PaymentOrder.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data,
      
    }
    return Response(data)




@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    # print(type(request.data["response"]))
    res = eval(request.data["response"])


    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id =""
    raz_pay_id = ""
    raz_signature = ""
    amount=request.data['amount']
    token=request.data['token']
    
    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]
        elif key == res['amount']:
            amount = res[key]

       
    # get order by payment_id which we've created earlier with isPaid=False
    order = PaymentOrder.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=('rzp_test_gHJS0k5aSWUMQc', '8hPVwKRnj4DZ7SB1wyW1miaf'))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if not check:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()
    #cart_to_order_shift(token,amount,ord_id)

    res_data = {
        'message': 'payment successfully received!'
    }
 
  

    return Response(res_data)
