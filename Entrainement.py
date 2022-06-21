class Banque():
    def __init__(self, nom):
        self.nom = nom
        self.solde = 0
        self.historique = []
    def depot(self, quantité):
        self.solde += quantité
        self.historique.append(("Depot", quantité))
        print(self.nom, "a déposé", quantité, "$ sur son propre compte")
        print(self.nom, "a desormais", self.solde,"$")
    def retrait(self, quantité):
        self.solde -= quantité
        self.historique.append(("Retrait", quantité))
        print(self.nom, "a retiré", quantité, "$ sur son propre compte")
        print(self.nom, "a desormais", self.solde,"$")
    def recoit(self, quantité, nom):
        self.solde += quantité
        self.historique.append(("Reception de".format(nom),quantité ))
    def transfert(self, quantité, destinataire ):
        self.solde -= quantité
        self.historique.append(("Tranfert vers {}".format(destinataire.nom), quantité))
        print(self.nom, "viens de donner", quantité, "$ à", destinataire.nom)
        print(self.nom, "a desormais", self.solde,"$")
        destinataire.recoit(quantité, self.nom)
        print(destinataire.nom, "a desormais",destinataire.solde)


Max_account = Banque("Max")
Pierre_account =  Banque("Pierre")
Max_account.depot(50000)
Pierre_account.depot(45000)
Max_account.transfert(2000, Pierre_account)
Max_account.retrait(10000)
Pierre_account.retrait(12000)
print(Max_account.historique)
print((Pierre_account.historique))


