
def get_account_limit():
    try:
        with open("limit_account.txt", "r") as f:
            account_limit = f.read().strip()
        return int(account_limit)
    except FileNotFoundError:
        print("No saved data found.")
    except ValueError:
        print("No valid data")
    except Exception as e:
        print(f"Error loading data: {e}")
    return 10

def get_initial_link():
    try:
        with open("initial_link.txt", "r") as f:
            initial_link = f.read().strip()
        return initial_link
    except FileNotFoundError:
        print("No saved data found.")
    except ValueError:
        print("No valid data")
    except Exception as e:
        print(f"Error loading data: {e}")
    return 10
