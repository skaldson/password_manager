def delete_rspace(user_str: str) -> str:
    temp = user_str.rsplit()
    temp = ' '.join(temp)

    if temp == ' ':
        return ''
    else:
        return temp
