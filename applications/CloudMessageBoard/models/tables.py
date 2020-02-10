# -*- coding: utf-8 -*-
db.define_table('MESSAGE_BOARD',
                Field('sender', 'text'),
                Field('receiver', 'text'),
                Field('message_content', 'text'),
                # Field('sent_time', 'datetime', requires=IS_DATE(format='%d-%m-%Y %H:%M:%S')),
                Field('sent_time', 'datetime'),
                Field('has_read', 'boolean', default=False),
                Field('comments', 'text'),
                redefine=True)
