# Add these to your existing settings.py file

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider's SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'f.bencharef@esi-sba.dz'
EMAIL_HOST_PASSWORD = 'amgp jrjh cmza dchq'  # Use an app password for security
EMERGENCY_CONTACT_EMAIL = 'f.bencharef@esi-sba.dz'
DEFAULT_FROM_EMAIL = 'f.bencharef@esi-sba.dz'