from utils.database_handler import get_database
from datetime import datetime

toot = get_database()
print(toot)
memos = toot.memo
print(memos)

memo = {"author": "Alanen", "text": "Cool new memo, bro!",
        "date": datetime.utcnow()}
try:
    memo_id = memos.insert_one(memo).inserted_id
    print(memo_id)
except Exception as e:
    print(e)
