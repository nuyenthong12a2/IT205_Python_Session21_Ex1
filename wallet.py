import logging


class InvalidAmountError(Exception):
    """Exception raised for invalid transaction amounts (<= 0)."""
    pass


class InsufficientBalanceError(Exception):
    """Exception raised when transfer amount exceeds current balance."""
    pass


class TransactionLogger:
    """Handles logging operations for wallet transactions."""
    
    def __init__(self, log_file: str = 'momo_transactions.log'):
        """Initializes the logger with file handler and specific formatting."""
        self.logger = logging.getLogger('MoMoLogger')
        self.logger.setLevel(logging.INFO)
        
      
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_info(self, message: str):
        """Logs an informational message."""
        self.logger.info(message)

    def log_warning(self, message: str):
        """Logs a warning message."""
        self.logger.warning(message)

    def log_error(self, message: str):
        """Logs an error message."""
        self.logger.error(message)


class Wallet:
    """Represents a MoMo user wallet with deposit and transfer capabilities."""
    
    def __init__(self, logger: TransactionLogger):
        """Initializes a new wallet with 0 balance and a logger instance."""
        self.balance = 0
        self.logger = logger

    def deposit(self, amount: int):
        """
        Deposits money into the wallet.
        
        Raises:
            InvalidAmountError: If the deposit amount is <= 0.
        """
        if amount <= 0:
            self.logger.log_error(
                f"InvalidAmountError: Attempted to process {amount} VND."
            )
            raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")
        
        self.balance += amount
        self.logger.log_info(
            f"Deposit successful: +{amount} VND. "
            f"Current Balance: {self.balance}"
        )

    def transfer(self, amount: int, phone: str):
        """
        Transfers money to a specific phone number.
        
        Raises:
            InvalidAmountError: If the transfer amount is <= 0.
            InsufficientBalanceError: If the transfer amount exceeds balance.
        """
        if amount <= 0:
            self.logger.log_error(
                f"InvalidAmountError: Attempted to process {amount} VND."
            )
            raise InvalidAmountError("Số tiền giao dịch phải lớn hơn 0.")
        
        if amount > self.balance:
            self.logger.log_error(
                f"InsufficientBalanceError: Attempted to transfer "
                f"{amount} VND with balance {self.balance} VND."
            )
            raise InsufficientBalanceError(
                "Giao dịch thất bại: Số dư của bạn không đủ."
            )
        
        self.balance -= amount
        
        # High-value transaction warning
        if amount >= 10000000:
            self.logger.log_warning(
                f"High value transaction detected: {amount} VND to {phone}"
            )
            
        self.logger.log_info(
            f"Transfer successful: -{amount} VND to {phone}. "
            f"Current Balance: {self.balance}"
        )


def display_menu():
    """Displays the main CLI menu."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("=======================================")


def main():
    """Main execution block for the MoMo Wallet Simulator."""
    logger = TransactionLogger()
    wallet = Wallet(logger)
    
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-4): ").strip()
        
        if choice == "1":
            print("\n--- NẠP TIỀN VÀO VÍ ---")
            try:
                amount = int(input("Nhập số tiền cần nạp: "))
                wallet.deposit(amount)
                print(f"\nNạp tiền thành công: +{amount:,} VND")
                print(f"Số dư hiện tại: {wallet.balance:,} VND")
            except ValueError:
                logger.log_error(
                    "ValueError: Invalid numeric input for deposit."
                )
                print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
            except InvalidAmountError as e:
                print(f"\nLỗi: {e}")
                
        elif choice == "2":
            print("\n--- CHUYỂN TIỀN ---")
            phone = input("Nhập số điện thoại người nhận: ").strip()
            try:
                amount = int(input("Nhập số tiền cần chuyển: "))
                wallet.transfer(amount, phone)
                print(f"\nChuyển tiền thành công tới số điện thoại {phone}.")
                print(f"Số tiền đã chuyển: {amount:,} VND")
                print(f"Số dư còn lại: {wallet.balance:,} VND")
            except ValueError:
                logger.log_error(
                    "ValueError: Invalid numeric input for transfer."
                )
                print("\nLỗi: Vui lòng nhập số tiền hợp lệ.")
            except (InvalidAmountError, InsufficientBalanceError) as e:
                print(f"\n{e}")
                
        elif choice == "3":
            print("\n--- SỐ DƯ VÍ MOMO ---")
            print(f"Số dư hiện tại: {wallet.balance:,} VND")
            logger.log_info(
                f"Balance checked. Current Balance: {wallet.balance}"
            )
            
        elif choice == "4":
            print("\nCảm ơn bạn đã sử dụng dịch vụ")
            logger.log_info("System shutdown")
            break
        else:
            print("\nLựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 4.")


if __name__ == "__main__":
    main()