from setuptools import setup, find_packages

PACKAGE_NAME = "enigma"
DESCRIPTION = "A Ciphertext Module"
VERSION = "1.0.0"
AUTHOR = "Tebee_Sunaookami"
AUTHOR_EMAIL = "tebeebmgo@gmail.com"
URL = "https://github.com/TebeeDeveloper/_Python_Community_"

REQUIRED_PACKAGES = ['enigma']

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=open('README.md').read(), # Đọc nội dung từ README.md
    long_description_content_type='text/markdown',
    url=URL,
    
    # find_packages() là một cách Clean Code để tự động tìm tất cả các 
    # thư mục chứa package (thư mục có chứa __init__.py)
    packages=find_packages(),
    
    # Dependencies (Phụ thuộc)
    install_requires=REQUIRED_PACKAGES,
    
    # Cấu hình classifier giúp PyPI hoặc người dùng biết package này dùng cho gì
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        # Chọn phiên bản Python mà cậu hỗ trợ:
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8', # Phiên bản Python tối thiểu
)