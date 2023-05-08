from music_library import *
from tkinter.filedialog import askopenfilename


def add_ratings(source: str, destination: str) -> None:
    """It adds songs ratings from iTunes library to Rhythmbox library.

    Args:
        source (str): Path to the iTunes library XML file.
        destination (str): Path to the Rhythmbox library XML file.
    """
    print("Copying songs ratings:" + "\n - From\t" + source + "\n - To\t" + destination)
    library = Library([source], language="iTunes")
    file = open(destination, mode="r", encoding="utf-8")
    tree = ElementTree.parse(destination)
    root = tree.getroot()
    counter = {"edited": 0, "added": 0}
    for song in library.songs:
        for index, element in enumerate(root):
            if element.attrib["type"] == "song":
                if (
                    get_property(element, "artist") == song.artist
                    and get_property(element, "album") == song.album
                    and get_property(element, "title") == song.title
                ):
                    if get_property(element, "rating"):
                        set_property(element, "rating", str(song.rating))
                        counter["edited"] += 1
                    else:
                        ElementTree.SubElement(root[index], "rating").text = str(
                            song.rating
                        )
                        counter["added"] += 1
                    break
    tree.write(destination)
    file.close()
    # Console output
    total = 0
    for action in counter:
        total += counter[action]
    print("Successfully set ratings to " + str(total) + " song(s):")
    for action in counter:
        print(" - " + str(counter[action]) + " song(s) were " + action + ".")


def get_property(xml: ElementTree, key: str) -> ElementTree:
    """It returns the value of a XML tag inside of another XML tag.

    Args:
        xml (ElementTree): Parent XML tag.
        key (str): Children XML tag key.

    Returns:
        ElementTree: Value of the children XML tag.
    """
    if xml.find(key) is not None:
        return xml.find(key).text


def set_property(xml: ElementTree, key: str, value: str) -> None:
    """It sets the value of a XML tag inside of another XML tag.

    Args:
        xml (ElementTree): Parent XML tag.
        key (str): Children XML tag key.
        value (str): Value of the children XML tag.
    """
    if xml.find(key) is not None:
        xml.find(key).text = value


# Main
source = askopenfilename(
    title="Select the source iTunes library XML file",
    filetypes=[("XML File", "*.xml")],
)
if source != "":
    destination = askopenfilename(
        title="Select the destination Rhythmbox library XML file",
        filetypes=[("XML File", "*.xml")],
    )
    if destination != "":
        add_ratings(source, destination)
