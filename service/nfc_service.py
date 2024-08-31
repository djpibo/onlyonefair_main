import time

from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardMonitoring import CardMonitor, CardObserver

class PrintObserver(CardObserver):
    def update(self, observable, actions):
        (added_cards, removed_cards) = actions
        for card in added_cards:
            print("+Inserted: ", toHexString(card.atr))
        for card in removed_cards:
            print("-Removed: ", toHexString(card.atr))

class NfcService:
    def __init__(self):
        self.reader = readers()
        self.card_monitor = CardMonitor()
        self.card_observer = PrintObserver()

    def card_reader(self):
        self.card_monitor.addObserver(self.card_observer)
        time.sleep(60 * 60 * 12)
        self.card_monitor.deleteObserver(self.card_observer)

    def nfc_reader(self):
        r = self.reader
        if not r:
            raise RuntimeError("No NFC reader detected.")
        return r[0]

    def nfc_receiver(self):
        reader = self.nfc_reader()
        uid_command = [0xFF, 0xCA, 0x00, 0x00, 0x00]  # Command to get UID
        connection = reader.createConnection()

        while True:
            try:
                connection.connect()
                uid_data, sw1, sw2 = connection.transmit(uid_command)

                if (sw1, sw2) == (0x90, 0x00):
                    uid_hex = toHexString(uid_data)
                    print(f"[log] NFC UID: {uid_hex}")
                    return uid_hex  # Return the UID of the NFC tag
                else:
                    print(f"[error] Failed to read command. SW1: {sw1}, SW2: {sw2}")

            except Exception as e:
                print(f"[error] Exception during NFC tag reading: {e}")

            time.sleep(1)  # for memory full charged