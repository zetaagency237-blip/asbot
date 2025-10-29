print("Test basique...")

try:
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    
    print(f"Token trouvé: {token is not None}")
    if token:
        print(f"Token début: {token[:20]}...")
    
    print("Test réussi!")
    
except Exception as e:
    print(f"Erreur: {e}")
