from db import Records

l = [
    'UMDEYJM1D', # andrewb
    'UDSABB9SL', # adam
    'U158JB91N', # grant-jba
    'UNYD614SV', # marc
    'UCPQU1V60', # mitchell
    'UJM0SM43X', # sujay
    'UD51HSESC', # joe
    'UK8GENM1P', # quentin
    'U7EKZUNGZ', # alexb
    'UMJ4K7HNK', # vladimir
    'UFCSXUJKW', # russeld.baoy
]
d = {
    'UMDEYJM1D': 'andrewb',
    'UDSABB9SL': 'adam',
    'U158JB91N': 'grant-jba',
    'UNYD614SV': 'marc',
    'UCPQU1V60': 'mitchell',
    'UJM0SM43X': 'sujay',
    'UD51HSESC': 'joe',
    'UK8GENM1P': 'quentin',
    'U7EKZUNGZ': 'alexb',
    'UMJ4K7HNK': 'vladimir',
    'UFCSXUJKW': 'russeld.baoy',
}
l2 = [
    'andrewb',
    'adam',
    'grant-jba',
    'marc',
    'mitchell',
    'sujay',
    'joe',
    'quentin',
    'alexb',
    'vladimir',
    'russeld.baoy',
]
d2 = {
    'andrewb': 'UMDEYJM1D',
    'adam': 'UDSABB9SL',
    'grant-jba': 'U158JB91N',
    'marc': 'UNYD614SV',
    'mitchell': 'UCPQU1V60',
    'sujay': 'UJM0SM43X',
    'joe': 'UD51HSESC',
    'quentin': 'UK8GENM1P',
    'alexb': 'U7EKZUNGZ',
    'vladimir': 'UMJ4K7HNK',
    'russeld.baoy': 'UFCSXUJKW',
}

def main():
    for i in l:
        n = d[i]
        q = Records.update(user=n).where(Records.user==i)
        q.execute()
        print(n, 'updated')
    print('done')
        # update user = n where user = i

if __name__ == '__main__': main()