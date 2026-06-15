import logging


logging.basicConfig(
    filename='momo_transactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
balance = 0


def deposit(amount):
    global balance
    if amount <= 0:
        logging.error(f"InvalidAmountError: Attempted to process (amount) VND.")
        raise ValueError("Số tiền giao dịch phải lớn 0.")
    balance += amount
    logging.info(f"Deposit successful: +{amount} VND. Current Balance : {balance}")
    return balance


def transfer(amount, phone):
    """Xử lý chuyển tiền"""
    global balance
    if amount <= 0:
        logging.error(f"InvalidAmountError:Attempted to process {amount} VND.")
        raise ValueError("Số tiền giao dịch phải lớn 0.")
    if amount > balance:
        logging.error(
            f"InsufficientBalanceError: Attempted to transfer "
            f"{amount} VND with balance {balance} VND."
        )
        raise ValueError("Số dư của bạn không đủ.")
    balance -= amount 
    if amount >= 10000000:
        logging.waring(f"High value transaction detected: {amount} VND to {phone}")
        logging.info(
            f"Transfer successful: -{amount} VND to {phone}. "
            f"Current Balance: {balance}"
        )
    return balance


def main():
    """Hàm chạy vòng lặp chính của chương trình"""
    global balance
    while True:
        print("\n ====== VÍ MOMO GIẢ LẬP ========")
        print("1.Nạp tiền vào ví")
        print("2.Chuyển tiền")
        print("3.Xem số dư")
        print("4.Thoát chương trình")
        choice = input("Nhập lựa chọn chức năng (1-4):").strip()

        try:
            if choice == "1":
                amount = int(input("Nhập số tiền cần nạp :"))
                deposit(amount)
                print(f"Nạp thành công: +{amount:,} VND")
            elif choice == "2":
                phone = input("Nhập SĐT người nhận :")
                amount = int(input("Nhập số tiền cần chuyển :"))
                transfer(amount, phone)
                print(f"Chuyển thành công tới {phone}. Số dư : {balance:,} VND")
            elif choice == "3":
                print(f"Số dư hiện tại : {balance:,}VND")
                logging.info(f"Balance checked.Current Balance : {balance}")
            elif choice == "4":
                logging.info("Kết thúc")
                print("Tạm biệt")
                break
        except ValueError:
            print("Lỗi : Vui lòng nhập số tiền hợp lệ (số nguyên).")


if __name__ == "__main__":
    main()
