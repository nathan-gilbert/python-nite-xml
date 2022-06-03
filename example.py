import sys
from nitexml.nitexml import NiteXML

if __name__ == "__main__":

    nite = NiteXML(sys.argv[1])

    # cross reference Words by DialogueActs annotations
    nite.get_attribute_text_from_collection("DialogueActs", "Words", "s.x")
