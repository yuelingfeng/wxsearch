from .models import Company,Users
from .exts import db
from json import dumps

def company_query(sn):
    '''
    :description Use sn to query companies
    :input type str sn
    '''
    return Company.query.filter_by(sn = sn).first()

def user_wxid_query(wxid):
    '''
    :description Query users using wxid. If wxid exists and the state == N, the user exists
    '''
    return Users.query.filter_by(wxid=wxid,state='N').first()

def user_add(wxid,name,phone,company):
    '''
    :description Add a user into the table
    :input wxid 
    :input name
    :input phone
    :input company
    '''
    try:
        user = Users(name=name,wxid=wxid,phone=phone,company=company)
        db.session.add(user)
        db.session.commit()
        return dumps({
            'code':'0',
            'msg':'注册成功'
            })
    except Exception as e:
        return dumps({
            'code':'1',
            'msg':'querys.user_add error ' + str(e)
            })

class SalesQuery(object):
    """
    description：Sale query at one store or all 
    """
    def __init__(self):
        pass
    
