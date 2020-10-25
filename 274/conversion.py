def dec_to_base(number, base):
    """
    Input: number is the number to be converted
           base is the new base  (eg. 2, 6, or 8)
    Output: the converted number in the new base without the prefix (eg. '0b')
    """
    if number < base:
        return number
    else:
        quotient, remainder = divmod(number, base)
        return 10 * dec_to_base(quotient, base) + remainder


if __name__ == "__main__":
    nums = [24, 177, 256, 1024, 2020]

    for num in nums:
        print(dec_to_base(num, 8))
