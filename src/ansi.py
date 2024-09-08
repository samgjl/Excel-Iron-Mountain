# Credit to GeeksforGeeks for the ANSI codes! 
# https://www.geeksforgeeks.org/how-to-add-colour-to-text-python/

class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)
    
    # Purple
    def header(h: str) -> None:
        print(ANSI.color_text(35) + h + ANSI.color_text(39))

    # Blue 
    def info(i: str) -> None:
        print(ANSI.color_text(36) + i + ANSI.color_text(39))
        
    # Yellow
    def warn(w: str) -> None:
        print(ANSI.color_text(33) + w + ANSI.color_text(39))
    
    # Red
    def error(e: str) -> None:
        print(ANSI.color_text(31) + e + ANSI.color_text(39))
        exit(1)

    # Green
    def success(s: str) -> None:
        print(ANSI.color_text(32) + s + ANSI.color_text(39))

if __name__ == "__main__":
    example_ansi = ANSI.background(
    97) + ANSI.color_text(35) + ANSI.style_text(4) + "Here's an example of ANSI codes!" + ANSI.color_text(39) + ANSI.background(49)
    print(example_ansi)

        