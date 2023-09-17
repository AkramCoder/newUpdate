# import spacy
# import docx2txt
# import PyPDF2

# pdf_file_path = './cv1.pdf'

# def get_text_pdf(path):
#     pdf_file = open(path, 'rb')
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ''

#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text()

#     pdf_file.close()

#     return text

# def get_text_word(path):
#     return docx2txt.process(path)

import pickle
import spacy
import time
import re

def find_indices_of_starting_0(text):
    # Regular expression pattern to match '0' at the beginning of words
    pattern = r'\b0'

    # Find all matches in the text
    matches = re.finditer(pattern, text)

    # Get the indices of the matches
    indices = [match.start() for match in matches]

    return indices

def find_phone(text, indice):
    i = indice
    result = '0'
    while len(result) < 10:
        while text[i+1] in (' ', '/', '-', '.'):
            i += 1
        try:
            int(text[i+1])
            result = result + text[i+1]
            i += 1
        except:
            return
    
    return result

def find_email(text):
    email_pattern = r'@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}'

    email_domains = re.findall(email_pattern, text)
    emails = []
    for domain in email_domains:
        index = text.index(domain)
        words_before = text[:index].split()
        username = words_before[-1]
        result = username+domain
        emails.append(result)

    return emails
    
            
    
       



nlp = spacy.load('C:\\Users\\XPS\\Downloads\\lapem_manager_app-main-master (1)\\lapem_manager_app-main-master\\backend_\\user\\myModel')
# newText = ''' Bac scientifique (2017).  Lycée elkerma eldjadida.  Licence LMD en Génie des Procédés.   Université des sciences et de la technologie MB (Usto). Faculté De Chimie .2017/2020  Master 2éme année en Génie des procédés de l’environnement   Université des sciences et de la technologie MB (Usto).             	Faculté De Chimie . 2021/2022	 Certificat de secourisme. L’entraineur : Taibi Hichem (international coach). 16 Juillet 2022 
# COMPETENCES 	                                                                                                                                         Permi de conduire catégorie B. Compétences liees à l’emploi  Travailler dans un cadre dynamique où je pourrais développer et mettre En œuvre mes capacités, mes connaissances et mon savoir-faire. Persévérance, Autonomie, capacité d’adaptation, sens de l’organisation, esprit d’équipe.  Compétences informatiques  Outils: Maîtrise des logiciels de bureautique (Word, Excel,…..).  Autres 6mois vendeur dans une supérette. 6mois caissier dans une supérette. 5mois caissier dans une cosmétique.  3 semaine stage au niveau de complexe GP2/Z (sonatrach) 2 semaine stage au niveau de complexe GL2/Z (sonatarch)  EXPÉRIENCE PROFESSIONNELLE 	Zouaimia Oualid Né le 22 mars 1998. á Ouargla Nationalité : Algérienne. célibataire.     FORMATION 
# Arabe : Langue maternelle  Français : très bien parlé et écrire Anglais : Moyen 	LANGUES 06 58 12 97 59 // 07 95 48 33 31    zouaimiaoualid@gmail.com  Cité 100 logts bloc B3 N: 03, el kerma , Oran , Algérie      CONTACT 
# Sport, Cultures générale, Actualités (Nouvelles technologies, Energies propres, Environnement…). 	CENTRES D’INTÉRÊT '''

def get_data_type(text):
    try: 
        
        text = " ".join(text.split())
        text = text.replace('\n', " ")
        print(text)
        
        indices = find_indices_of_starting_0(text)
        print("phone_number--->",indices)

        phone_numbers = []
        for indice in indices:
            r = find_phone(text, indice)
            if r:
                phone_numbers.append(r)

        print(phone_numbers)
        print(find_email(text))

        doc = nlp(text)
        result = []
        for ent in doc.ents:
            data = {
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            }
            result.append(data)

        return result
    except Exception as e:
        print("Error:", str(e))
        return []