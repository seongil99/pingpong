from rest_framework.decorators import api_view
from .decorators import spa_login_required

@api_view(['GET'])
@spa_login_required
def spa_login_required_test(request):
    return "hello world"

