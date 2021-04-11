from utils.database_handler import connect_database
from datetime import datetime
from entities.memo import Memo
from bson.objectid import ObjectId
from mongoengine import connect
from utils.config import database_uri
from repositories.MemoRepository import MemoRepository
from services.memo_service import MemoService
from utils.helpers import get_test_memo


memorepo = MemoRepository(prod=False)
memoservice = MemoService()

new_memo = get_test_memo()
#saved_memo = memorepo.new(new_memo)
amount = memorepo.count_m('all')
#amount_2 = memoservice.count('all')

memos = memorepo.get_m('all')
print('>', memos)
for memo in memos:
    print(memo.title, '-', memo.date)

#print('get-memo-test:', memorepo.get('id', saved_memo.id).title)


# try:
#     memo_id = memos.insert_one(memo.format()).inserted_id
#     print(memo_id)
# except Exception as e:
#     print(e)
