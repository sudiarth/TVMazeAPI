from db.data_layer import get_show, create_user, login_user, create_like, get_user_likes, delete_like

# for show in get_show('star'):
#     print(show.id)

# user = create_user('Sudi','sa@sudigital.com', 'password', 'password')
# print(user)

user = login_user('sa@sudigital.com', 'password')
print(user)

# print(create_like(1, 10))

# print(get_user_likes(1))

# print(delete_like(1))