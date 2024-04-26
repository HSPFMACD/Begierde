from flask import Flask, request, jsonify, render_template
from story_generator import extractKeywords, printFurtherStory, requestFurtherStoryWithOption, storyTextFileName

def startWebServer():
    app = Flask(__name__, template_folder = 'template')

    @app.route('/keywords', methods = ['GET'])
    def getKeywords():
        return jsonify(extractKeywords())
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/option', methods = ['POST'])
    def optionSelection():
        # select option
        option = request.get_json()
        printFurtherStory(requestFurtherStoryWithOption(option))
        return jsonify({"selected-option": option})
    
    app.run(host='0.0.0.0', port='8000')