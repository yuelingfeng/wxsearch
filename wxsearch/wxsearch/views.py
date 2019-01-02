"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request
from wxsearch import app,db
from .models import Company,Users
from datetime import timedelta,datetime
import json
from .urlexts import getOpenID
from .querys import company_query,user_wxid_query,user_add
import random
import time

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')

@app.route('/query',methods=['GET','POST'])
def query():
    return 'query'

@app.route('/register',methods=['GET','POST'])
def register():
    '''
    :deacripton Company register
    '''
    if request.method == 'GET':
        _sn = request.args.get('sn')
        _ipaddress = request.args.get('ipaddress')
        _name = request.args.get('name')
        try:
            company = Company.query.filter_by(sn = _sn).first()
            if not company:
                company = Company(sn=_sn,ipaddress = _ipaddress,name=_name,state='N',duedate=datetime.now() + timedelta(days=365))
                db.session.add(company)
                db.session.commit()
                return json.dumps({'code':'0'})
        except Exception as e:
            return json.dumps({'code':'-1','msg':str(e)})
        #return '%s %s %s' % (_wxid,_ipaddress,_name)
        else:
            _remsg = u'序列号:' + _sn + u'已经注册，请检查序列号是否正确！'
            return json.dumps({'code':'1','msg':_remsg})

@app.route('/updateip',methods=['GET'])
def updateip():
    _sn = request.args.get('sn')
    _ipaddress = request.args.get('ipaddress')
    try:
        company = company_query(_sn)
        if company:
            company.ipaddress = _ipaddress
            db.session.commit()
            return json.dumps({'code':'0'})
        else:
            _remsg = u'序列号:' + _sn + u'还没有注册，请先注册，如果已经注册请检查序列号是否正确！'
            return json.dumps({'code':'1','msg':_remsg})
    except Exception as e:
        return  json.dumps({'code':'-1','msg':str(e)})

@app.route('/dataquery',methods=['GET'])
def dataquery():
    _wxid = request.args.get('wxid')
    try:
        user = Users.query.filter_by(wxid = _wxid).first()
        if not user:
            return json.dumps({'code':'1',
                 'msg':u''
                    })
    except Exception as e:
        return json.dumps({
            'code':'-1',
            'msg':str(e)})

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    try:
        _wxid = request.args.get('wxid')
        _sn = request.args.get('sn')
        _phone = request.args.get('phone')
        _name = request.args.get('name')
        _args = ''

        if not _wxid:
            _args = 'wxid'
        if not _sn:
            _args = 'sn'
        if not _phone:
            _args = 'phone'
        if not _name:
            _args = "name"

        if _args:
            return json.dumps({
                'code':'1',
                'msg':u'参数错误! %s ' % _args
                })

        _company = company_query(_sn)
        if not _company:
            return json.dumps({
                'code':'1',
                'msg':u'序列号%s不存在' % _sn
                })
        '''
        user login
        '''
        _users = user_wxid_query(_wxid)
        if _users:
            return json.dumps({
                'code':'2',
                'msg':u'用户登陆'
                })
        '''
        The new user register
        '''
        return user_add(_wxid,_name,_phone,_company.id)

    except Exception as e:
        return json.dumps({
            'code':'-1',
            'msg': 'views.userregister error ' + str(e)})


@app.route('/getwxopenid',methods=['GET'])
def getwxopenid():
    try:
       _js_code = request.args.get('jscode')
       return json.dumps(getOpenID(_js_code))
    except Exception as e:
        return json.dumps({
            'code':'-1',
            'msg': 'views.getwxopenid error' + str(e)
            })

@app.route('/nowdata',methods=['GET'])
def nowdata():
    _wxid = request.args.get('wxid')
    return json.dumps({
        'sales': '1900.00',
        'import': '3150.00',
        'customercount':128,
        'paypercustomer':'15.76',
        'salestrendslist':[random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,random.randint(1000,30000) / 10,
                           random.randint(1000,30000) / 10,]
        })

@app.route('/wxDataQuery',methods=['GET'])
def wxDataQuery():
    _code = request.args.get('code')
    _sn = request.args.get('sn')
    _formId = request.args.get('formId') ##根据formId号确定需要查询的数据是什么类型。

    time.sleep(random.randint(0,3))
    if _formId == 'providerCount':
        if _code not in ['1001','10001','1']:
            return json.dumps({
            
                'code':'1',
                'msg':'供应商不存在'
                })
        else:
            return json.dumps({
                'code':'0',
               'dataDetail':[{
                 'code': '1001',
                  'name': '昆明方凡科技有限公司',
                  'detail': {
                    'import': {
                      'quantity': '1358.85',
                      'amount': '58561.7'
                    },
                    'sales': {
                      'quantity': '111328.5',
                      'amount': '357857.23'
                    },
                    'stock': {
                      'quantity': '96874.33',
                      'amount': '196844.96'
                    }
                  }
                },
                {
                  'code': '10001',
                  'name': '王老吉',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                }
             ,
                {
                  'code': '10002',
                  'name': '王老吉2',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                },
                {
                  'code': '10003',
                  'name': '王老吉3',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                },
                {
                  'code': '10004',
                  'name': '王老吉4',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                },
                {
                  'code': '10005',
                  'name': '王老吉',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                },
                {
                  'code': '10006',
                  'name': '王老吉',
                  'detail': {
                    'import': {
                      'quantity': '4358.85',
                      'amount': '58961.7'
                    },
                    'sales': {
                      'quantity': '211328.5',
                      'amount': '657857.23'
                    },
                    'stock': {
                      'quantity': '196874.33',
                      'amount': '1960844.96'
                    }
                  }
                }]
                })
    elif _formId == 'providerDetail':
        return json.dumps({
            'code':'0',
            'dataDetail':[{
                'code': '10000081',
                'name': 'FF8000-收银机',
                'detail': {
                'import': {
                    'quantity': '1358.85',
                    'amount': '58561.7'
                },
                'sales': {
                    'quantity': '111328.5',
                    'amount': '357857.23'
                },
                'stock': {
                    'quantity': '96874.33',
                    'amount': '196844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            },
            {
                'code': '100000014',
                'name': '服务器 IBM X3100M4',
                'detail': {
                'import': {
                    'quantity': '4358.85',
                    'amount': '58961.7'
                },
                'sales': {
                    'quantity': '211328.5',
                    'amount': '657857.23'
                },
                'stock': {
                    'quantity': '196874.33',
                    'amount': '1960844.96'
                }
                }
            }
                          ]
            })
    else:
        return json.dumps({
                    'code':'0',
                   'dataDetail':[{
                     'code': '6901028317112',
                      'name': '花玉溪',
                      'detail': {
                        'import': {
                          'quantity': '1358.85',
                          'amount': '58561.7'
                        },
                        'sales': {
                          'quantity': '111328.5',
                          'amount': '357857.23'
                        },
                        'stock': {
                          'quantity': '96874.33',
                          'amount': '196844.96'
                        }
                      }
                    }]
                    })