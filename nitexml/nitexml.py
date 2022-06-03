import xml.etree.ElementTree as ET
import os
import re


class NiteXML:

    def __init__(self, collection_base_directory: str):
        self.__base_dir = collection_base_directory
        self.__prefix_match = re.compile(r"([^\.]*\.[^\.])\.*")
        self.__id_match = re.compile(r"\((.*?)\)")

    @staticmethod
    def parse_file(input_filename: str):
        tree = ET.parse(input_filename)
        return tree.getroot()

    @staticmethod
    def find_children_attributes(root, attribute: str):
        attribute_nodes = []
        for child in root:
            if child.attrib.get('type', '') == attribute:
                for grandchild in child:
                    attribute_nodes.append(grandchild)
        return attribute_nodes

    def get_attribute_text_from_collection(self,
                                           annotation1: str,
                                           annotation2: str,
                                           attribute: str):

        word_files = os.listdir(f"{self.__base_dir}{os.sep}{annotation2}")
        for file in os.listdir(f"{self.__base_dir}{os.sep}{annotation1}"):
            file_pwd = f"{self.__base_dir}{os.sep}{annotation1}{os.sep}{file}"
            file_root = self.parse_file(file_pwd)
            attribute_nodes = self.find_children_attributes(file_root,
                                                            attribute)

            for attr in attribute_nodes:
                href = attr.get('href', '')
                ids = re.findall(self.__id_match, href)

                if ids is not None:
                    start_id = ids[0]
                    end_id = ids[1]

                    # get the words for this attribute
                    file_prefix_search = re.search(self.__prefix_match, file)
                    if file_prefix_search is not None:
                        file_prefix = file_prefix_search.group(0)
                        wf = ''.join(list(filter(lambda x: x.startswith(
                            file_prefix), word_files)))
                        wf_file_pwd = f"{self.__base_dir}{os.sep}" \
                                      f"{annotation2}{os.sep}{wf}"
                        wf_root = self.parse_file(wf_file_pwd)
                        in_span = False
                        final_text = []
                        for child in wf_root:
                            if child.attrib.get('{http://nite.sourceforge.net/}id', '') == start_id:
                                in_span = True
                            if in_span:
                                #print(f"Tag:{child.tag}, Attrib
                                # :{child.attrib}, Text:{child.text}")
                                if child.text is not None:
                                    final_text.append(str(child.text))
                            if child.attrib.get('{http://nite.sourceforge.net/}id', '') == end_id:
                                in_span = False
                        print(' '.join(final_text))
