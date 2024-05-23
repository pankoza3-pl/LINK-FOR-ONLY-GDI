import os

class Dosya:
    def __init__(self):
        pass

    def olustur(self, dosya_adi, icerik):
        dosya_yolu = os.path.join(os.getcwd(), dosya_adi)
        with open(dosya_yolu, 'w') as dosya:
            dosya.write("\n".join(map(str, icerik)))

if __name__ == "__main__":
    icerik = [
        "org 0x7c00",
        "bits 16",
        "",
        "start:",
        "   call cls",
        "   mov bx, display",
        "",
        "print:"
        "",
        "   mov al, [bx]",
        "   cmp al, 0",
        "   je halt",
        "   call print_char",
        "   inc bc",
        "   jmp print"
        "",
        "print_char:",
        "   mov ah, 0x0e",
        "   int 0x10",
        "   ret",
        "",
        "",
        "halt:",
        "   ret"
        "",
        "cls:",
        "   mov ah, 0x07",
        "   mov al, 0x00",
        "   mov bh, 0x04",
        "   mov cx, 0x00",
        "   mov dx, 0x184f",
        "   int 0x10",
        "   ret",
        "",
        "display db \"Your system non usable!\", 13, 10, \"Hexadecimalexe\", 13, 10, 0",
        "times 510 - ($ - $$) db 0",
        "dw 0xaa55"
    ]

    dosya_adi = "boot.asm"

    yeni_dosya = Dosya()
    yeni_dosya.olustur(dosya_adi, icerik)