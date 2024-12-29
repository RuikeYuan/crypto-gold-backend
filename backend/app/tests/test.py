from django.contrib.auth.models import User

# Try to get the user by username
user = User.objects.get(username="testuser")

# Check if the password is correct
print(user.check_password("testpassword123"))
