import datetime

def get_message():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Health check OK — Leo Stephen Pipeline — {now}"

if __name__ == "__main__":
    print(get_message())
