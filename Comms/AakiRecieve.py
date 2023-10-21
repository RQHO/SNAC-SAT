import serial
import gzip
from PIL import Image
from rscode import RSCodec

def decompress_image(filename, output_filename):
    with gzip.open(filename, 'rb') as file:
        data = file.read()
    image = Image.frombytes("P", (1, 1), data)  # createing a temporary image object
    image.save(output_filename)

def receive_data(filename, port='/dev/tty0', baud_rate=9600):
    try:
        ser = serial.Serial(port, baud_rate)
        received_data = ser.read_all()

        # Reed-Solomon decoding
        rs = RSCodec(4)  # parameter is number of error correction symbols used by RS encoder
        try:
            decoded_data = rs.decode(received_data)

            # decompression
            decompressed_file = "decompressed_image.png"
            with open(decompressed_file, 'wb') as file:
                file.write(decoded_data)

            print(f"Data received and saved to {decompressed_file}!")
        except rs.CodeError as e:
            print(f"Reed-Solomon decoding error: {e}")

        ser.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_to_save = "insert_image_path_here"  # Replace with image save path
    receive_data(file_to_save)
