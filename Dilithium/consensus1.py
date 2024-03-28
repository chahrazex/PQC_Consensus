import time
import hashlib
import random
import base64
from dilithium import Dilithium2
from collections import Counter

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class ConsensusProcess:
    ROUND_TIME = 60  # Durée d'un cycle de consensus en secondes

    def __init__(self):
        self.CONSENSUS_START_TIME = time.time()  # Heure de début du consensus
        self.monotonic_counter = self.get_monotonic_counter_from_tee()  # Compteur monotone

    def generate_block(self, delegated_vote):
        # Vérification de l'intégrité du bloc
        if not self.verify_block_integrity(delegated_vote):
            return False

        # Génération de la chance (luck) en utilisant TEE
        luck = delegated_vote

        # Génération de la preuve dans le processus d'Attestation à distance
        proof = self.generate_proof(luck)

        # Diffusion du bloc
        self.broadcast_block(luck, proof)

        return True

    def verify_block_integrity(self, delegated_vote):
        # Vérifie si le temps du cycle de consensus est écoulé
        if time.time() > self.CONSENSUS_START_TIME + self.ROUND_TIME:
            print("Le temps du cycle de consensus est écoulé.")
            return False

        # Vérifie le compteur monotone
        current_monotonic_counter = self.get_monotonic_counter_from_tee()
        if current_monotonic_counter != self.monotonic_counter:
            print("La vérification du compteur monotone a échoué.")
            return False

        return True

    def generate_luck(self, delegated_vote):
        # Génère une valeur de chance (luck) en utilisant un générateur de nombres aléatoires
        # Utilise le vote délégué pour influencer la génération de la chance
        luck = delegated_vote 
        print("Chance (luck) générée avec succès.")
        return luck

    def generate_proof(self, luck):
        # Génère une preuve en concaténant la valeur de chance et le nonce
        nonce = self.calculate_nonce()
        proof = str(luck) + nonce
        proof_encoded = base64.b64encode(proof.encode()).decode()
        print("Preuve générée avec succès.")
        return proof_encoded

    def calculate_nonce(self):
        # Calcule un nonce à partir de l'en-tête du bloc
        block_header = "block_header_data"
        nonce = hashlib.sha256(block_header.encode()).hexdigest()
        print("Nonce calculé avec succès.")
        return nonce

    def broadcast_block(self, luck, proof):
        # Diffuse le bloc aux autres nœuds délégués
        print(f"Diffusion du bloc - Chance (luck): {luck}, Preuve: {proof}")

    def get_monotonic_counter_from_tee(self):
        # Récupère le compteur monotone depuis TEE
        monotonic_counter = 12345  # Valeur fictive pour la démonstration
        print("Compteur monotone récupéré avec succès.")
        return monotonic_counter

    def verify_block(self, block_data, delegated_vote):
        # Vérifie l'intégrité d'un bloc
        nonce = self.calculate_nonce()
        if nonce != block_data['nonce']:
            return False

        proof = block_data['proof']
        luck = block_data['luck']   
        proof_expected = str(luck) + nonce
        proof_expected_encoded = base64.b64encode(proof_expected.encode()).decode()
        if proof != proof_expected_encoded:
            return False

        return True

    def generate_transaction(self):
        # Génère une transaction en signant le message avec la clé privée
        transaction = Transaction("sender1", "receiver1", 1)
        print("Transaction générée avec succès.")
        return transaction.__dict__

    def sign_transaction(self, transaction_data):
        pk, sk = Dilithium2.keygen()# de sender
        self.private_key = sk  # initialise l'attribut 
        self.public_key = pk  # //
        T = str(transaction_data).encode()
        signature = Dilithium2.sign(self.private_key, T)
        print("Transaction signée avec succès.")
        return signature

    def verify_transaction(self, transaction_data, signature):
        T = str(transaction_data).encode()
        result = Dilithium2.verify(self.public_key, T, signature)
        return result

def main():
    consensus_process = ConsensusProcess()
    delegated_vote = random.randint(1, 10)  # ex pour ==random Simulation d'un vote délégué
    block_generated = consensus_process.generate_block(delegated_vote)

    if block_generated:
        print("Bloc généré avec succès.")

        # Exemple de vérification de bloc
        luck = consensus_process.generate_luck(delegated_vote)  # Génération de la chance
        block_data = {
            'nonce': consensus_process.calculate_nonce(),
            'luck': luck,
            'proof': consensus_process.generate_proof(luck)  # Génération de la preuve
        }
        if consensus_process.verify_block(block_data, delegated_vote):
            print("Bloc vérifié avec succès.")
        else:
            print("Échec de la vérification du bloc.")

        # Exemple de vérification de transaction
        transaction_data = consensus_process.generate_transaction()
        signature = consensus_process.sign_transaction(transaction_data)
        if consensus_process.verify_transaction(transaction_data, signature):
            print("Transaction vérifiée avec succès.")
        else:
            print("Échec de la vérification de la transaction.")
    else:
        print("Échec de la génération du bloc. La vérification de l'intégrité du bloc a échoué.")

if __name__ == "__main__":
    main()