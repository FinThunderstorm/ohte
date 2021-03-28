from utils.database_handler import connect_database
from datetime import datetime
from entities.memo import Memo
from bson.objectid import ObjectId
from mongoengine import connect
from utils.config import database_uri
from repositories.MemoRepository import MemoRepository
from utils.helpers import get_test_memo
# toot = get_database()
# print(toot)
# memos = toot.memo
# print(memos)


print(get_test_memo()["title"], get_test_memo()["author_id"])

memorepo = MemoRepository(prod=False)

new_memo = get_test_memo()
saved_memo = memorepo.new_memo(new_memo)

memos = memorepo.get_all_memos()
print('>', memos)
for memo in memos:
    print(memo.title, '-', memo.date)

memorepo.count_memos()
print('get-memo-test:', memorepo.get_memo(saved_memo.id).title)


# try:
#     memo_id = memos.insert_one(memo.format()).inserted_id
#     print(memo_id)
# except Exception as e:
#     print(e)
