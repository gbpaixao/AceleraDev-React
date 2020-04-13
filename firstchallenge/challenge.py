import json
import requests
import hashlib

def decrypt(crypted, step):
    decrypted = ''
    
    for letter in crypted:
        letter_code = ord(letter)
        
        if ord(letter) >= (97+step) and ord(letter) <= 122:
            letter_code -= step
        elif ord(letter) >= 97 and ord(letter) < (97+step):
            letter_code = letter_code - step + 26 # 122 - (97 - (ord(letter) - step)) + 1

        letter = chr(letter_code)
        decrypted = decrypted + letter

    return decrypted

def main():
    # Get json from codenation's api
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=a3e9b70a5022e52c4450ada5aa626f5d592da21c'
    answer_dic = requests.get(url).json()

    # write req to a file in pretty-printed
    file = open('answer.json', 'w')
    file.write(json.dumps(answer_dic, indent=4))
    file.close()

    # get parameters
    crypted, step = answer_dic['cifrado'], answer_dic['numero_casas']

    # decrypt message
    answer_dic['decifrado'] = decrypt(crypted, step)

    # sha1 enconding 
    answer_dic['resumo_criptografico'] = hashlib.sha1(answer_dic['decifrado'].encode()).hexdigest()
    
    # write output to a file in pretty-printed
    file = open('answer.json', 'w')
    file.write(json.dumps(answer_dic, indent=4))
    file.close()

    # send to codenation's api
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=a3e9b70a5022e52c4450ada5aa626f5d592da21c'
    files = {'answer': open('answer.json', 'rb')}
    r = requests.post(url, files=files)
    print(r.text)
main()
