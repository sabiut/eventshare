import qrcode


def generate_qr_code(url, save_path="qrcode.png"):
    img = qrcode.make(url)
    img.save(save_path)


if __name__ == "__main__":
    # Replace with the URL for your Django image upload page
    unique_url = "http://localhost:8000/"
    generate_qr_code(unique_url)
