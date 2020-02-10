# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    # response.flash = T("Hello World")
    # return dict(message=T('Welcome to web2py!'))
    return redirect("cloud_message_board")


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status': 'success', 'email': auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership('admin')  # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html'  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def cloud_message_board():
    # response.view = 'generic.' + request.extension
    response.title = "Cloud Message Board"
    if request.method == 'GET':
        # print("GET Method")
        return dict()
    elif request.method == 'POST':
        # print("POST Method")

        import time
        time.strftime("%Y-%m-%d %H:%M:%S")
        db.MESSAGE_BOARD.insert(
            sender=request.vars['sender'],
            receiver=request.vars['receiver'],
            message_content=request.vars['msg'],
            sent_time=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        return redirect('after_post_message')
    else:
        raise HTTP(403)


def after_post_message():
    response.view = "default/cloud_message_board.html"
    response.title = "Cloud Message Board"
    return dict()


@request.restful()
def api():
    response.view = 'generic.json'

    def GET(*args, **vars):
        sender = vars.get('sender', None)
        receiver = vars.get('receiver', None)
        has_read = vars.get('has_read', None)

        # result = db.executesql("SELECT * FROM MESSAGE_BOARD", as_dict=True)
        # print(result)
        # query = db.MESSAGE_BOARD.id > 0
        query = True
        if sender:
            query &= (db.MESSAGE_BOARD.sender == sender)
        if receiver:
            query &= (db.MESSAGE_BOARD.receiver == receiver)
        if has_read:
            query &= (db.MESSAGE_BOARD.has_read == has_read)

        rows = db(query).select(db.MESSAGE_BOARD.id,
                                db.MESSAGE_BOARD.message_content,
                                db.MESSAGE_BOARD.sender,
                                db.MESSAGE_BOARD.receiver,
                                db.MESSAGE_BOARD.has_read,
                                db.MESSAGE_BOARD.sent_time)

        return dict(records=rows)

    def POST(*args, **vars):
        import timeit
        sender = vars.get('sender', None)
        receiver = vars.get('receiver', None)
        has_read = vars.get('has_read', None)
        # result = db.executesql("SELECT * FROM MESSAGE_BOARD", as_dict=True)
        # print(result)
        # query = db.MESSAGE_BOARD.id > 1
        query = db.MESSAGE_BOARD.id > 0
        if sender:
            query &= (db.MESSAGE_BOARD.sender == sender)
        if receiver:
            query &= (db.MESSAGE_BOARD.receiver == receiver)
        if has_read:
            query &= (db.MESSAGE_BOARD.has_read == has_read)

        # rows = db(query).select(db.MESSAGE_BOARD.id,
        #                         db.MESSAGE_BOARD.message_content,
        #                         db.MESSAGE_BOARD.sender,
        #                         db.MESSAGE_BOARD.receiver,
        #                         db.MESSAGE_BOARD.has_read,
        #                         db.MESSAGE_BOARD.sent_time)
        #
        # print("========================================")
        # start_time = timeit.default_timer()
        # for r in rows:
        #     r.update_record(has_read=True)
        # print(str(timeit.default_timer() - start_time) + " seconds")

        start_time = timeit.default_timer()
        db(query).update(has_read=True)
        print(str(timeit.default_timer() - start_time) + " seconds")
        print("=========================================")

        return HTTP(201)

    return locals()
