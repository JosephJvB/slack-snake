from db import Records

l = [
    'UMDEYJM1D' # andrewb
    'UDSABB9SL' # adam
    'U158JB91N' # grant-jba
    'UNYD614SV' # marc
    'UCPQU1V60' # mitchell
    'UJM0SM43X' # sujay
    'UD51HSESC' # joe
    'UK8GENM1P' # quentin
    'U7EKZUNGZ' # alexb
    'UMJ4K7HNK' # vladimir
    'UFCSXUJKW' # russeld.baoy
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

def main():
    for i in l:
        n = d[i]
        Records.update(user=n).where(Records.user==i)
        print(n, 'updated')
    print('done')
        # update user = n where user = i

if __name__ == '__main__': main()