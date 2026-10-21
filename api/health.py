from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    checks = {
        'database': False,
        'redis': False,
        'status': 'degraded',
    }

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT 1')
        checks['database'] = True
    except Exception:
        pass

    try:
        from django.core.cache import cache
        cache.set('health_test', 'ok', 1)
        result = cache.get('health_test')
        cache.delete('health_test')
        checks['redis'] = result == 'ok'
    except Exception:
        pass

    if checks['database'] and checks['redis']:
        checks['status'] = 'healthy'
    elif checks['database']:
        checks['status'] = 'degraded'

    return Response(checks, status=status.HTTP_200_OK if checks['database'] else status.HTTP_503_SERVICE_UNAVAILABLE)
