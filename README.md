Jeg fikk høre at jeg kunne bruke noe som het "pygame" så jeg fant denne siden om hvordan jeg skulle installere det: https://www.geeksforgeeks.org/how-to-install-pygame-in-windows/
Koden jeg forklarer er ganske lang, men den mest fylte og interesante er kanskje klassene: class Pipe, og class Player, som begge har mange funksjoner. 
Jeg valgte å bruke klasser for player og pipe fordi da kan jeg lett bare legge til flere players eller pipes.
Jeg har brukt mest av hjernen min (matte, fysikk, IKT kunnskap, osv) og ting jeg har kommet opp med gjennom kodingen, 
men hvis jeg satt fast (ofte om noe innenfor pygame som jeg ikke skjønte) søkte jeg på nettet etter løsninger. 
Hvis jeg fikk en error som jeg ikke sjønte så gikk jeg til ChatGpt som ofte klarte å løse det, 
men jeg merket når koden min ble lengere og lengere så ga ChatGpt værre og værre svar.
Da virket ChatGpt mer som et hint.

På starten er de mange konstante variabler, eller variabler som lagres så lenge vindue er åpent.
Det er to hoved funksjoner:

    -   QuickText(): jeg syntes det var klønete å lage så mange ting for å tegne text. Du måtte lage font, lage teksten også tegne den. 
        Med denne funksjonen er det bare input parametre så tegner den det med en gang.

    -   QuickImage(): i prinsippe det samme som QuickText(), men tar en pygame.image input istedet for en image source. 
        Dette er fordi det å bruke pygame.image.load() hver gang jeg skulle tegne et bilde var veldig krevende, 
        så istedet loader den bildene på forhånd og bare setter størrelse og posisjon i funksjonen.

Så kommer de store delene, Classes:

    -   Class Pipe: jeg forklarer hver funksjon hver for seg:

        __init__(): 
            Først definerer vi en boolean som blir true når den har passert player. Dette hjelper øke score.
            Når en pipe initialiseres så tar den en input av X. 
            Siden x posisjonen på player endres aldri, så setter vi bare self.x = X. 
            Dette kan være anderledes hvis du har er guest også.
            Toppen av pipe hullet defineres tilfeldig, og Bunnen av pipe hullet defineres baser på toppen + hull størrelse.
        draw():
            Definerer høyden på pipe bildet, dette endres såvidt med pipe bredde.
        move():
            Beveger pipen til venste.
        offScrean():
            Returnerer True hvis pipen har gått helt til venste av skjermen.
        hitboxTop():
            Returnerer posisjon, width og height til den øverste pipen.
        hitboxBottom():
            Returnerer posisjon, width og height til den nederste pipen.
        
    - Class Player:

        __init__():
            Definerer en del variabler som blir holdt i player.
        gravity():
            Kalkulerer gravitasjon og oppdaterer hastigheten.
        updateJump():
            Sjekker om knappen har blitt sluppet etter en veldig kort periode, 
            og oppdaterer hastighet basert på jump kraft.
        updateGlide():
            Sjekker om knappen har blitt holdt mer enn en kort stund,
            og oppdaterer hastighet med sin egen hastighet^2.
            Så dette er egentlig formelen til luftmotstand. Dragforce = Velocity^2
        updatePosition():
            Oppdaterer posisjonen basert på hastighet.
        draw():
            Tegner fuglen på posisjonen.
        executeOps():
            Denne kaller gravity(), updateJump(), updateGlide(), updatePosition(), paths(), draw() i et så jeg senere slipper å skrive alle funksjonene.
        hitbox():
            Returnerer hitboxen til player.
        collided():
            Returnerer True hvis player hitboxen treffer enten pipeTop eller pipeBottom.
        paths():
            Fyller en liste, path[], med posisjonen.
            Oppdaterer den listen til å vise bevegelse fram og litt air turbulance.
            Så tegner den list ved bruk av pygame.draw.lines() funksjonen.

Denne koden har to hoved "phases"

Phase 0: Blue Phase
    -   I denne seksjonen viser den brukeren et bildet ("ash665") som har en prosent del som går helt opp til 98%, (irriterende, ikke sant?)
    - Brukeren kan trykke tallet 8 på tastaturet for å starte fase 1

Phase 1: The Running Phase
    -   Fase 1 består egentlig av to "Sub Phases"

    -   På starten av fase 1 definerer den noen variables som skal restarte etter hver runde, dette inkluderer: 

            Mange pipe variabler som f.eks: pipeSpeed, pipeGap, pipeWidth, osv. 
            Disse må jeg definere her fordi de endres gjennom spillet og jeg vil at de skal resettes etter du starter en ny runde.

            "pipes" liste,
            
            Time variables:

            "timeSinceLastPipe" som er brukt til å forstå når en ny pipe skulle bli lagd.
            "timeStep" som er brukt i et annet interval for å øke vansklighetsgraden over tid, litt og litt.
            "clock" som er en pygame class som kan bli brukt til å forholde intervaler som er basert på tid (hvis ikke ville bilde frekvensen kunne endre på sånt, det er ikke bra.)

            Players:

            "player" objekt,
            "guest" objekt som kunne bli brukt dersom brukeren valgte coop mode.

            Score trackers:

            "newHighscore" boolean,
            "score" en integer som øker når en pipe har passert.
    
    Sub Phase 0: The Game
        -   Definerer noe først som jeg vil kalle si at man kunne kalt "deltaTime", eller det er det jeg ville gjort i andre program. Ganske standar.

        -   Event check: Sjekker etter knap tasting og utgjør en operasjon, ofte med en funksjon.

        -   Background Image: fyller skjermen med bakgrunns bilde gjennom funksjon QuickImage() jeg lagde, dette må gjøres tidligere før vi begynner å tegne andre ting.

        -   Pipe Assignment: tillegger "pipe" basert på frekvensen tilgitt. 
            Dette er sjekket sånn: timeSinceLastPipe * pipeSpeed >= pipeFreq, fordi frekvensen trenger ikke å endre distanse mellom pipene selv om pipene beveger seg raskere.
        
        -   Difficulty over time: over tid øker mange av pipe variablene som f.eks: pipeSpeed, pipeGap, pipeWidth, osv.

        -   Pipe Operations: tilsetter posisjonene til pipene, og tegner pipene. Pipene sjekkes også om spilleren har kollidert, hvis de har det er det game over. 
            Hvis pipene har gått ut av skjermen, POP! (pipes.pop(i) fjærner elemente med index i fra listen)

        -   Player Operations: kaller funksjonen executeOps() som kaller andre funksjoner som: updatePosition(), gravity(), draw(), paths(), osv. 
            Dette gjøres også på guest hvis det er coop mode

        -   Draw score: denne sjekker om player har fått en ny highscore, hvis det så tegner den highscore med en grønn farge, hvis ikke så er den svart.

        -   Update Display: oppdaterer display, dette må gjøres etter hver gang for å se tingene vi har tegnet.

    Sub Phase 1: Death Screen
        -   Fyller bakgrunnen til en farge
        -   Tegner score meldingen som er anderledes om du fikk en ny highscore eller ikke.
        -   Sjekker events om du trykker Spacebar så starter en ny runde.

Egen vurdering:
Jeg syntes min kode er ganske greit, hadde lyst til å rotere fuglen men det funket ikke. 
Jeg hadde lyst til å reworke pygame.draw.lines() funksjonen, men hadde ikke tid til det. 
Det er garantert litt usystematisk eller klønete men jeg syntes jeg fikk til en bra orden.
Det er flere ting jeg hadde lyst til å gjøre, noen ting kodet jeg som jeg valgte å kutte fra spillet, 
f.eks litt like som paths så kan du se den fremtidige trajectory av fuglen ved å kalkulere tyngdekraften.
Hvis jeg hadde mer tid så ville jeg kanskje forberedt utsene på ting, spesielt death screen.
Jeg fokuserte jo mest av min tid på å teste ut forskjellige funksjoner til spillet mitt, mange som funket.
Jeg ville kanskje sett mer på hvordan man ville gjort rotation av fuglen siden det fungerte ikke i det hele tatt når jeg prøvde.
Derfor endte jeg med dråppet den ideen. Så jeg håper at paths() funksjonen min la til noe litt mer interesant å se på.
