from abc import ABC, abstractmethod


class BackendBase(ABC):
    UNCONFIRMED_ADDRESS_BALANCE = 0
    CONFIRMED_ADDRESS_BALANCE = 1
    UNDERPAID_ADDRESS_BALANCE = -1
    NO_HASH_ADDRESS_BALANCE = -2

    @abstractmethod
    def __init__(self, public_key, strict=False):
        self.public_key = public_key
        self.strict_mode = strict

    @abstractmethod
    def convert_from_fiat(self, amount, currency="USD"):
        """
        Convert a fiat amount to coin amount
        :param amount: Fiat amount to convert
        :param currency: Fiat currency
        :return: Rounded coin amount
        """

    @abstractmethod
    def convert_to_fiat(self, amount, currency):
        """
        Convert a coin amount to fiat amount
        :param amount: coin amount to convert
        :param currency: Fiat currency to convert
        :return: Amount in specified currency
        """

    @abstractmethod
    def create_payment_uri(self, address, total_crypto_amount):
        """
        Create payment URI for a particular address and amount
        e.g. ethereum:0x123455?value=122334

        Args:
            total_crypto_amount (float): amount in crypto currency
            address (str): address of receiver
        """
    
    @abstractmethod
    def generate_new_address(self, index, address_type="p2wpkh", derivation_path="m/0"):
        """
        Generate new coin address from a hd public master key based on a particlar index
        Address can be generated sequentially like in the case of electrum
        :param index: Index to use to generate address
        :param address_type: Address type to generate
        :return: Generated address
        """

    @abstractmethod
    def confirm_address_payment(
        self,
        address,
        total_crypto_amount,
        confirmation_number=1,
        accept_confirmed_bal_without_hash_mins=20,
        tx_hash=None,
    ):
        """
        Confirm if a payment was made to a specified address.
        A payment that was already confirmed on the blockchain before running
        this tool can still be seen as paid by specifying a time
        frame such payment was confirmed and the time this tool is used on accept_confirmed_bal_without_hash_mins.
        :param address: Address to check for payment
        :param total_crypto_amount: Amount to check
        :param accept_confirmed_bal_without_hash_mins : You can accept already confirmed payment within this minute
         if there is no previous hash provided
        :param tx_hash: Transaction hash if any can be gotten from this method if payment is unconfirmed
        :param confirmation_number: Block chain confirmations below this are returned as unconfirmed
        :return: UNCONFIRMED_ADDRESS_BALANCE, traansaction hash | CONFIRMED_ADDRESS_BALANCE, payment_amount |
                    UNDERPAID_ADDRESS_BALANCE, remaining_crypto_amount |  NO_HASH_ADDRESS_BALANCE, None
        """
