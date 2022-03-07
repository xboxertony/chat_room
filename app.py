from time import sleep
from flask import Flask,render_template,session,request,redirect,url_for
from flask_socketio import SocketIO,emit,join_room,leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app)

@app.route("/chat")
def chat():
    room = session["room"]
    return render_template("index.html",room = room)

@socketio.on("my event",namespace="/chat")
def index(data):
    join_room(session.get("room"))
    # emit("status",data)

@socketio.on("text",namespace="/chat")
def get_msg(data):
    room = session["room"]
    print(request.sid)
    emit("message",session["user"]+" : "+data,room = room)
    sleep(10)
    emit("message","I am Here",room = room)

@app.route("/jjj")
def jjj():
    socketio.emit("message1",{"data":"Are you ok?"},namespace='/chat',to=session['room'])
    return "ok"

@app.route("/ggg")
def ggg():
    socketio.emit("message1",{"data":"Are you ok?"},namespace='/chat',to=session['room'])
    return "ok"

@app.route("/jjjj")
def kjkjk():
    socketio.emit("message",{"data":"Are you ok?"},namespace='/jjjj')
    return "ok"

@app.route("/testtest")
def gggg():
    return render_template("test.html")

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST" and request.form["user"] and request.form["room"]:
        session["user"]=request.form["user"]
        session["room"]=request.form["room"]
        return redirect(url_for("chat"))
    return render_template("home.html")

@socketio.on("left",namespace="/chat")
def leave(data):
    room = session["room"]
    leave_room(session["room"])
    print(data)
    emit("message",session["user"]+" leave the room \n",room = room)

@socketio.on("broadcast",namespace="/chat")
def b(data):
    emit("message",session["user"]+" from "+session["room"]+"  "+data+" \n",broadcast=True)

if __name__=="__main__":
    app.debug = True
    socketio.run(app)