from app import app,db,Admin,User

with app.app_context():
    db.drop_all()
    db.create_all()


    users = [
        {'firstname':'Jackson','lastname':'John','username': 'john', 'email': 'john@example.com', 'password': 'password123'},
        {'firstname':'Jackson','lastname':'John','username': 'jane', 'email': 'jane@example.com', 'password': 'password456'},
        {'firstname':'Jackson','lastname':'John','username': 'jake', 'email': 'jake@example.com', 'password': 'password789'},
        {'firstname':'Jackson','lastname':'John','username': 'jill', 'email': 'jill@example.com', 'password': 'password4842'}
    ]
    for user_data in users:
        user = User(firstname = user_data['firstname'],lastname=user_data['lastname'],username=user_data['username'], email=user_data['email'])
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        print("Users Added Successfully!!")

    
    admins = [
        {'firstname':'Jackson','lastname':'John','username': 'john', 'email': 'john@example.com', 'password': 'password123'},
        {'firstname':'Jackson','lastname':'John','username': 'jane', 'email': 'jane@example.com', 'password': 'password456'},
        {'firstname':'Jackson','lastname':'John','username': 'jake', 'email': 'jake@example.com', 'password': 'password789'},
        {'firstname':'Jackson','lastname':'John','username': 'jill', 'email': 'jill@example.com', 'password': 'password4842'}
    ]
    for admin_data in admins:
         admin = Admin(firstname = admin_data['firstname'],lastname=admin_data['lastname'],username=admin_data['username'], email=admin_data['email'])
         admin.set_password(admin_data['password'])
         db.session.add(admin)
         db.session.commit()
         print("Admin added Successfully!!")
