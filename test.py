string = 'hello""""  , joy, pep,     marsello,   , , ,   haha, jaja , ajsdfs,'
split_string = [x.strip('\'\" ') for x in string.split(',')]
split_string = [x for x in split_string if x]
print split_string