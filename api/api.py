from ninja import NinjaAPI
from .auth import AuthBearer

api = NinjaAPI(
    title="Zest Store API",
    version="1.0.0",
    description="API for Zest Store e-commerce platform",
    auth=AuthBearer(),
)

@api.get("/hello", auth=None)
def hello(request):
    return {"message": "Welcome to Zest Store API!"}

@api.get("/protected")
def protected(request):
    return {"message": "This is a protected endpoint"} 