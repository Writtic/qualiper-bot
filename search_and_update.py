import sys
import random
from notion_client import Client
from settings import Settings

notion_tkn = Settings().NOTION_TOKEN
gspread_id = Settings().WEBHOOK_ID
gspread_tkn = Settings().WEBHOOK_TOKEN

notion = Client(auth=notion_tkn)

NOTION_DATABASE_NAME = "학습노트"

print(f"Searching database '{NOTION_DATABASE_NAME}' ...", end="", flush=True)

search_database = notion.search(
    **{
        "query": NOTION_DATABASE_NAME,
    }
)

if len(search_database["results"]) == 0:
    print(" not found!")
    sys.exit()

print(" found!")

my_database_id = search_database["results"][0]["id"]

park = "d79db92f-d114-4f6f-937c-83cc10c66d7a"
data = notion.databases.query(
    database_id=my_database_id,
    **{"filter": {"and": [{"property": "담당자", "people": {"contains": park}}]}},
)
results = data.get("results", [])
com_cnt = 0
che_cnt = 0
for res in results:
    prop = res.get("properties", {})
    coms = prop["칭찬카드"]["multi_select"]
    for com in coms:
        print(com["name"])
        if "칭찬" in com["name"]:
            com_cnt += 1
        if "격려" in com["name"]:
            che_cnt += 1

print("칭찬 카드 갯수:", com_cnt)
print("격려 카드 갯수:", che_cnt)

search_database = notion.search(
    **{
        "query": "칭찬카드",
    }
)
my_database_id = search_database["results"][0]["id"]

data = notion.databases.query(
    database_id=my_database_id,
    **{"filter": {"and": [{"property": "대상", "people": {"contains": park}}]}},
)
_id = data["results"][0]["id"]

notion.pages.update(page_id=_id, **{
    "properties": {
        "칭찬수": {
            "number": com_cnt
        },
        "격려수": {
            "number": che_cnt
        }
    }
})


# my_database = notion.databases.retrieve(database_id=my_database_id)
# print(my_database)