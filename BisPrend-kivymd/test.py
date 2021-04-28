from user import User

userInst = User()

userInst.createUserFile("John Doe")

print(userInst.getName())
print(userInst.getProgress())
print(userInst.hasUser())

userInst.registername("Mark")
userInst.updateuserprogress(5)

userInst2 = User()

print(userInst.getName())
print(userInst.getProgress())
print(userInst.hasUser())