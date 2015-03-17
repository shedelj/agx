# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


@auth.requires_login()
def fav():
    r = db(db.dev.id == request.args(0)).select().first()
    fav = db(db.auth_user.id == auth.user_id).select().first().favorites
    if r not in fav:
        fav.append(r)
    db(db.auth_user.id == auth.user_id).update(favorites=fav)
    redirect(URL('default', 'index'))
    return

def time():
    r = db(db.dev.id == request.args(0)).select().first()
    form = SQLFORM(db.dev, record=r, readonly=True)
    time35 = r.time_35
    time120 = r.time_120
    return dict(form=form, time35=time35, time120=time120)

def index():
    """
        This is the main dev chart display.
    """
    q = (db.dev)

    def generate_fav_button(row):
        b = ''
        b = A('Favorite', _class='btn', _href=URL('default', 'fav', args=[row.id]))
        return b

    def generate_time_button(row):
        b = ''
        b = A('Time', _class='btn', _align="center", _href=URL('default', 'time', args=[row.id]))
        return b

    links = [dict(header='', body=generate_fav_button),
             dict(header='', body=generate_time_button),]

    form = SQLFORM.grid(q,
        links = links,
        fields=[db.dev.film,
                db.dev.developer,
                db.dev.dilution,
                db.dev.iso,
                db.dev.time_35,
                db.dev.time_120,
                db.dev.temperature,
                ],
        orderby = [db.dev.film],
        editable=False, deletable=False, details=False,
        paginate = 15,
        csv = False,
        )
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
