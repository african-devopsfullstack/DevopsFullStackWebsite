import httpx as r
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "Host": 'data.usajobs.gov',
    "User-Agent": 'idrisniyi94@gmail.com',
    "Authorization-Key": os.getenv("USAJOB_API")
}

response = r.get("https://data.usajobs.gov/api/search?Keyword=Software%20Developer&LocationName=Washington%2C%20District%20of%20Columbia", headers=headers)

print(response.json())