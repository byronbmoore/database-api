from functools import wraps



def sanitize(f):
    ''' Sanitize various input strings '''

    @wraps(f)
    def inner(*args, **kwargs):

        ''' Part of speech ambiguity - singular or plural?
        capture input, remove 's' making either work '''
        if 'part_of_speech' in kwargs:
            if kwargs['part_of_speech'][-1] == 's':
                kwargs['part_of_speech'] = kwargs['part_of_speech'][:-1]
        if 'limit' in kwargs:
            print('limit')
            kwargs['limit'] = int(kwargs['limit'])
            

        return f(*args, **kwargs)
    return inner 
