from flask import Flask
app =  Flask("test")

@app.route('/')
def index():
        return "Hello world !"

if __name__ == '__main__':
    app.run()