import re
# user_msg = 'sony 810 價格'
# searchObj = re.search(r'(.*) 價格', user_msg, re.M | re.I)
# print(searchObj.group(1))
# if searchObj:
# 	print("searchObj.group() : ", searchObj.group())
# 	print("searchObj.group() : ", searchObj.group(1))
# 	print(type(searchObj.group(1)))
# 	# print("searchObj.group(2) : ", searchObj.group(2))
# else:
# 	print("Nothing found!!")
# if searchObj == user_msg:
#


line = "Cats are smarter than dogs"
user_msg = 'sony 810 價格'
match_obj = re.match(r'(.*) 價格', user_msg, re.M | re.I)
a = match_obj.group()
if match_obj:
	print(match_obj.group())
else:
	print("No match!!")

if user_msg == a:
	print(match_obj.group())
# matchObj = re.search(r'dogs', line, re.M | re.I)
# if matchObj:
# 	print("search --> searchObj.group() : ", matchObj.group())
#
# else:
# 	print("No match!!")
