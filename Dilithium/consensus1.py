import time
import hashlib
import random
import base64
from dilithium import Dilithium2

class ConsensusProcess:
    ROUND_TIME = 60

    def __init__(self):
        self.CONSENSUS_START_TIME = time.time()
        self.monotonic_counter = self.get_monotonic_counter_from_tee()
        pk, sk = Dilithium2.keygen()  # Générer les clés une seule fois ici pour la classe ConsensusProcess
        self.public_key = pk
        self.private_key = sk

    def generate_block(self, delegated_vote):
        if not self.verify_block_integrity(delegated_vote):
            return False

        luck = delegated_vote
        proof = self.generate_proof(luck)

        self.broadcast_block(luck, proof)

        return True

    def verify_block_integrity(self, delegated_vote):
        if time.time() > self.CONSENSUS_START_TIME + self.ROUND_TIME:
            print("Le temps du cycle de consensus est écoulé.")
            return False

        current_monotonic_counter = self.get_monotonic_counter_from_tee()
        if current_monotonic_counter != self.monotonic_counter:
            print("La vérification du compteur monotone a échoué.")
            return False

        return True

    def generate_proof(self, luck):
        nonce = self.calculate_nonce()
        proof = str(luck) + nonce
        proof_encoded = base64.b64encode(proof.encode()).decode()
        print("Preuve générée avec succès.")
        return proof_encoded

    def calculate_nonce(self):
        block_header = "block_header_data"
        nonce = hashlib.sha256(block_header.encode()).hexdigest()
        print("Nonce calculé avec succès.")
        return nonce

    def broadcast_block(self, luck, proof):
        print(f"Diffusion du bloc - Chance (luck): {luck}, Preuve: {proof}")

    def get_monotonic_counter_from_tee(self):
        monotonic_counter = 12345
        print("Compteur monotone récupéré avec succès.")
        return monotonic_counter

    def verify_block(self, block_data, delegated_vote):
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

    def generate_transaction(self, sender, receiver, amount):
        transaction = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        }
        print("Transaction générée avec succès.")
        return transaction

    def sign_transaction(self, transaction_data, sk):
        T = str(transaction_data).encode()
        signature = Dilithium2.sign(self.private_key, T)
        print("Transaction signée avec succès.")
        return signature

    def get_transaction_size(self, transaction_data):
        sender = transaction_data['sender']
        receiver = transaction_data['receiver']
        amount = str(transaction_data['amount'])
        transaction_data_string = f"{sender}{receiver}{amount}"
        return len(transaction_data_string.encode())

    def verify_transaction(self, transaction_data, signature, pk):
        T = str(transaction_data).encode()
        result = Dilithium2.verify(self.public_key, T, signature)
        return result
