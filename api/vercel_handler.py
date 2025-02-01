from core.wsgi import application

# Handler for Vercel
def handler(request, **kwargs):
    return application(request, **kwargs) 