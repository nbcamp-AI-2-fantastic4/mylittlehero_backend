from pymongo import MongoClient

client = MongoClient('mongodb://test:test@15.165.161.237', 27017)
db = client.dbmylittlehero

# result db 전체 리스트 가져오기
all_results = list(db.results.find({},{'_id':False}))

# all_list 라는 빈 리스트값을 지정
all_list = []
# all_results에서 for 문으로 반복 할때 필요한 정보만 가져오기
for result in all_results:
    element = {
        'user_img': result['user_img'],
        'acc': result['accuracy'],
        'name': result['hero']
    }
    # hero_info db값을 가져오기 이때 element 리스트에 hero_info 원하는 값을 넣어주기
    hero_info = db.heros.find_one({'hero': element['name']}, {'_id': False})
    element['hero_img'] = hero_info['hero_img']
    element['description'] = hero_info['description']
    all_list.append(element)

for i in all_list:
    print(i)


