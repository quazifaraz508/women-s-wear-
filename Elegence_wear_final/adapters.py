from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    
    def pre_social_login(self, request, sociallogin):
        # If the social account is already linked to a user, proceed
        if sociallogin.is_existing:
            return

        # --- THIS IS THE FIXED SECTION ---
        # Get the email address from the social account's extra data
        email = sociallogin.account.extra_data.get('email')

        # If an email address was returned, try to link it to an existing account
        if email:
            try:
                # Find a user with this email address
                User = get_user_model()
                user = User.objects.get(email__iexact=email)

                # If a user is found, connect the social account to this user
                sociallogin.connect(request, user)

            except User.DoesNotExist:
                # If no user is found, proceed with the normal signup flow
                pass
    
     # ---- Add this new method ----
    def authentication_error(self, request, provider_id, error, exception, extra_context):
        """
        Handles authentication errors.
        Instead of showing the default "Login Cancelled" page,
        we redirect the user back to the login page with a message.
        """
        # You could add more sophisticated logic here based on the 'error' code
        messages.error(request, "Login was cancelled or an error occurred.")
        return redirect(reverse('account_login')) # Or redirect to your main login page URL