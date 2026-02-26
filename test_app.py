import sys
sys.path.insert(0, 'C:/Users/LOQ/OneDrive/Desktop/flask')

from app1 import app

# Test the signup route
with app.test_client() as client:
    print("Testing GET /signup...")
    response = client.get('/signup')
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.data.decode('utf-8')[:500]}")
    else:
        print("✓ Signup page loads successfully")
    
    print("\nTesting POST /signup...")
    response = client.post('/signup', data={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'test123',
        'role': 'Student'
    }, follow_redirects=False)
    print(f"Status: {response.status_code}")
    print(f"Location: {response.location if response.status_code in [301, 302] else 'N/A'}")
    
    print("\nTesting GET /login...")
    response = client.get('/login')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Login page loads successfully")
