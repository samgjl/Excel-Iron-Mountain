# Credit to GeeksforGeeks for the ANSI codes! 
# https://www.geeksforgeeks.org/how-to-add-colour-to-text-python/

class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)
    
    def header(h: str) -> None:
        print(ANSI.color_text(35) + h + ANSI.color_text(39))
        
    def info(i: str) -> None:
        print(ANSI.color_text(34) + i + ANSI.color_text(39))
    
    def warn(w: str) -> None:
        print(ANSI.color_text(33) + w + ANSI.color_text(39))
    
    def error(e: str) -> None:
        print(ANSI.color_text(31) + e + ANSI.color_text(39))
        exit(1)

    def success(s: str) -> None:
        print(ANSI.color_text(32) + s + ANSI.color_text(39))