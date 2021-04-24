import replit
for key in replit.db.keys():
	del replit.db[key]