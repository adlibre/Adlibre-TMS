from django.db import models

from picklefield.fields import PickledObjectField


class XeroAuthCredentials(models.Model):
    consumer_key = models.CharField(max_length=30, help_text="XERO App OAuth Credentials Consumer Key")
    consumer_secret = models.CharField(max_length=30, help_text="XERO App OAuth Credentials Consumer Secret")

    pin_code = models.IntegerField(null=True, blank=True)
    access_token = models.CharField(
        help_text='XERO stored access token',
        max_length=30,
        editable=False,
        null=True,
        blank=True
    )   # calculated field

    def verify_pin_code(self):
        xero_credentials = XeroCredentials.objects.filter(secret=self.consumer_secret)
        if xero_credentials:
            for c in xero_credentials:
                creds = c.credentials
                token = creds.verify(unicode(self.pin_code))
                if token:
                    for cr in xero_credentials:
                        cr.delete()
                    return token
        else:
            raise KeyError('no credentials provided. Press get pin code and enter pin.')

    def save(self, *args, **kwargs):
        self.access_token = self.verify_pin_code()
        print self.access_token

        super(XeroAuthCredentials, self).save(*args, **kwargs)


class XeroCredentials(models.Model):
    """Internal place to store credentials object for future interaction."""
    secret = models.CharField(max_length=30, help_text="XERO App OAuth Credentials Consumer Secret")
    credentials = PickledObjectField()