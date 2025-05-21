import time
import os
from PyPDF2 import PdfWriter, PdfReader


OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def merge_pdfs():
    merger = PdfWriter()
    pdfs = []

    try:
        n = int(input("Enter the number of Pdfs to merge: "))
    except ValueError:
        print("Invalid number entered.")
        return


    for i in range(0, n):
        name = input(f"Enter the name of the pdf {i + 1} (with extension): ")
        if not os.path.exists(name):
            print(f"File '{name}' does not exist. Skipping this file.")
            continue
        pdfs.append(name)

    if not pdfs:
        print(" No valid PDFs to merge.")
        return
    
    for pdf in pdfs:
        try:
            merger.append(pdf)
        except Exception as e:
            print(f"Failed to add '{pdf}': {e}")

    # Generate a unique filename using timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    merged_filename = os.path.join(OUTPUT_DIR, f"merged-{timestamp}.pdf")

    try:
        merger.write(merged_filename)
        merger.close()
        print(f"PDFs merged successfully into '{merged_filename}'.")
    except Exception as e:
        print(f"Failed to write merged PDF: {e}")


def encrypt_pdf():
    name_pdf = input("Enter the name of the Pdf to encrypt (with extention): ")
    if not os.path.exists(name_pdf):
        print(f"File '{name_pdf}' does not exist.")
        return
    
    password = input("Enter the password to encrypt the PDF: ")

    try:
        reader = PdfReader(name_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        output_file = os.path.join(OUTPUT_DIR, "encrypted-" + name_pdf)
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Encrypted PDF saved as '{output_file}'.")
    except Exception as e:
        print(f"Failed to encrypt PDF: {e}")


def decrypt_pdf():
    name_pdf = input("Enter the name of the PDF to decrypt (with extension): ")
    if not os.path.exists(name_pdf):
        print(f"File '{name_pdf}' does not exists.")
        return
    
    password = input("Enter the password to decrypt the PDF: ")

    try:
        reader = PdfReader(name_pdf)
        if not reader.is_encrypted:
            print("This PDF is not encrypted.")
            return

        if not reader.decrypt(password):
            print("Incorrect password. Could not decrypt the PDF.")
            return

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_file = os.path.join(OUTPUT_DIR, "decrypted-" + name_pdf)
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Decrypted PDF saved as '{output_file}'.")
    except Exception as e:
        print(f"Failed to decrypt PDF: {e}")


def main():
    while True:
        print("\n PDF Tool Options:")
        print("1. Merge PDFs")
        print("2. Encrypt a PDF")
        print("3. Decrypt a PDF")
        print("4. Exit")

        choice = input ("Enter your choice (1/2/3/4): ")

        match choice:
            case "1":
                merge_pdfs()
            case "2":
                encrypt_pdf()
            case "3":
                decrypt_pdf()
            case "4":
                print("Thankyou for using the tool")
                break
            case default:
                print("Invalid choice, Please enter 1, 2, 3, or 4")

if __name__ == "__main__":
    main()