import threading
from datetime import datetime
import story_generator
from story_generator import printFurtherStory, requestInitialStory
from user_input import receive_console_input
from web_server import startWebServer


if __name__ == "__main__":
    print("----- PrinterBox gestartet")
    currentDate = datetime.now()
    dateFormat = currentDate.strftime("%Y-%m-%d_%H:%M:%S")
    story_generator.storyTextFileName = "story_" + dateFormat + ".txt"
    f = open(story_generator.storyTextFileName, "w")  
    f.write("Datum: " + dateFormat + "\n")
    f.close()   

    story_generator.createJSONFile()

    printFurtherStory(requestInitialStory())
    # Starte Threads für die Konsoleingabe und den Webserver
    flask_thread = threading.Thread(target=startWebServer)
    #console_input_thread = threading.Thread(target=receive_console_input)

    flask_thread.start()
   # console_input_thread.start()

    # Warte darauf, dass die Threads beendet werden
    flask_thread.join()
   # console_input_thread.join()