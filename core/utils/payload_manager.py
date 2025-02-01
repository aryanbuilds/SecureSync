import os

class PayloadManager:
    @staticmethod
    def load_payloads(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

class PayloadFactory:
    def __init__(self):
        self.payloads = {}

    def get_payloads(self, attack_type):
        if attack_type not in self.payloads:
            file_path = f'wordlists/{attack_type}.txt'
            self.payloads[attack_type] = PayloadManager.load_payloads(file_path)
        return self.payloads[attack_type]