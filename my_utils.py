import PyPDF2
import io
def read_file(file_bytes):
    # try:
        # with open(file_bytes, 'rb') as file:
        with io.BytesIO(file_bytes) as open_pdf_file:
            pdf_reader = PyPDF2.PdfReader(open_pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text
    # except Exception as e:
    #     with open(file_path, 'r') as file:
    #         return file.read()
    # except Exception as e:
    #     print("File format not supported")
    #     raise Exception("File format not supported")

def write_to_txt(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def read_file_and_write_to_txt(file_bytes, file_path_write):
    content = read_file(file_bytes)
    write_to_txt(file_path_write, content)