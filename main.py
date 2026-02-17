# api/ban.py
import requests
import base64
import json
import time
import os
from flask import Flask, request, jsonify

# Base64 encoded body (decoded later) - same as in main.py
BODY_BASE64 = 'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'

# Flask app for Vercel
app = Flask(__name__)

def decode_jwt(token):
    """Decode JWT token to extract user information"""
    try:
        payload_part = token.split('.')[1]
        payload_part += '=' * (-len(payload_part) % 4)
        decoded_bytes = base64.b64decode(payload_part)
        decoded_str = decoded_bytes.decode('utf-8')
        data = json.loads(decoded_str)
        return data
    except Exception as e:
        return {}

def process_ban(access_token):
    """Core ban logic from main.py adapted for API response"""
    try:
        # API URL from main.py
        API_URL_1 = 'https://api.freefireservice.dnc.su/oauth/account:login?data={}'
        API_URL_2 = 'https://client.ind.freefiremobile.com/GetLoginData'
        
        # Step 1: Validate token with first API
        try:
            response = requests.get(API_URL_1.format(access_token), timeout=20)
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"Connection Failed! Status: {response.status_code}"
                }
            
            resp_json = response.json()
            
            # Check for error in response (field '8' indicates error in main.py logic)
            if '8' in resp_json:
                return {
                    "success": False,
                    "message": "Invalid Token or Expired!"
                }
            
            jwt_token = resp_json['8']
            user_data = decode_jwt(jwt_token)
            
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Internet Error! Check your connection."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Token validation failed: {str(e)}"
            }
        
        # Extract user info for response
        nickname = user_data.get('nickname', 'Unknown')
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', 'Latest')
        
        # Step 2: Send ban request
        try:
            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'X-Unity-Version': '2018.4.11f1',
                'X-GA': 'v1 1',
                'ReleaseVersion': version,
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
                'Accept-Encoding': 'gzip'
            }
            
            body = base64.b64decode(BODY_BASE64)
            ban_resp = requests.post(API_URL_2, headers=headers, data=body, timeout=20)
            
            if ban_resp.status_code == 200:
                return {
                    "success": True,
                    "message": "Ban Successfully 🗿 Ban by Kevin",
                    "data": {
                        "name": nickname,
                        "uid": account_id,
                        "region": region,
                        "patch": version,
                        "status": "SUSPENDED (100%)",
                        "method": "Kevin V9 Private API"
                    }
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to Ban! Server returned: {ban_resp.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Ban request failed: {str(e)}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }

@app.route('/')
def home():
    return jsonify({
        "message": "Kevin Ban V9 API",
        "endpoints": {
            "ban": "/ban?access_token={token}"
        },
        "note": "Returns response in JSON format"
    })

@app.route('/ban', methods=['GET'])
def ban_endpoint():
    access_token = request.args.get('access_token', '')
    
    if not access_token:
        return jsonify({
            "success": False,
            "message": "access_token parameter is required"
        })
    
    result = process_ban(access_token)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "API is running"})

# For Vercel serverless function
def handler(request):
    return app(request)

# For local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)