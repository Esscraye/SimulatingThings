class Snippet:
    @staticmethod
    def couleur(degrade, coefficient=0):
        if not degrade:
            return 14, 248, 244
        coefficient = coefficient % 1530

        if coefficient < 255:
            rouge, vert, bleu = 255, 127.5 + coefficient / 2, 0
        elif coefficient < 510:
            rouge, vert, bleu = 510 - coefficient, 255, 0
        elif coefficient < 765:
            rouge, vert, bleu = 0, 255, coefficient - 510
        elif coefficient < 1020:
            rouge, vert, bleu = 0, 1020 - coefficient + (coefficient % 765) / 2, 255
        elif coefficient <= 1275:
            rouge, vert, bleu = coefficient - 1020, 127.5, 255
        else:
            rouge, vert, bleu = 255, 127.5, 1530 - coefficient
        return rouge, vert, bleu
