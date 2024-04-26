import time
from story_generator import extractKeywords, printFurtherStory, requestFurtherStoryWithOption

def receive_console_input():
    # solange das Programm läuft soll diese Schleife loopen und eine benutzereingabe erwarten
    while True:
        try:
            furtherStory = input ("Was soll ich drucken? ").strip()
            if furtherStory.startswith("1"):
                printFurtherStory("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eleifend magna consequat, feugiat mauris a, semper arcu. Vestibulum blandit dui quis diam lobortis, eget iaculis turpis volutpat. Vivamus sed ex semper, commodo arcu.")
                printFurtherStory("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eleifend magna consequat, feugiat mauris a, semper arcu. Vestibulum blandit dui quis diam lobortis, eget iaculis turpis volutpat. Vivamus sed ex semper, commodo arcu.")
                printFurtherStory("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eleifend magna consequat, feugiat mauris a, semper arcu. Vestibulum blandit dui quis diam lobortis, eget iaculis turpis volutpat. Vivamus sed ex semper, commodo arcu.")
                time.sleep(30)
                break       
            elif furtherStory.startswith("2"):
                print("Sonderfall 2")
                break
            else:
                #print(furtherStory)
                printFurtherStory(furtherStory)
                
        except ValueError:
            print ("Error - fehlerhafte eingabe")