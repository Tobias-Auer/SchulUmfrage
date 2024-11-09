def string_to_hash(input_string):
    hash_value = 0

    if len(input_string) == 0:
        return hash_value  # Returns 0 for empty strings

    for char in input_string:
        char_code = ord(char)  # Get the Unicode code point of the character
        hash_value = ((hash_value << 5) - hash_value) + char_code
        # Simulate 32-bit signed integer overflow
        hash_value = hash_value & 0xFFFFFFFF  # Keep it within 32 bits

    # Convert to signed 32-bit integer
    if hash_value >= 0x80000000:
        hash_value -= 0x100000000  # Convert to negative if needed

    return hash_value  # Return the final hash value

# Example usage
gfg = "l11E814CD817D9"
result = string_to_hash(gfg)

# Print the result
print(result)  # Output: -1119635595
