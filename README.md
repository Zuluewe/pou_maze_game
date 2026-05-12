# Pou Maze Game

![image](assets/images/pou_hungry.png)

Pou maze game er et spil der tager udgangspunkt i det populære virtuel kældeyrs spil Pou. I dette projekt uviklede vi et "mini game", hvor man skal igennem en labyrint med en 60 sekunders timer. Man kan manipulere med tiden ved at samle et ur der giver 5 ekstra sekunder. For at komme til den næste bane skal man spise et stykke mad i slutningen af banen.

## MVC (Model, View, Controller)
Gennem dette projekt har vi taget udgangspunkt i MVC arkitektur strukten. Dvs at vi således har delt vores filer op på denne måde.

Model kommer til at håndtere spillerens logik, objekter i spiller og genereationen af labyrinter. Dette kan ses i:
 - <code> maze_generator.py </code>
 - <code> level.py </code>
     - <code> class LevelModel </code>

View kommer til at håndtere hvordan scenerne bliver tegnet samt objekter og spiller. Dette kan ses i:
 - <code> start.py </code>
 - <code> level.py </code>
    - <code> class LevelView </code>
 - <code> pause.py </code>
 - <code> game_over.py </code>

Controller kommer til at håndtere om spilleren bevæger sig (input) og om der er collision mellem spilleren og et objekt, samt hvilket level spilleren er på. Dette kan ses i:
- <code> controller.py </code>

## Flow Chart
Vores flowchart illustrerer kodens flow og arkitektur, den visser de forskellige processer der kører i vores app. Denne Flowchart illustrerer programmets flow og de forskellige processer der kører i løbet af spillet. Den er essentielt til optimering af koden og general visualisering af programmets struktur.

<img width="2649" height="2947" alt="image" src="https://github.com/user-attachments/assets/b71d4a66-559c-4f74-afcf-086ebb97374d"/>

## State Machine Diagram
Vores program fungerer ved at behandle forskellige views. Derfor er det relevant at udarbejde en adfærdsmæssige UML-diagram eksempelvis et stae machine diagram. En State Machine Diagram viser, hvordan en enhed reagerer på forskellige begivenheder ved at skifte fra en tilstand til en anden, og bruges derfor til at modeller et dynamisk system.

<img width="772" height="501" alt="image" src="https://github.com/user-attachments/assets/2d3e0f26-f761-448f-915e-d06f90826555" />

# Årsprojekt
<img width="120" height="92" alt="under_construction" src="https://github.com/user-attachments/assets/62064376-c006-4efd-9ddc-a7babe38beca" />

Da dette årlige projekt lige nu er i eksamensperioden, er koden stadig under udvikling, hvor der løbende indarbejdes fremtidige forbedringer.



