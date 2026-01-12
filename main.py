from flask import Flask, redirect, render_template, request,session, url_for
from random import randint as rd
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
def cvu(uch)->int:
    cch = rd(1,3)
    if uch == cch : return -1,cch
    else:
        if ((uch ==1 and cch == 2 ) or (uch ==2 and cch == 3 ) or (uch ==3 and cch ==1 ) ) : return 0,cch
        else : return 1,cch


@app.route("/",methods=['GET'])
def hello_world():
    session['userscore']=0
    return redirect(url_for('scp'))

@app.route('/scp',methods = ['POST','GET'])
def scp():
    if request.method=='POST':
        
        
        uchval = request.form.get('radioDefault')
        if not uchval:
            return render_template('SPC.html', ans=4)
        ch ={'stone':1,'paper':2,'scissor':3}
        chl=['stone','paper','scissor']
        uch = ch[uchval]
        ans = cvu(uch)
        if session.get('count')==0:
                session['count']=1
                session['userscore']=0
        if ans[0] == 1 or ans[0] == -1:
            if session.get('count')==0:
                session['count']=1
                session['userscore']=0
                
            else:
                session['userscore']=session.get('userscore')+10
                
        else:
            session['userscore']=session.get('userscore')-5
        
        return render_template('SPC.html',ans=ans[0],cch=chl[ans[1]-1],uch=chl[uch-1], score = session.get('userscore'))
    
    return render_template('SPC.html',ans=4)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
