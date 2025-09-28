import json

from DTOs.UserAuthResponse import UserAuthResponse

new_user = UserAuthResponse(status=0,message='not propperly defined',user_id=0)

print('porperty',new_user.message)
print('from method',new_user.to_dict())

stringified = json.dumps(new_user.to_dict())
print('stringified and typeof',stringified, type(stringified))

obejctpy = json.loads(stringified)
print('Pythonobject and property', obejctpy,type(obejctpy), obejctpy["message"])