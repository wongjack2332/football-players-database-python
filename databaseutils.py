def generate_regex(input_string):
    regex_parts = []

    for char in input_string:
        regex_parts.append(f"(?=.*{re.escape(char)})")

    regex = "^" + "".join(regex_parts) + ".*"
    return regex


def player_entry(player_dict, *args):
    keys = list(player_dict.keys())
    index = f"{len(keys)+1:04d}"
    row = args
    if len(row) != 12:
        return "incorrect amount of attributes"
    if row in list(player_dict.values()):
        return "player already exists"
    player_dict[index] = row
    return None


def match_player_name_exact(df, name):
    return df[(df["firstname"] + " " + df["lastname"]).str.contains(name)]


def match_player_name_any(df, name):
    """allow any character and any number of characters between each character in name"""
    return df[
        (df["firstname"] + " " + df["lastname"]).str.contains(
            generate_regex(name), regex=True
        )
    ]


def player_search(df, exact=True, **kwargs):
    """error code:
    -1: invalid attribute name"""
    for key in list(kwargs.keys())[1:]:
        if key not in list(df.columns):
            return -1
    if exact:
        result_df = match_player_name_exact(df, kwargs["name"])
    else:
        result_df = match_player_name_any(df, kwargs["name"])
    for k, v in list(kwargs.items())[1:]:
        result_df = result_df[result_df[k].str.contains(v)]
    return result_df


def parse_search_command(string):
    """error code:
    -1: missing value"""
    string = string.split("#")
    name = string.pop(0)
    string_dict = {"name": name.lower().strip()}
    for i in string:
        s = i.split()
        if len(s) < 2:
            return -1
        tag, text = s
        string_dict[tag] = text
    return string_dict
