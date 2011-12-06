from eh import app, db
db.create_all()
app.run(debug=True)
