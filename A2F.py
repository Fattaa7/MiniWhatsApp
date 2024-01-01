import re

def is_arabic(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\s]+')  # Range for Arabic Unicode characters

    return bool(arabic_pattern.search(text))

def convert_to_arabic_franco(text):
    # Define mapping of Arabic characters to their Franco-Arabic counterparts
    arabic_to_franco_mapping = {
        'ا': 'a',
        'أ': 'a',
        'آ': 'a',
        'إ': 'e',
        'ئ': '2',
        'ب': 'b',
        'ت': 't',
        'ث': 'th',
        'ج': 'g',
        'ح': '7',
        'خ': '5',
        'د': 'd',
        'ذ': 'z',
        'ر': 'r',
        'ز': 'z',
        'س': 's',
        'ش': 'sh',
        'ص': 's',
        'ض': 'd',
        'ط': 't',
        'ظ': 'z',
        'ع': '3',
        'غ': '8',
        'ف': 'f',
        'ق': 'q',
        'ك': 'k',
        'ل': 'l',
        'م': 'm',
        'ن': 'n',
        'ه': 'h',
        'و': 'w',
        'ي': 'y',
        'ة': 'a',
        'ء': '2',
        '؟': '?',
        'ڤ': 'v',
    }

    # Convert the input text to Arabic Franco
    converted_text = ''
    for char in text:
        converted_text += arabic_to_franco_mapping.get(char, char)

    return converted_text

def check_and_convert_to_franco(text):
    textawy = text
    if is_arabic(textawy):
        textawy = convert_to_arabic_franco(textawy)
    
    return textawy
    