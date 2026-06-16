import unittest
import os
from wallet import (
    Wallet,
    TransactionLogger,
    InvalidAmountError,
    InsufficientBalanceError,
)


class TestWallet(unittest.TestCase):
    """Unit test cases for the Wallet application."""

    def setUp(self):
        """Set up a fresh wallet and logger instance before each test."""
        
        self.test_log_file = "test_momo_transactions.log"
        self.logger = TransactionLogger(self.test_log_file)
        self.wallet = Wallet(self.logger)

    def tearDown(self):
        """Clean up test log files after execution."""
        if os.path.exists(self.test_log_file):
            # Clear file content for the next test
            open(self.test_log_file, "w").close()

    def test_deposit_success(self):
        """Test if a valid deposit increases the wallet balance correctly."""
        self.wallet.deposit(500000)
        self.assertEqual(self.wallet.balance, 500000)

    def test_transfer_insufficient_balance(self):
        """Test if transferring more than current balance raises an error."""
        self.wallet.deposit(300000)

        with self.assertRaises(InsufficientBalanceError):
            self.wallet.transfer(500000, "0987654321")

    def test_invalid_amount(self):
        """Test if depositing a negative amount raises an error."""
        with self.assertRaises(InvalidAmountError):
            self.wallet.deposit(-100000)


if __name__ == "__main__":
    unittest.main()
