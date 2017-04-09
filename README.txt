Name: Andrei Iordache
Email: andrei.iordache.uk@gmail.com

For questions or simply out of boredom, do not hesitate to contact me.

Disclaimer:
  The game is supposed to be played from various IP addresses. I am using localhost
        as it proved itself reliable. Using different IP addresses returns a timeout
        usually.

  For best performances and in lack of friends, use localhost and challenge yourself
        from multiple terminals.
  Enjoy ^^

HOW TO PLAY:
  start server with:
    python myserver.py localhost [port]
  join with:
    python client.py localhost [port] [name]

COMMANDS:
  'status' - Displays info about the trainers and their Kudomons

  'move up' - from {x, y} to {x, y - 1}
  'move down' - from {x, y} to {x, y + 1}
  'move left' - from {x, y} to {x - 1, y}
  'move right' - from {x, y} to {x + 1, y}

  'nearby' - Displays the nearby Kudomons based on 3 levels:
                        -in range: you can catch them
                        -close: pretty close, yet you can not catch them
                        -nearby: not as close, but you can smell them

  'catch' - Allows you to randomly catch a kudomon if in range
  'challenge [enemy_name]' - Sends a challenge to [enemy_name]. If he agrees, the fight will commence


Example:
  [0]: python myserver.py localhost 8072
  [1]: python client.py localhost 8072 Alex
  [2]: python client.py localhost 8072 Andrei
  [1]: status
              Andrei(89, 83) - Score:0  //Andrei - name, {89, 83} position
              Kudomons:
              Alex(22, 92) - Score:0
              Kudomons:
  [2]: nearby
              In range:
              Close:
                      Finn: rock(179, 28) //Finn - name; (179, 28) - (HP, CP)
                                          //HP = 179
                                          //CP = 28
                      Louie: rock(83, 5)
              Nearby:
                      Cash: grass(122, 20)
                      Moose: electric(176, 10)
                      Samson: rock(148, 12)

  //fast forward till I catch some kudomons

  [1]: challenge Andrei
  [2]: yes
              //Output on [2].. on [1] it said I lost and I did not want to lose :(
              Elvis: electric(105, 26) attacks Finn: rock(179, 28)inflicting 26 damage.       Finn: rock(153, 28)
              Finn: rock(153, 28) attacks Elvis: electric(105, 26)inflicting 49 damage. It is SUPER EFFECTIVE!        Elvis: electric(56, 26)
              Elvis: electric(56, 26) attacks Finn: rock(153, 28)inflicting 26 damage.        Finn: rock(127, 28)
              Finn: rock(127, 28) attacks Elvis: electric(56, 26)inflicting 28 damage.        Elvis: electric(28, 26)
              Elvis: electric(28, 26) attacks Finn: rock(127, 28)inflicting 26 damage.        Finn: rock(101, 28)
              Finn: rock(101, 28) attacks Elvis: electric(28, 26)inflicting 28 damage.        Elvis: electric(0, 26)
              You won the fight!

  [2]: status
              //Notice that Alex lost his kudomon. ^^
              Andrei(89, 88) - Score:0
              Kudomons:
                      Finn: rock(101, 28)
              Alex(26, 89) - Score:0
              Kudomons:
