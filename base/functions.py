from collections import defaultdict

def image_field_parser(querydict):
    parsed_data = defaultdict(lambda: defaultdict(dict))
    
    for key, value in querydict.lists():
        field, rest = key.split('[', 1)
        index, field = rest.split(']', 1)
        index = int(index)
        field = field.strip('[').strip(']')
        parsed_data[index][field] = value[0] if len(value) == 1 else value
    
    result = {'image': [], 'blogs': []}
    for idx in sorted(parsed_data):
        if 'image' in parsed_data[idx]:
            result['image'].append(dict(parsed_data[idx]))
        elif 'title' in parsed_data[idx]:
            result['blogs'].append(dict(parsed_data[idx]))
    
    return result


def field_parser(query_dict) -> dict:
    parsed_data = {
        'title': query_dict.get('title', '').strip(),
        'credit': query_dict.get('credit', '').strip(),
        'credit_url': query_dict.get('credit_url', '').strip(),
        'image': query_dict.get('image')  # This will be an instance of InMemoryUploadedFile
    }

    return parsed_data

def parse_querydict(querydict):
    parsed_data = {}

    for key, value in querydict.items():
        if '[' in key:
            # Handle nested properties like profile_photo[title]
            main_key, sub_key = key.split('[', 1)
            sub_key = sub_key.rstrip(']')
            if main_key not in parsed_data:
                parsed_data[main_key] = {}
            parsed_data[main_key][sub_key] = value
        else:
            # Handle regular fields and lists
            if isinstance(value, list):
                parsed_data[key] = []
                for item in value:
                    parsed_data[key].append({k.split('[')[0]: v for k, v in item.items()})
            else:
                parsed_data[key] = value

    # Convert scattered official_links to list of dictionaries
    if 'official_links' in parsed_data and isinstance(parsed_data['official_links'], dict):
        official_links = []
        for key, value in parsed_data['official_links'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(official_links) <= index:
                official_links.append({})
            official_links[index][sub_key] = value
        parsed_data['official_links'] = official_links
    
    # Convert scattered photos to list of dictionaries
    if 'photos' in parsed_data and isinstance(parsed_data['photos'], dict):
        photos = []
        for key, value in parsed_data['photos'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(photos) <= index:
                photos.append({})
            photos[index][sub_key] = value
        parsed_data['photos'] = photos
    
    
    # Convert scattered videos to list of dictionaries
    if 'videos' in parsed_data and isinstance(parsed_data['videos'], dict):
        videos = []
        for key, value in parsed_data['videos'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(videos) <= index:
                videos.append({})
            videos[index][sub_key] = value
        parsed_data['videos'] = videos
    
    
    # Convert scattered socials to list of dictionaries
    if 'socials' in parsed_data and isinstance(parsed_data['socials'], dict):
        socials = []
        for key, value in parsed_data['socials'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(socials) <= index:
                socials.append({})
            socials[index][sub_key] = value
        parsed_data['socials'] = socials
    
    
    # Convert scattered blogs to list of dictionaries
    if 'blogs' in parsed_data and isinstance(parsed_data['blogs'], dict):
        blogs = []
        for key, value in parsed_data['blogs'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(blogs) <= index:
                blogs.append({})
            blogs[index][sub_key] = value
        parsed_data['blogs'] = blogs
    
    
    # Convert scattered additional_info to list of dictionaries
    if 'additional_info' in parsed_data and isinstance(parsed_data['additional_info'], dict):
        additional_info = []
        for key, value in parsed_data['additional_info'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(additional_info) <= index:
                additional_info.append({})
            additional_info[index][sub_key] = value
        parsed_data['additional_info'] = additional_info
    
    # Convert scattered casts to list of dictionaries
    if 'casts' in parsed_data and isinstance(parsed_data['casts'], dict):
        casts = []
        for key, value in parsed_data['casts'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(casts) <= index:
                casts.append({})
            casts[index][sub_key] = value
        parsed_data['casts'] = casts
    
    if 'crews' in parsed_data and isinstance(parsed_data['crews'], dict):
        crews = []
        for key, value in parsed_data['crews'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(crews) <= index:
                crews.append({})
            crews[index][sub_key] = value
        parsed_data['crews'] = crews
    
    # Convert scattered books to list of dictionaries
    if 'books' in parsed_data and isinstance(parsed_data['books'], dict):
        books = []
        for key, value in parsed_data['books'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(books) <= index:
                books.append({})
            books[index][sub_key] = value
        parsed_data['books'] = books
    
    # Convert scattered soundtracks to list of dictionaries
    if 'soundtracks' in parsed_data and isinstance(parsed_data['soundtracks'], dict):
        soundtracks = []
        for key, value in parsed_data['soundtracks'].items():
            index = int(key.split('][')[0].lstrip('['))
            sub_key = key.split('[')[1].rstrip(']')
            if len(soundtracks) <= index:
                soundtracks.append({})
            soundtracks[index][sub_key] = value
        parsed_data['soundtracks'] = soundtracks
    
    # # Convert scattered crews to list of dictionaries with nested 'name' field
    # if 'crews' in parsed_data and isinstance(parsed_data['crews'], dict):
    #     crews = []
    #     for key, value in parsed_data['crews'].items():
    #         index = int(key.split('][')[0].lstrip('['))
    #         sub_key = key.split('[')[1].rstrip(']')

    #         # Ensure crews list is long enough to accommodate index
    #         while len(crews) <= index:
    #             crews.append({})

    #         # Handle nested 'name' field
    #         if sub_key == 'title':
    #             crews[index]['title'] = value
    #         elif sub_key == 'name':
    #             if 'name' not in crews[index]:
    #                 crews[index]['name'] = []
    #             crews[index]['name'].append({'name': value})
                
    #     parsed_data['crews'] = crews


    return parsed_data



def event_parse_querydict(query_dict):
    def parse_key(key):
        keys = key.split('[')
        parsed_keys = [keys[0]]
        for k in keys[1:]:
            parsed_keys.append(k[:-1])
        return parsed_keys

    def set_nested_item(d, keys, value):
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value

    data = defaultdict(dict)
    for key, value in query_dict.items():
        keys = parse_key(key)
        set_nested_item(data, keys, value)
    
    # Convert defaultdict back to a regular dict
    return dict(data)