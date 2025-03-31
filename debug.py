

def get_location(all_info):
    if 'smap' in all_info and len(all_info['smap']) > 0:
        return 'in sail'

    if 'dmap' in all_info and len(all_info['dmap']) > 0:
        if 'daura' in all_info['hero'] and len(all_info['hero']['daura']) > 0:
            return all_info['hero']['daura'] + ' (dungeon)'
        return 'in dungeon'

    if 'r_map' in all_info and len(all_info['r_map']) > 0:
        return 'in royale'

    if 'opponent' in all_info:
        return 'in arena'

    return all_info['hero']['town_name']


def print_debug(all_info, action_availability):
    hero_info = all_info['hero']

    print('-'*50)
    print('location:', get_location(all_info))
    print('-'*50)
    keys = [
        # 'd_a', 'd_send_after',
        # 's_a', 's_send_after', 's_progress',
        # 'r_a', 'r_after', 'r_t',
        'is_chf_available', 'chf_pending', 'chfr_after',

        'fight_type',

        # 'arena_fight', 'arena_send_after',
        # 'a_cmd', 'arena_god_cmd_disabled',
        # 'is_arena_available', 'is_arena_disabled',

        'c_town', 'in_town', 'town_name',
        # 'diary_last',

        # 'health',
        # 'godpower',
        # 'retirement', 'gold', 

    ]

    # for key in hero_info:
    #     if key not in keys:
    #         keys.append(key)
    keys.sort()

    max_key_len = max([len(key) for key in keys])
    for key in keys:
        if key in hero_info:
            print(key.rjust(max_key_len) + ': ', hero_info[key])
        else:
            print(key.rjust(max_key_len) + ': ', 'N/A')

    print('-'*50)
    from pprint import pprint
    pprint(action_availability)
    print('-'*50)


    import math
    for key in ['arena_send_after', 'd_send_after', 's_send_after', 'r_after']:
        # if hero_info[key] == 0:
        #     continue

        seconds = hero_info[key]
        hours = math.floor(seconds / 3600)
        seconds -= hours * 3600
        minutes = math.ceil(seconds / 60)

        print(key, f'{hours:01}:{minutes:02}')



    print('-'*50)
