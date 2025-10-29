import sys
import traceback

try:
    print("=== TEST CLOUDINARY ===", flush=True)
    
    # Test import
    import cloudinary
    import cloudinary.api
    print("✅ Modules importés", flush=True)
    
    # Configuration
    cloudinary.config(
        cloud_name="dkpf8ovsd",
        api_key="398734649392149", 
        api_secret="9AJGURM4X2oaDV01r3XIKt7pomI",
        secure=True
    )
    print("✅ Configuration OK", flush=True)
    
    # Test ping
    result = cloudinary.api.ping()
    print(f"✅ PING RÉUSSI: {result}", flush=True)
    
    # Écrire le résultat dans un fichier
    with open("cloudinary_test_result.txt", "w") as f:
        f.write("SUCCESS: Cloudinary fonctionne correctement\n")
        f.write(f"Ping result: {result}\n")
        
except Exception as e:
    error_msg = f"ERREUR: {str(e)}"
    print(f"❌ {error_msg}", flush=True)
    print(f"❌ Type: {type(e)}", flush=True)
    traceback.print_exc()
    
    # Écrire l'erreur dans un fichier
    with open("cloudinary_test_result.txt", "w") as f:
        f.write(f"ERROR: {error_msg}\n")
        f.write(f"Type: {type(e)}\n")
        f.write(f"Traceback: {traceback.format_exc()}\n")

print("=== FIN TEST ===", flush=True)
