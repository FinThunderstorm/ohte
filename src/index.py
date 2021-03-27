from utils.database_handler import get_database
from datetime import datetime
from entities.memo import Memo
from bson.objectid import ObjectId

toot = get_database()
print(toot)
memos = toot.memo
print(memos)

memo = Memo("6ebeb3f8-1876-4119-b4fc-0ca1222602b6",
            "", "Testing new cool memo, bro")
print('>', ObjectId())


try:
    memo_id = memos.insert_one(memo.format()).inserted_id
    print(memo_id)
except Exception as e:
    print(e)
