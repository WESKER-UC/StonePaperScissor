from flask import Flask, render_template, request
from random import randint as rd

app = Flask(__name__)

def cvu(uch)->int:
    cch = rd(1,3)
    if uch == cch : return -1,cch
    else:
        if ((uch ==1 and cch == 2 ) or (uch ==2 and cch == 3 ) or (uch ==3 and cch ==1 ) ) : return 0,cch
        else : return 1,cch


@app.route("/")
def hello_world():
    return render_template('SPC.html')

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
        return render_template('SPC.html',ans=ans[0],cch=chl[ans[1]-1],uch=chl[uch-1])
    
    return render_template('SPC.html',ans=4)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
