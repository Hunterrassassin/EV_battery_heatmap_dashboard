import base64

with open("token.json", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

with open("token_b64.txt", "w") as f:
    f.write(encoded)

print("✅ token.json has been encoded and saved to token_b64.txt")
