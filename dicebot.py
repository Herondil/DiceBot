# -*- coding: utf-8 -*-
'''
nom : dice bot
auteur : Erendil - DoubleZ
Description : A bot dedicated to random dice values
'''


'''
                LICENCE PUBLIQUE RIEN À BRANLER
                      Version 1, Mars 2009

 Copyright (C) 2009 Sam Hocevar
  14 rue de Plaisance, 75014 Paris, France
 
 La copie et la distribution de copies exactes de cette licence sont
 autorisées, et toute modification est permise à condition de changer
 le nom de la licence. 

         CONDITIONS DE COPIE, DISTRIBUTON ET MODIFICATION
               DE LA LICENCE PUBLIQUE RIEN À BRANLER

  0. Faites ce que vous voulez, j’en ai RIEN À BRANLER. 
'''

#Libraries
import irclib
import ircbot
import random

#Variables importantes
nick = "DiceBot"
description = "Génère des scores de dés"
room = "#riff"
server = "irc.worldnet.net"
port = 6667
utilisateurs = ["Herondil"]
messagePublic = "Bien joué, je suis un bot ! Parle moi en MP si tu en veux plus"
#Maximum dice is 10d100
maxDiceThrows = 10
maxDiceFaces  = 100

    
def isNumber(chaine):
  if len(chaine) > 0 :
    for lettre in chaine :
      if not (lettre in ["0","1","2","3","4","5","6","7","8","9"]):
        return False
    return True
  else :
    return False
    
class DiceBot(ircbot.SingleServerIRCBot):
  def __init__(self):
    global nick
    global room
    global server
    global port
    global messagePublic
    global maxDiceThrows
    global maxDiceFaces
    
    ircbot.SingleServerIRCBot.__init__(self, [(server, port)],nick,description)
    
  def on_welcome(self,serv,ev):
    serv.join(room)

  #Commande en public
  def on_pubmsg(self,serv,ev):
    auteur = irclib.nm_to_n(ev.source())
    canal = ev.target()
    message = ev.arguments()[0].split(" ")

    if message[0] == "!" + nick :
      serv.privmsg(room,messagePublic)

    if message[0] in ["!lancer","!lance"] :
      serv.privmsg(room,"%s fait %s" % (auteur, random.randint(1,6)) )

    if message[0] == "!throw" :
      if len(message) != 3 :
        serv.privmsg(auteur,"Erreur, écrire '!throw 1 6' par exemple")
      else :
        if isNumber(message[1]) and isNumber(message[2]) :
          faces  = int(message[2])
          if faces <= maxDiceFaces :
            throws = int(message[1])
            if throws <= maxDiceThrows :
              if faces != 0 :
                result = ""
                for i in range(0,throws) :
                  result = "%d %s" % (random.randint(1,faces), result)
                serv.privmsg(room,"%s fait %s" % (auteur, result) )
              else :
                serv.privmsg(auteur,"Erreur, on ne peut pas lancer un dés à 0 faces !")
            else :
              serv.privmsg(auteur, "%d dés maximum pour le lancé" % (maxDiceThrows, ) )
          else :
            serv.privmsg(auteur, "%d faces maximum pour le lancé" % (maxDiceFaces, ))
        else :
          serv.privmsg(auteur,"Erreur, écrire des entiers naturels après '!throw'")
        
  
  #Les commandes a utiliser via MP
  def on_privmsg(self,serv,ev):
    auteur = irclib.nm_to_n(ev.source())
    canal = ev.target()
    message = ev.arguments()[0].split(" ")
    
    #Commandes réalisable par les modos uniquement
    if auteur in utilisateurs:
      #En cas de commande erronée test
      if not (message[0] in ["!pubMessage","!nick","!help","!aide","!modo","!nomodo","!listmodo","!listmodos","!parler","!parle","!throw"]) :
		serv.privmsg(auteur,"Erreur de commande, utilisez !aide pour voir les commandes")
	
      #Commande ne necessitant aucun paramètre
      if message[0] == "!help" or message[0] == "!aide" :
		serv.privmsg(auteur,"Commandes possibles :")
		serv.privmsg(auteur,"-****__=_=_=_=_=___****-")
		serv.privmsg(auteur,"!throw X Y     : lance X dés à Y faces résultat en public")
		serv.privmsg(auteur,"!modo X        : ajoute X comme utilisateur du bot")
		serv.privmsg(auteur,"!nomodo X      : retire X comme utilisateur du bot")
		serv.privmsg(auteur,"!parle X       : fait parler le bot sur #riff")
		serv.privmsg(auteur,"!nick X        : renomme le bot par X ")
		serv.privmsg(auteur,"!listmodo      : liste tous les utilisateurs du bot")
		serv.privmsg(auteur,"!pubMessage X  : change en X le message public donné par !"+nick)
		serv.privmsg(auteur,"-****__=_=_=_=_=___****-")

      if message[0] == "!pubMessage" :
        if len(message) == 1 :
	  serv.privmsg(auteur,"Cette commande requiert de rentrer une phrase en tant que message public du bot")
        else :
          global messagePublic
          nouveau3 = message[1:]
	  phrase3 = ""
          for mot in nouveau3 :
            phrase3 += mot + " "
	  messagePublic = phrase3
	  serv.privmsg(auteur, phrase3 + " est la nouvelle phrase publique du bot")
      
      if message[0] == "!parle" or message[0] == "!parler" :
        if len(message) == 1 :
	  serv.privmsg(auteur,"Cette commande requiert de rentrer une phrase à faire prononcer par le bot")
	else :
	  try :
	    nouveau = message[1:]
	    phrase2 = ""
	    for mot in nouveau :
	      phrase2 += mot + " "
	      
	    serv.privmsg(room,phrase2)
	    serv.privmsg(auteur,"Message publique envoyé")
	  except :
	    pass
	  
      if message[0] == "!nick" :
        if len(message) == 1 :
          serv.privmsg(auteur,"Cette commande requiert de rentrer le nouveau nom du bot")
        else :
          serv.nick(message[1])
          serv.privmsg(auteur,"Bot renommé")
	  
      if message[0] == "!listmodo" or message[0] == "!listmodos" :
	serv.privmsg(auteur,"Les utilisateurs pouvant utiliser le bot sont : " + str(utilisateurs))
	          
      if message[0] == "!modo" :
        if len(message) == 1 :
          serv.privmsg(auteur,"Cette commande requiert de rentrer un nom")
        else :
          try :
            utilisateurs.append(message[1])
            serv.privmsg(auteur,message[1] + " peut maintenant utiliser les commandes du bot")
          except :
            pass
	      
      if message[0] == "!nomodo" :
        if len(message) == 1 :
          serv.privmsg(auteur,"Cette commande requiert de rentrer un nom de modo à supprimer")
        else :
          if message[1] != auteur :
            try :
              if message[1] in utilisateurs :
                for index,name in enumerate(utilisateurs):
                  if name == message[1]:
                    utilisateurs.pop(index)
                    serv.privmsg(auteur,message[1] + " ne peut plus utiliser les commandes du bot")
              else :
                serv.privmsg(auteur,"utilisateur invalide, !listmodo pour voir les utilisateur du bot")
	    
            except :
              pass
            
          else :
            serv.privmsg(auteur,"Vous ne pouvez pas vous enlever vous-même de la liste des utilisateurs")
			           
if __name__ == "__main__":
  DiceBot().start()
