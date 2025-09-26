# metadata_extraction.py
from PyPDF2 import PdfReader
import os
import zipfile
import xml.dom.minidom

# Set the location of output file to the current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class metadataExtractor:
    def extract_metadata(self) -> None:
        # Extract metadata for PDF file.
        pdf_file = os.path.join(__location__, 'Totally_Safe_File.pdf')
        if os.path.exists(pdf_file):
            pdf_reader = PdfReader(pdf_file)
            print('\nMetadata for PDF file: ', pdf_reader.metadata)
            print('\nCheck if PDF file encrypted:', pdf_reader.is_encrypted)
        else:
            print(f'[SKIP] PDF not found at: {pdf_file}')

        # Extract metadata for Word file.
        docx_file = os.path.join(__location__, 'Totally_Safe_File.docx')
        if os.path.exists(docx_file):
            word_document = zipfile.ZipFile(docx_file)
            # document.extractall() will extract the entire Word document into its components including various XML files.
            word_extraction_path = os.path.join(__location__, 'Totally_Safe_File_word')
            word_document.extractall(word_extraction_path)
            xml_dom = xml.dom.minidom.parse(os.path.join(word_extraction_path, 'docProps', 'core.xml'))
            print('\n\nMetadata for Word file: ', xml_dom.toprettyxml())
        else:
            print(f'[SKIP] Word file not found at: {docx_file}')

        # Extract metadata for Excel file.
        xlsx_file = os.path.join(__location__, 'Totally_Safe_File.xlsx')
        if os.path.exists(xlsx_file):
            excel_document = zipfile.ZipFile(xlsx_file)
            # document.extractall() will extract the entire Excel workbook into its components including various XML files.
            excel_extraction_path = os.path.join(__location__, 'Totally_Safe_File_excel')
            excel_document.extractall(excel_extraction_path)
            xml_dom = xml.dom.minidom.parse(os.path.join(excel_extraction_path, 'docProps', 'core.xml'))
            print('\n\nMetadata for Excel file: ', xml_dom.toprettyxml())
        else:
            print(f'[SKIP] Excel file not found at: {xlsx_file}')

        # Extract metadata for PowerPoint file.
        pptx_file = os.path.join(__location__, 'Totally_Safe_File.pptx')
        if os.path.exists(pptx_file):
            ppt_document = zipfile.ZipFile(pptx_file)
            # document.extractall() will extract the entire PowerPoint deck into its components including various XML files.
            ppt_extraction_path = os.path.join(__location__, 'Totally_Safe_File_ppt')
            ppt_document.extractall(ppt_extraction_path)
            xml_dom = xml.dom.minidom.parse(os.path.join(ppt_extraction_path, 'docProps', 'core.xml'))
            print('\n\nMetadata for PowerPoint file: ', xml_dom.toprettyxml())
        else:
            print(f'[SKIP] PowerPoint file not found at: {pptx_file}')

if __name__ == '__main__':
    extractor = metadataExtractor()
    extractor.extract_metadata()
#In this code I included a checking method to check if the file exists in different formats and if it doesn't it skips it
# I did this because I tried the first code in the book and I had errors because the file was only in pdf and the code
#could not find any other formats of the file so it was throwing errors.
