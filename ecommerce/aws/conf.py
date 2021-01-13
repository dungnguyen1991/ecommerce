import datetime

AWS_GROUP_NAME = "eCommerce_group"
AWS_USERNAME = "ecommerce-user"
AWS_ACCESS_KEY_ID = "AKIAR2XFA5JMIYJHNCVC"
AWS_SECRET_ACCESS_KEY = "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"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True

DEFAULT_FILE_STORAGE = 'ecommerce.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'ecommerce.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'dung-ecommerce'
AWS_S3_REGION_NAME = 'us-east-2'
S3_URL = '//{}.s3.{}.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
MEDIA_URL = '//{}.s3.{}.amazonaws.com/media/'.format(AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = { 
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}

# S3DIRECT_REGION =  'us-east-2' 

PROTECTED_DIR_NAME = 'protected'
PROTECTED_MEDIA_URL = '//%s.s3.amazonaws.com/%s/' %( AWS_STORAGE_BUCKET_NAME, PROTECTED_DIR_NAME)

AWS_DOWNLOAD_EXPIRE = 5000 #(0ptional, in milliseconds)