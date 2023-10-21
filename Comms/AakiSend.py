### Send With Reed-Solomon and 8-bit compression 


import serial
import gzip
from PIL import Image
from rscode import RSCodec

def compress_image(filename, output_filename):
    image = Image.open(filename)
    image = image.convert("P", palette=Image.ADAPTIVE, colors=256)
    image.save(output_filename)

def send_data(filename, port='/dev/tty0', baud_rate=9600):
    try:
        ser = serial.Serial(port, baud_rate)

        # Compression
        compressed = "compressed_image.gz"
        compress_image(filename, compressed)

        with open(compressed_file, 'rb') as file:
            data = file.read()

        # reed-Solomon encoding
        rs = RSCodec(4)  # parameter is num of error-correction symbols to use
        encoded_data = rs.encode(data)

        ser.write(encoded_data)
        ser.close()
        print(f"Data sent successfully from {filename}!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_to_send = "insert_image_path_here"  # change to image to send's file path
    send_data(file_to_send)
