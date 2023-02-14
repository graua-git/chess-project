properties = {
            'castle': False,
            'check': False,
            'takes': False,
            'promotion': False
        }

def set_properties(**kwargs):
    for key, value in kwargs.items():
        properties[key] = value
    
set_properties(check=True, takes=True)

print(properties)
