# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Appointment

# @receiver(post_save, sender=Appointment)
# def send_appointment_confirmation(sender, instance, created, **kwargs):
#     if not created:
#         return
    
    
#     customer_email = instance.customer.user.email
#     customer_name = instance.customer.user.username
#     stylist_name = instance.stylist.user.username
#     service_name = instance.service.name
#     due_date = instance.due_date
    
#     try:
        
         
#         send_mail(
#             subject=f'Appointment Confirmation - {service_name}',
            
#             message=f'''
#             Hi {customer_name},
            
#             Your appointment has been confirmed.
            
#             Details: 
#                 Service : {service_name}
#                 Stylist : {stylist_name}
#                 due_date : {due_date}
#                 Status : Pending
                
#             We look forward to seeing you,
            
#             Salon Team.    
#             ''',
            
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[customer_email],
#             fail_silently=False,
        
    
            
            
#         )
#     except Exception as e: 
#         print('Email failed', e)   
    