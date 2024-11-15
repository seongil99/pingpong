from common.decorators import spa_login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
@spa_login_required
def spaLoginRequiredView(request):
    return Response({'message': 'Success'}, status = 200)

