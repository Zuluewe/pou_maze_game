# Pou Maze Game

![image](assets/images/pou_hungry.png)

Pou maze game er et spil der tager udgangspunkt i det populære virtuel kældeyrs spil Pou. I dette projekt uviklede vi et "mini game", hvor man skal igennem en labyrint med en 60 sekunders timer. Man kan manipulere med tiden ved at samle et ur der giver 5 ekstra sekunder. For at komme til den næste bane skal man spise et stykke mad i slutningen af banen.

## MVC (Model, View, Controller)
Gennem dette projekt har vi taget udgangspunkt i MVC arkitektur strukten. Dvs at vi således har delt vores filer op på denne måde.

Model kommer til at håndtere spillerens logik, objekter i spiller og genereationen af labyrinter. Dette kan ses i:
 - <code> maze_generator.py </code>
 - <code> Level.py </code>
     - <code> class LevelModel </code>

View kommer til at håndtere hvordan scenerne bliver tegnet samt objekter og spiller. Dette kan ses i:
- <code> views folder </code>
    - <code> start.py </code>
    - <code> level.py </code>
    - <code> pause.py </code>
    - <code> game_over.py </code>

Controller kommer til at håndtere om spilleren bevæger sig (input) og om der er collision mellem spilleren og et objekt, samt hvilket level spilleren er på. Dette kan ses i:
- <code> controller.py </code>

