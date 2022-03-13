import sys
import random
from notion_client import Client
from settings import Settings

notion_tkn = Settings().NOTION_TOKEN
gspread_id = Settings().WEBHOOK_ID
gspread_tkn = Settings().WEBHOOK_TOKEN

notion = Client(auth=notion_tkn)

from pprint import pprint

list_users_response = notion.users.list()
pprint(list_users_response)

NOTION_DATABASE_NAME = "Test Notion SDK for Python Database"

print(f"Searching database '{NOTION_DATABASE_NAME}' ...", end="", flush=True)

search_database = notion.search(**{
    'query': NOTION_DATABASE_NAME,
})

if len(search_database['results']) == 0:
    print(" not found!")
    sys.exit()

print(" found!")

my_database_id = search_database['results'][0]['id']

# this is a bit useless since we already have the database id
my_database = notion.databases.retrieve(database_id=my_database_id)

# this will create 3 pages
for page_id in range(1, 4):
    rand_page_type = random.choice(['Animal', 'Vegetal'])

    # set how other properties types here:
    # https://developers.notion.com/reference/database#database-property
    new_page_props = {
        'Name': {'title': [{'text': {'content': f"My Page of {rand_page_type} {page_id}"}}]},
        'Value': {'number': page_id},
        'Link': {'type': 'url', 'url': f"http://examples.org/page/{page_id}"},
        'Tags': {'type': 'multi_select', 'multi_select': [{'name': rand_page_type}]}
    }

    notion_page = notion.pages.create(
        parent={'database_id': my_database['id']},
        properties=new_page_props
    )

    if notion_page['object'] == 'error':
        print("ERROR", notion_page['message'])
        continue

    print(f"Page for {rand_page_type} {page_id} created with id {notion_page['id']}")