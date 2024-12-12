from .rocket_reach import RocketReach


def fill_data_into_rocket_reach(data: list, delay: int):
    processed_list = []
    un_successful_list = []
    try:
        j = RocketReach(proxy='')
        for username, email in data:
            if j.fill_information(
                username=username,
                email=email,
                password=email,
                delay=delay
            ):
                processed_list.append([username, email])
            else:
                un_successful_list.append([username, email])
    except (Exception) as e:
        print(e)
        pass

    return processed_list, un_successful_list
