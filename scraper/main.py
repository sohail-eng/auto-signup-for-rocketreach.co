from .rocket_reach import RocketReach


def fill_data_into_rocket_reach(data: list, driver):
    processed_list = []
    un_successful_list = []
    try:
        j = RocketReach(proxy='', driver=driver)
        for username, email in data:
            if j.fill_information(
                username=username,
                email=email,
                password=email
            ):
                if j.no_browser:
                    break
                processed_list.append([username, email])
            else:
                un_successful_list.append([username, email])
    except (Exception) as e:
        print(e)
        pass

    return processed_list, un_successful_list
