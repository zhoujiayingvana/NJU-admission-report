import base64


def convert2base64(input_path, output_path):
    with open(input_path, 'rb') as f_reader:
        with open(output_path, 'wb+') as f_writer:
            im = f_reader.read()
            b64 = base64.b64encode(im)
            print(b64)
            f_writer.write(b64)


if __name__ == '__main__':
    i_path = './for_test/01.png'
    o_path = './for_test/output.txt'
    convert2base64(i_path, o_path)
