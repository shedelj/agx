from datetime import datetime

def get_name():
	name = request.client
	if auth.user:
		name = auth.user.first_name + auth.user.last_name
	return name

db.define_table('dev',
	Field('film'),
	Field('developer'),
	Field('dilution'),
	Field('iso', 'integer'),
	Field('time_35', 'decimal(4,2)'),  # Time in seconds
	Field('time_120', 'decimal(4,2)'), # Time in seconds
	Field('temperature'),
	Field('date_posted', 'datetime'),
	Field('notes', 'text'),
	Field('author_id', db.auth_user),
	)

db.dev.id.readable = False
db.dev.author_id.default = auth.user_id
db.dev.author_id.writable = db.dev.author_id.readable = False
db.dev.date_posted.default = datetime.utcnow()
db.dev.date_posted.writable = False
