# Djurschack

Ett roligt schackspel i tecknad stil där pjäserna är djur!

## Pjäserna
- **Dam** = katt (med krona)
- **Kung** = hund (med krona)
- **Häst** = häst
- **Bonde** = ankunge
- **Löpare** = klumpfisk
- **Torn** = bok

## Det här finns i spelet
- Schack för två spelare vid samma dator, eller mot datorn (nivå 1–10)
- Flytta pjäserna genom att dra dem med musen
- Gröna markeringar visar vart pjäsen kan gå
- Alla schackregler: schack och matt, rockad, en passant och patt
- Förklarande meddelanden när ett drag inte är tillåtet
- **Schackuppgifter** i tolv kapitel för den som just lärt sig reglerna:
  slå pjäser, skydda pjäser, schack, ur schack, schackmatt, matt eller patt,
  bondeförvandling, gaffel, bindning och spett, avtäckt schack, försvar och
  matt på två drag
- Ljud vid schack och vinst (om ljudfiler finns)

## Installera

1. Installera Python 3.7 eller nyare
2. Installera det som behövs:
   ```bash
   pip install -r requirements.txt
   ```

## Starta spelet

```bash
python main.py
```

Om spelet kraschar skrivs felet till `logs/game.log`.

## Så spelar du

1. Vit börjar
2. Klicka och dra en pjäs för att flytta den
3. När du tar upp en pjäs visas de rutor den kan gå till i grönt
4. Om ett drag inte är tillåtet förklarar en ruta varför

## Schackuppgifter

Välj **Lös schackproblem** i menyn. Varje uppgift har ett mål, en **Tips**-knapp,
**Börja om** och **Nästa**. Gör du fel börjar uppgiften om, och efter två
misslyckade försök visas tipset automatiskt.

Alla uppgifter kontrolleras med:

```bash
python test_problems.py
```

## Ljud (valfritt)

Lägg de här WAV-filerna i mappen `assets/sounds/`:
- `check.wav` – spelas vid schack
- `win.wav` – spelas vid schackmatt

## Kontroller

- **Vänster musknapp**: klicka och dra för att flytta pjäser
- **Stäng fönstret**: avsluta spelet

Lycka till med djurschacket!
