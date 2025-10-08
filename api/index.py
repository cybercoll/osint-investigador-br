def handler(request):
    """
    Vercel Serverless Function Handler
    """
    import json
    
    # Resposta básica para qualquer requisição
    response_data = {
        "status": "success",
        "message": "OSINT Investigador BR - API Funcionando!",
        "version": "1.0.0",
        "method": request.method if hasattr(request, 'method') else "UNKNOWN",
        "path": request.path if hasattr(request, 'path') else "/"
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(response_data)
    }