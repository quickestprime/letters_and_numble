def sample_from_dict(dictionary):
    return random.choices(list(dictionary.keys()), weights=dictionary.values())[0]
