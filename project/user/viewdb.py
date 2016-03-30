for user in query_db('select * from users'):
    print user['username'], 'has the id', user['user_id']
