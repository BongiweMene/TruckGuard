import requests

print("================================")
print("      OSIRIS CONNECTION TEST")
print("================================")

url = "https://www.osirisai.live/api/weather"

print("\nTesting:")
print(url)

try:
    response = requests.get(url, timeout=15)

    print("\nSTATUS CODE:", response.status_code)

    print("\nRESPONSE:")
    print(response.text)

except Exception as e:
    print("\nERROR:")
    print(e)

print("\n================================")
print("          TEST COMPLETE")
print("================================")