from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'flask-todo'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask-todo'

mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def index():
    tasks = []
    for task in mongo.db.tasks.find():
        tasks.append({
            "_id": task["_id"],
            "task": task["task"],
            "status": task["status"]
        })
    return render_template("index.html", tasks=tasks, task_count=len(tasks))


@app.route("/", methods=["POST"])
def add_task():
    task = request.form.get("task")
    task_id = mongo.db.tasks.insert_one({
        "task": task,
        "status": False
    })
    return redirect("/")


@app.route("/remove/<id>")
def remove_task(id):
    mongo.db.tasks.delete_one({"_id": ObjectId(id)})
    return redirect("/")


@app.route("/update/<id>")
def update_task(id):
    task = mongo.db.tasks.find_one({"_id": ObjectId(id)})
    task["status"] = not task["status"]
    mongo.db.tasks.update_one({"_id": ObjectId(id)}, {
        "$set": task
    })
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
