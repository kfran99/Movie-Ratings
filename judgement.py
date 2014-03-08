from flask import Flask, render_template, redirect, request
import model

@app.route("/")
def index():
    return "Hello world!"

if __name__ == "__main__":
    app.run(debug = True)