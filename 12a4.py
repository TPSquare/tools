import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

dir = "D:\\Documents\\Kỉ yếu\\Nộp tiền\\560k"

namelist = [
    "Nguyễn Gia Bảo",
    "Cao Đại Doãn",
    "Nguyễn Công Đạt",
    "Nguyễn Quang Hào",
    "Nguyễn Thị Quý Hân",
    "Hồ Phương Huyền",
    "Nguyễn Gia Hưng",
    "Hồ Duy Khang",
    "Văn Thị Nhã Linh",
    "Lê Yến Loan",
    "Lê Thị Cẩm Ly",
    "Nguyễn Thị Cẩm Ly",
    "Hồ Nguyễn My My",
    "Nguyễn Thị Kiều Ngân",
    "Từ Hoàng Thảo Ngân",
    "Huỳnh Khánh Nguyên",
    "Nguyễn Trung Nguyên",
    "Huỳnh Anh Nhật",
    "Nguyễn Anh Nhật",
    "Lê Nguyễn Ý Nhi",
    "Nguyễn Đỗ Tố Như",
    "Thái Thị Quỳnh Như",
    "Huỳnh Ngọc Ny",
    "Nguyễn Thị Kiều Oanh",
    "Thái Phan Thanh Phú",
    "Võ Tạ Anh Quốc",
    "Đặng Thị Thúy Quỳnh",
    "Thái Đặng Như Quỳnh",
    "Trần Duy Sơn",
    "Trịnh Gia Thi",
    "Phan Ngọc Thiện",
    "Ngô Thị Thanh Thúy",
    "Hồ Hà Trâm",
    "Nguyễn Ngọc Bảo Trâm",
    "Nguyễn Ngọc Bảo Trân",
    "Nguyễn Trần Quế Trân",
    "Nguyễn Thị Thúy Trinh",
    "Nguyễn Thành Vũ",
    "Nguyễn Xuân Vũ",
    "Thái Thanh Vũ",
    "Phan Tường Vy",
    "Nguyễn Chí Vỹ",
    "Trần Phạm Gia Vỹ",
    "Nguyễn Nhật Ý",
]

for filename in os.listdir(dir):
    filename = filename[0:filename.rfind(".")]
    if filename in namelist:
        namelist.remove(filename)
    else:
        print(f"File {filename} không có trong danh sách.")

print("\n".join(namelist))
