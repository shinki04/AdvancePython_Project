import bcrypt

# Mã hóa mật khẩu
def hash_password(password):
    salt = bcrypt.gensalt()  # Tạo salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # Băm mật khẩu
    return hashed

# Kiểm tra mật khẩu
def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

# Test mã hóa và kiểm tra
if __name__ == "__main__":
    # Mật khẩu gốc
    original_password = "secure_password123"
    
    # Mã hóa mật khẩu
    hashed_password = hash_password(original_password)
    print(f"Mật khẩu gốc: {original_password}")
    print(f"Mật khẩu đã băm: {hashed_password.decode('utf-8')}")  # In ra dạng chuỗi để dễ đọc

    # Kiểm tra mật khẩu đúng
    is_valid = check_password("secure_password123", hashed_password)
    print(f"Kiểm tra mật khẩu đúng: {'Thành công' if is_valid else 'Thất bại'}")

    # Kiểm tra mật khẩu sai
    is_valid = check_password("wrong_password", hashed_password)
    print(f"Kiểm tra mật khẩu sai: {'Thành công' if is_valid else 'Thất bại'}")
