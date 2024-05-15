import json
from flask import Flask, request, jsonify, render_template
from story_generator import extractKeywords, printFurtherStory, requestFurtherStoryWithOption, storyTextFileName

def startWebServer():
    app = Flask(__name__, template_folder = 'template')

    @app.route('/keywords', methods = ['GET'])
    def getKeywords():
        return jsonify(extractKeywords())
    
    @app.route('/story', methods = ['GET'])
    def getStory():
        try:
            with open('story.json', 'r') as file:
                story_data = json.load(file)
            return jsonify(story_data), 200
        except FileNotFoundError:
            return jsonify({'error': 'Die Datei story.json wurde nicht gefunden.'}), 404
        except Exception as e:
            return jsonify({'error': 'Ein Fehler ist aufgetreten: {}'.format(str(e))}), 500
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/macd')
    def macd():
        return render_template('website/index.html')
    
    @app.route('/option', methods = ['POST'])
    def optionSelection():
        # select option
        option = request.get_json()
        printFurtherStory(requestFurtherStoryWithOption(option))
        return jsonify({"selected-option": option})
    
    app.run(host='0.0.0.0', port='8000')