from django.contrib.contenttypes.models import ContentType

# Assuming you have an instance of Metal or Crypto
metal_instance = Metal.objects.first()  # or Crypto.objects.first()

# Get the content type for Metal (or Crypto)
content_type = ContentType.objects.get_for_model(Metal)  # or Crypto

# Create a new transaction
transaction = Transaction.objects.create(
    user=user,
    content_type=content_type,
    object_id=metal_instance.id,  # or crypto_instance.id
    action='buy',
    quantity=10,
    price=Decimal('500'),
    status='completed'
)

