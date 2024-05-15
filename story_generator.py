import json
import time
from yattag import Doc
from openai import OpenAI
from datetime import datetime


current_options_buttons = {}
current_story_object = {
   "story":"Geschichte",
   "option1":{
      "path":"Option wie die geschichte weiter gehen könnte",
      "keyword":"Option 1"
   },
   "option2":{
      "path":"Option wie die geschichte weiter gehen könnte",
      "keyword":"Option 2"
   },
   "option3":{
      "path":"Option wie die geschichte weiter gehen könnte",
      "keyword":"Option 3"
   }
}
storyTextFileName = ""


initialPrompt = 'Erstelle eine Geschichte mit der Länge von 30 Worten. Nach der Geschichte erzeuge drei Optionen bzw. Erzählstränge wie die geschichte weitergehen könnte. Beschreibe grob die potentiellen Erzählstränge und stelle für jede Option bzw. jeden Erzählstrang ein eindeutiges Wort oder maximal zwei Wörter dar und stelle dieses Wort bzw. Wörter im json format dar.  Erstelle die Antwort im folgenden JSON Format: { "story":"Geschichte", "option1":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" }, "option2":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" }, "option3":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" } }'

# Create a new HTML document
doc, tag, text = Doc().tagtext()

def requestInitialStory():
    try:
        client = OpenAI(api_key = "xx")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. Du gibst nur Antworten in deutscher Sprache aus."},
                {"role": "user", "content": initialPrompt}
              ]
            )
        global current_story_object
        current_story_object = json.loads(response.choices[0].message.content)

        print("----- Initiale Story: " + current_story_object["story"])
        return current_story_object["story"]
    except Exception as e:
        print("Fehler beim Aufrufen des Endpunkts:", e)
        return None

def requestFurtherStoryWithOption(option):
    print("----- Option gewählt: " +option)
    try:
        client = OpenAI(api_key = "xxx")
        global current_story_object
        prompt = 'Erzähle die Geschichte logisch und zusammenhängend mit dem Keyword "' + current_story_object[option]["keyword"] + '" weiter und ersetze die Fortführung im Story objekt. Der vorgeschlagene Erzählstrang der am Keyword hängt ist wie folgt: '+current_story_object[option]["path"]+'. Es soll ausschließlich der neu generierte Text in der Antwort auftauchen - vorangegangene Passagen dürfen nicht nochmal in der Antwort erscheinen. Die letzte vorangegangene Passage war wie folgt: "' + current_story_object["story"] + '". Schlage nach dem erstellen der neuen zusammenhängenden Textpassage erneut drei weitere Optionen bzw. Erzählstränge vor und gib mir die Antwort im folgenden JSON Format: { "story":"Geschichte", "option1":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" }, "option2":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" }, "option3":{ "path":"Option wie die geschichte weiter gehen könnte", "keyword":"Option" } }. Die Erzählstränge haben ein möglichds konkretes bzw. prägnantes Keyword. Die neue Passage darf ebenfalls maximal 30 Worte umfassen.'
       
        print("----- Folge Prompt: " + prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. Du antwortest immer in der deutschen Sprache."},
                {"role": "user", "content": prompt}
              ]
            )
       
        current_story_object = json.loads(response.choices[0].message.content)


        print("----- Story Weiterführung: " + current_story_object["story"])
        print("----- "+ current_story_object["option1"]["keyword"] +": " + current_story_object["option1"]["path"])
        print("----- "+ current_story_object["option2"]["keyword"] +": " + current_story_object["option2"]["path"])
        print("----- "+ current_story_object["option3"]["keyword"] +": " + current_story_object["option3"]["path"])
        return current_story_object["story"]
    except Exception as e:
        print("Fehler beim Aufrufen des Endpunkts:", e)
        return None
    
def printFurtherStory(furtherStory):
    printer = open("furtherStory.txt", "w")
    printer.write(furtherStory)
    printer.close()
    concatStoryToTextFile(furtherStory)
    # TODO druckauftrag starten
    #os.system('paps --font=\"Courier, Monospace 52\" furtherStory.txt | lp -d POS58')

def concatStoryToTextFile(furtherStory):
    print(storyTextFileName)
    printer = open(storyTextFileName, "a+")
    printer.write(furtherStory)
    printer.close()
    addNewTextToHTML(furtherStory)
    updateJSONFile(furtherStory)


def addNewTextToHTML(text):
    currentDate = datetime.now()
    dateFormat = currentDate.strftime("%Y-%m-%d_%H:%M:%S")
    with doc.tag('div', id='story_' + dateFormat):
        with doc.tag('p'):
            doc.text(text)

     # Render HTML document
    html_content = doc.getvalue()

    # Write HTML content to a file
    with open('story.html', 'w') as file:
        file.write(html_content)


def extractKeywords():
    global current_options_buttons
    current_options_buttons = {"option-1": current_story_object["option1"]["keyword"], "option-2": current_story_object["option2"]["keyword"], "option-3": current_story_object["option3"]["keyword"]}
    return current_options_buttons

def createJSONFile():
    data = []
    with open('story.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)   


def updateJSONFile(new_storyphrase):
    with open('story.json', 'r') as json_file:
        data = json.load(json_file)
    
    new_data = {
        "timestamp": str(round(time.time() * 1000)),
        "storyphrase": new_storyphrase
    }
    data.append(new_data)

    with open('story.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
